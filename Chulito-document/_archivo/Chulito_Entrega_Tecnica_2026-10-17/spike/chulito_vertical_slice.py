"""Vertical slice sintética de captura, normalización, deduplicación y conciliación.

No contiene formatos reales de Nequi/Daviplata ni persiste contenido crudo. Es una
prueba del contrato y las reglas de dominio, no una integración con emisores.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import re
import sqlite3
from typing import Optional


class UnrecognizedMessage(ValueError):
    """No hay parser compatible con el origen o fixture recibido."""


class InvalidMessage(ValueError):
    """El fixture fue reconocido, pero faltan campos indispensables o son inválidos."""


def parse_datetime(value: str) -> datetime:
    normalized = value.strip().replace('Z', '+00:00')
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise InvalidMessage('La fecha debe incluir zona horaria u offset.')
    return parsed.astimezone(timezone.utc)


def utc_iso(value: datetime | str) -> str:
    parsed = parse_datetime(value) if isinstance(value, str) else value.astimezone(timezone.utc)
    return parsed.isoformat(timespec='seconds')


def digest(value: str) -> str:
    return sha256(value.encode('utf-8')).hexdigest()


@dataclass(frozen=True)
class CaptureEnvelope:
    tenant_id: str
    channel: str
    source_event_id: Optional[str]
    source_name: str
    title: str
    text: str
    received_at_utc: str

    def __post_init__(self):
        if not self.tenant_id.strip():
            raise ValueError('tenant_id es obligatorio.')
        if self.channel not in {'email_forward', 'android_listener'}:
            raise ValueError(f'Canal no soportado por este spike: {self.channel}')
        object.__setattr__(self, 'received_at_utc', utc_iso(self.received_at_utc))

    @property
    def payload_fingerprint(self) -> str:
        # No incluye el instante de recepción: un reenvío/reintento no cambia el hash
        # cuando el contenido sintético permanece idéntico.
        material = '\x1f'.join((self.source_name.strip().lower(), self.title.strip(), self.text.strip()))
        return digest(material)

    @classmethod
    def from_email(cls, tenant_id: str, payload: dict) -> 'CaptureEnvelope':
        return cls(
            tenant_id=tenant_id,
            channel='email_forward',
            source_event_id=payload.get('message_id'),
            source_name=payload.get('from', ''),
            title=payload.get('subject', ''),
            text=payload.get('body', ''),
            received_at_utc=payload['received_at_utc'],
        )

    @classmethod
    def from_android(cls, tenant_id: str, payload: dict) -> 'CaptureEnvelope':
        return cls(
            tenant_id=tenant_id,
            channel='android_listener',
            source_event_id=payload.get('notification_key'),
            source_name=payload.get('package', ''),
            title=payload.get('title', ''),
            text=payload.get('text', ''),
            received_at_utc=payload['posted_at_utc'],
        )


@dataclass(frozen=True)
class PaymentNotice:
    tenant_id: str
    issuer: str
    amount_cop: int
    occurred_at_utc: str
    reference: Optional[str]
    operation_type: str
    source_channel: str
    source_event_id: Optional[str]
    received_at_utc: str
    payload_fingerprint: str


class NequiFixtureParser:
    """Parser deliberadamente limitado a los fixtures inventados para esta prueba."""

    issuer = 'NEQUI_FIXTURE'
    _amount = re.compile(r'Monto:\s*(?:COP\s*)?\$?\s*([0-9][0-9.]*)', re.IGNORECASE)
    _occurred = re.compile(r'Fecha de transacci[oó]n:\s*([^\r\n]+)', re.IGNORECASE)
    _reference = re.compile(r'Referencia:\s*([A-Za-z0-9_-]+)', re.IGNORECASE)

    def can_parse(self, envelope: CaptureEnvelope) -> bool:
        source = f'{envelope.source_name} {envelope.title}'.lower()
        return 'nequi' in source

    def parse(self, envelope: CaptureEnvelope) -> PaymentNotice:
        if not self.can_parse(envelope):
            raise UnrecognizedMessage('No se reconoce el emisor sintético.')
        amount_match = self._amount.search(envelope.text)
        occurred_match = self._occurred.search(envelope.text)
        if not amount_match or not occurred_match:
            raise InvalidMessage('Fixture reconocido sin monto o fecha de transacción.')
        amount = int(amount_match.group(1).replace('.', ''))
        if amount <= 0:
            raise InvalidMessage('El monto debe ser positivo.')
        try:
            occurred = utc_iso(occurred_match.group(1))
        except (ValueError, TypeError) as exc:
            raise InvalidMessage('Fecha de transacción inválida.') from exc
        reference_match = self._reference.search(envelope.text)
        reference = reference_match.group(1).strip() if reference_match else None
        return PaymentNotice(
            tenant_id=envelope.tenant_id,
            issuer=self.issuer,
            amount_cop=amount,
            occurred_at_utc=occurred,
            reference=reference,
            operation_type='credit',
            source_channel=envelope.channel,
            source_event_id=envelope.source_event_id,
            received_at_utc=envelope.received_at_utc,
            payload_fingerprint=envelope.payload_fingerprint,
        )


class ParserRegistry:
    def __init__(self, parsers=None):
        self.parsers = list(parsers or [NequiFixtureParser()])

    def parse(self, envelope: CaptureEnvelope) -> PaymentNotice:
        for parser in self.parsers:
            if parser.can_parse(envelope):
                return parser.parse(envelope)
        raise UnrecognizedMessage('No hay parser registrado para este emisor.')


@dataclass(frozen=True)
class IngestResult:
    outcome: str
    payment_key: Optional[str] = None
    match_status: Optional[str] = None
    reason: Optional[str] = None


class SQLiteLedger:
    """Almacén efímero; el prototipo no escribe contenido crudo de notificaciones."""

    def __init__(self, database: str = ':memory:', match_window_seconds: int = 600):
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self.match_window_seconds = match_window_seconds
        self._create_schema()

    def close(self):
        self.connection.close()

    def _create_schema(self):
        self.connection.executescript('''
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS expected_charges (
            charge_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            amount_cop INTEGER NOT NULL CHECK (amount_cop > 0),
            reference TEXT,
            created_at_utc TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        );
        CREATE INDEX IF NOT EXISTS ix_charges_tenant_status
            ON expected_charges(tenant_id, status, created_at_utc);
        CREATE TABLE IF NOT EXISTS payments (
            payment_key TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            issuer TEXT NOT NULL,
            amount_cop INTEGER NOT NULL CHECK (amount_cop > 0),
            currency TEXT NOT NULL CHECK (currency = 'COP'),
            occurred_at_utc TEXT NOT NULL,
            reference TEXT,
            operation_type TEXT NOT NULL,
            first_channel TEXT NOT NULL,
            first_source_event_id TEXT,
            first_received_at_utc TEXT NOT NULL,
            dedup_basis TEXT NOT NULL,
            match_status TEXT NOT NULL,
            match_reason TEXT,
            candidate_charge_ids TEXT NOT NULL DEFAULT '[]'
        );
        CREATE INDEX IF NOT EXISTS ix_payments_tenant_time
            ON payments(tenant_id, occurred_at_utc);
        CREATE TABLE IF NOT EXISTS capture_events (
            ingestion_key TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            channel TEXT NOT NULL,
            source_event_id TEXT,
            payload_fingerprint TEXT NOT NULL,
            received_at_utc TEXT NOT NULL,
            outcome TEXT NOT NULL,
            payment_key TEXT,
            detail TEXT
        );
        CREATE TABLE IF NOT EXISTS confirmed_matches (
            payment_key TEXT PRIMARY KEY REFERENCES payments(payment_key),
            charge_id TEXT NOT NULL UNIQUE REFERENCES expected_charges(charge_id),
            matched_at_utc TEXT NOT NULL
        );
        ''')
        self.connection.commit()

    def add_charge(self, charge_id: str, tenant_id: str, amount_cop: int,
                   reference: Optional[str], created_at_utc: str):
        self.connection.execute(
            '''INSERT INTO expected_charges
               (charge_id, tenant_id, amount_cop, reference, created_at_utc, status)
               VALUES (?, ?, ?, ?, ?, 'pending')''',
            (charge_id, tenant_id, amount_cop, reference, utc_iso(created_at_utc)),
        )
        self.connection.commit()

    @staticmethod
    def _ingestion_key(envelope: CaptureEnvelope) -> str:
        stable = envelope.source_event_id or envelope.payload_fingerprint
        return digest(f'ingest|{envelope.tenant_id}|{envelope.channel}|{stable}')

    @staticmethod
    def _payment_key(payment: PaymentNotice) -> tuple[str, str]:
        if payment.reference:
            # La unicidad de referencia por emisor es una hipótesis que requiere
            # validación por emisor antes de una integración de producción.
            material = f'transaction|{payment.tenant_id}|{payment.issuer}|{payment.reference.strip().upper()}'
            return digest(material), 'issuer_reference'
        # Sin referencia no se deduplica entre canales: es más seguro permitir revisión
        # que fusionar dos transacciones legítimas del mismo monto/instante.
        material = f'fallback|{payment.tenant_id}|{payment.source_channel}|{payment.payload_fingerprint}'
        return digest(material), 'channel_payload_fingerprint'

    def ingest(self, envelope: CaptureEnvelope, registry: Optional[ParserRegistry] = None) -> IngestResult:
        registry = registry or ParserRegistry()
        ingestion_key = self._ingestion_key(envelope)
        prior_event = self.connection.execute(
            'SELECT payment_key, outcome FROM capture_events WHERE ingestion_key = ?',
            (ingestion_key,),
        ).fetchone()
        if prior_event:
            return IngestResult('duplicate_event', prior_event['payment_key'], reason='Reintento del mismo evento de captura.')

        try:
            notice = registry.parse(envelope)
        except (UnrecognizedMessage, InvalidMessage) as exc:
            outcome = 'unparsed' if isinstance(exc, UnrecognizedMessage) else 'invalid'
            self.connection.execute(
                '''INSERT INTO capture_events
                   (ingestion_key, tenant_id, channel, source_event_id, payload_fingerprint,
                    received_at_utc, outcome, payment_key, detail)
                   VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?)''',
                (ingestion_key, envelope.tenant_id, envelope.channel, envelope.source_event_id,
                 envelope.payload_fingerprint, envelope.received_at_utc, outcome, str(exc)),
            )
            self.connection.commit()
            return IngestResult(outcome, reason=str(exc))

        payment_key, dedup_basis = self._payment_key(notice)
        existing_payment = self.connection.execute(
            'SELECT payment_key, match_status FROM payments WHERE payment_key = ?',
            (payment_key,),
        ).fetchone()
        if existing_payment:
            self.connection.execute(
                '''INSERT INTO capture_events
                   (ingestion_key, tenant_id, channel, source_event_id, payload_fingerprint,
                    received_at_utc, outcome, payment_key, detail)
                   VALUES (?, ?, ?, ?, ?, ?, 'duplicate_transaction', ?, ?)''',
                (ingestion_key, envelope.tenant_id, envelope.channel, envelope.source_event_id,
                 envelope.payload_fingerprint, envelope.received_at_utc, payment_key,
                 'Misma identidad de transacción ya vista; se conserva un solo pago.'),
            )
            self.connection.commit()
            return IngestResult('duplicate_transaction', payment_key, existing_payment['match_status'])

        self.connection.execute(
            '''INSERT INTO payments
               (payment_key, tenant_id, issuer, amount_cop, currency, occurred_at_utc,
                reference, operation_type, first_channel, first_source_event_id,
                first_received_at_utc, dedup_basis, match_status)
               VALUES (?, ?, ?, ?, 'COP', ?, ?, ?, ?, ?, ?, ?, 'unmatched')''',
            (payment_key, notice.tenant_id, notice.issuer, notice.amount_cop,
             notice.occurred_at_utc, notice.reference, notice.operation_type,
             notice.source_channel, notice.source_event_id, notice.received_at_utc, dedup_basis),
        )
        self.connection.execute(
            '''INSERT INTO capture_events
               (ingestion_key, tenant_id, channel, source_event_id, payload_fingerprint,
                received_at_utc, outcome, payment_key, detail)
               VALUES (?, ?, ?, ?, ?, ?, 'new_payment', ?, ?)''',
            (ingestion_key, envelope.tenant_id, envelope.channel, envelope.source_event_id,
             envelope.payload_fingerprint, envelope.received_at_utc, payment_key,
             f'dedup_basis={dedup_basis}'),
        )
        result = self._reconcile(payment_key, notice)
        self.connection.commit()
        return IngestResult('new_payment', payment_key, result['status'], result['reason'])

    def _reconcile(self, payment_key: str, notice: PaymentNotice) -> dict:
        payment_time = parse_datetime(notice.occurred_at_utc)
        rows = self.connection.execute(
            '''SELECT * FROM expected_charges
               WHERE tenant_id = ? AND status = 'pending' ''',
            (notice.tenant_id,),
        ).fetchall()
        in_window = []
        for row in rows:
            delta = (payment_time - parse_datetime(row['created_at_utc'])).total_seconds()
            if 0 <= delta <= self.match_window_seconds:
                in_window.append(row)

        exact = []
        amount_candidates_without_ref = []
        for row in in_window:
            if row['amount_cop'] != notice.amount_cop:
                continue
            charge_ref = row['reference']
            if charge_ref and notice.reference:
                if charge_ref.strip().upper() == notice.reference.strip().upper():
                    exact.append(row)
            else:
                amount_candidates_without_ref.append(row)

        if len(exact) == 1 and not amount_candidates_without_ref:
            charge = exact[0]
            self.connection.execute(
                'UPDATE payments SET match_status = ?, match_reason = ? WHERE payment_key = ?',
                ('confirmed', 'Monto, referencia y ventana temporal coinciden exactamente.', payment_key),
            )
            self.connection.execute(
                'UPDATE expected_charges SET status = ? WHERE charge_id = ?',
                ('confirmed', charge['charge_id']),
            )
            self.connection.execute(
                'INSERT INTO confirmed_matches(payment_key, charge_id, matched_at_utc) VALUES (?, ?, ?)',
                (payment_key, charge['charge_id'], utc_iso(datetime.now(timezone.utc))),
            )
            return {'status': 'confirmed', 'reason': 'Coincidencia exacta y única.'}

        if len(exact) > 1 or amount_candidates_without_ref:
            candidates = exact + amount_candidates_without_ref
            reason = 'Hay varias coincidencias posibles o falta una referencia; requiere revisión del cajero.'
            self.connection.execute(
                'UPDATE payments SET match_status = ?, match_reason = ?, candidate_charge_ids = ? WHERE payment_key = ?',
                ('review', reason, json.dumps([r['charge_id'] for r in candidates]), payment_key),
            )
            return {'status': 'review', 'reason': reason}

        if in_window:
            discrepancy_candidates = [
                row for row in in_window
                if row['amount_cop'] == notice.amount_cop
                or (row['reference'] and notice.reference
                    and row['reference'].strip().upper() == notice.reference.strip().upper())
            ]
            if discrepancy_candidates:
                candidates = [r['charge_id'] for r in discrepancy_candidates]
                reason = 'Existe una candidata por monto o referencia, pero hay discrepancia; no confirmar automáticamente.'
                self.connection.execute(
                    'UPDATE payments SET match_status = ?, match_reason = ?, candidate_charge_ids = ? WHERE payment_key = ?',
                    ('doubtful', reason, json.dumps(candidates), payment_key),
                )
                self.connection.execute(
                    "UPDATE expected_charges SET status = 'doubtful' WHERE charge_id IN (%s)" % ','.join('?' * len(candidates)),
                    candidates,
                )
                return {'status': 'doubtful', 'reason': reason}

        reason = 'No hay cobro pendiente del mismo negocio dentro de la ventana configurada.'
        self.connection.execute(
            'UPDATE payments SET match_status = ?, match_reason = ? WHERE payment_key = ?',
            ('unmatched', reason, payment_key),
        )
        return {'status': 'unmatched', 'reason': reason}

    def payment_count(self, tenant_id: Optional[str] = None) -> int:
        if tenant_id is None:
            return self.connection.execute('SELECT COUNT(*) FROM payments').fetchone()[0]
        return self.connection.execute('SELECT COUNT(*) FROM payments WHERE tenant_id = ?', (tenant_id,)).fetchone()[0]

    def event_count(self) -> int:
        return self.connection.execute('SELECT COUNT(*) FROM capture_events').fetchone()[0]

    def get_charge(self, charge_id: str):
        return self.connection.execute('SELECT * FROM expected_charges WHERE charge_id = ?', (charge_id,)).fetchone()

    def list_payments(self, tenant_id: str):
        return self.connection.execute(
            'SELECT * FROM payments WHERE tenant_id = ? ORDER BY occurred_at_utc', (tenant_id,)
        ).fetchall()

    def get_payment(self, payment_key: str):
        return self.connection.execute('SELECT * FROM payments WHERE payment_key = ?', (payment_key,)).fetchone()
