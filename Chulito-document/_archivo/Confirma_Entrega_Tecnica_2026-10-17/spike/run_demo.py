import json

from confirma_vertical_slice import CaptureEnvelope, SQLiteLedger


ledger = SQLiteLedger()
ledger.add_charge(
    'charge-001', 'store-001', 12500, 'NQ-001', '2026-10-13T13:55:00-05:00'
)

common_text = (
    'Emisor: Nequi\n'
    'Monto: COP 12.500\n'
    'Fecha de transacción: 2026-10-13T14:00:00-05:00\n'
    'Referencia: NQ-001\n'
)
email = CaptureEnvelope.from_email('store-001', {
    'message_id': 'mail-001',
    'from': 'avisos@nequi.fixture.invalid',
    'subject': 'Nequi — pago recibido (fixture sintético)',
    'body': common_text,
    'received_at_utc': '2026-10-13T14:00:02-05:00',
})
android = CaptureEnvelope.from_android('store-001', {
    'notification_key': 'notif-001',
    'package': 'com.nequi.fixture.invalid',
    'title': 'Nequi — pago recibido (fixture sintético)',
    'text': common_text,
    'posted_at_utc': '2026-10-13T14:00:02-05:00',
})

first = ledger.ingest(email)
second = ledger.ingest(android)
print(json.dumps({
    'synthetic_only': True,
    'email_capture': first.__dict__,
    'android_observation': second.__dict__,
    'canonical_payment_count': ledger.payment_count('store-001'),
    'capture_event_count': ledger.event_count(),
    'charge_status': ledger.get_charge('charge-001')['status'],
}, ensure_ascii=False, indent=2))
ledger.close()
