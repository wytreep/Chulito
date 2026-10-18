import unittest

from confirma_vertical_slice import CaptureEnvelope, SQLiteLedger


TENANT = 'store-001'
TIME = '2026-10-13T14:00:00-05:00'
RECEIVED = '2026-10-13T14:00:02-05:00'


def email_notice(reference='NQ-001', message_id='mail-001', amount='12.500', tenant=TENANT):
    ref_line = f'Referencia: {reference}\n' if reference else ''
    return CaptureEnvelope.from_email(tenant, {
        'message_id': message_id,
        'from': 'avisos@nequi.fixture.invalid',
        'subject': 'Nequi — pago recibido (fixture sintético)',
        'body': (
            'Emisor: Nequi\n'
            f'Monto: COP {amount}\n'
            f'Fecha de transacción: {TIME}\n'
            f'{ref_line}'
        ),
        'received_at_utc': RECEIVED,
    })


def android_notice(reference='NQ-001', notification_key='notif-001', amount='12.500', tenant=TENANT):
    ref_line = f'Referencia: {reference}\n' if reference else ''
    return CaptureEnvelope.from_android(tenant, {
        'notification_key': notification_key,
        'package': 'com.nequi.fixture.invalid',
        'title': 'Nequi — pago recibido (fixture sintético)',
        'text': (
            'Emisor: Nequi\n'
            f'Monto: COP {amount}\n'
            f'Fecha de transacción: {TIME}\n'
            f'{ref_line}'
        ),
        'posted_at_utc': RECEIVED,
    })


class VerticalSliceTests(unittest.TestCase):
    def setUp(self):
        self.ledger = SQLiteLedger()
        self.ledger.add_charge(
            'charge-001', TENANT, 12500, 'NQ-001', '2026-10-13T13:55:00-05:00'
        )

    def tearDown(self):
        self.ledger.close()

    def test_email_capture_normalizes_and_confirms_exact_charge(self):
        result = self.ledger.ingest(email_notice())
        self.assertEqual(result.outcome, 'new_payment')
        self.assertEqual(result.match_status, 'confirmed')
        payment = self.ledger.get_payment(result.payment_key)
        self.assertEqual(payment['amount_cop'], 12500)
        self.assertEqual(payment['currency'], 'COP')
        self.assertEqual(payment['issuer'], 'NEQUI_FIXTURE')
        self.assertEqual(payment['reference'], 'NQ-001')
        self.assertEqual(self.ledger.get_charge('charge-001')['status'], 'confirmed')

    def test_same_source_event_retry_is_idempotent(self):
        first = self.ledger.ingest(email_notice())
        second = self.ledger.ingest(email_notice())
        self.assertEqual(first.match_status, 'confirmed')
        self.assertEqual(second.outcome, 'duplicate_event')
        self.assertEqual(self.ledger.payment_count(TENANT), 1)
        self.assertEqual(self.ledger.event_count(), 1)

    def test_same_transaction_observed_by_email_and_android_is_one_payment(self):
        email_result = self.ledger.ingest(email_notice())
        android_result = self.ledger.ingest(android_notice())
        self.assertEqual(email_result.match_status, 'confirmed')
        self.assertEqual(android_result.outcome, 'duplicate_transaction')
        self.assertEqual(self.ledger.payment_count(TENANT), 1)
        self.assertEqual(self.ledger.event_count(), 2)

    def test_amount_discrepancy_is_doubtful_not_confirmed(self):
        self.ledger = SQLiteLedger()
        self.ledger.add_charge(
            'charge-mismatch', TENANT, 13000, 'NQ-001', '2026-10-13T13:55:00-05:00'
        )
        result = self.ledger.ingest(email_notice())
        self.assertEqual(result.match_status, 'doubtful')
        self.assertEqual(self.ledger.get_charge('charge-mismatch')['status'], 'doubtful')
        self.assertEqual(self.ledger.connection.execute('SELECT COUNT(*) FROM confirmed_matches').fetchone()[0], 0)

    def test_reference_discrepancy_is_doubtful_not_confirmed(self):
        result = self.ledger.ingest(email_notice(reference='NQ-DIFFERENT'))
        self.assertEqual(result.match_status, 'doubtful')
        self.assertEqual(self.ledger.get_charge('charge-001')['status'], 'doubtful')

    def test_nearby_unrelated_charge_stays_pending(self):
        self.ledger = SQLiteLedger()
        self.ledger.add_charge(
            'unrelated', TENANT, 99000, 'OTHER-REF', '2026-10-13T13:59:00-05:00'
        )
        result = self.ledger.ingest(email_notice())
        self.assertEqual(result.match_status, 'unmatched')
        self.assertEqual(self.ledger.get_charge('unrelated')['status'], 'pending')

    def test_missing_reference_needs_manual_review(self):
        result = self.ledger.ingest(email_notice(reference=None))
        self.assertEqual(result.match_status, 'review')
        self.assertEqual(self.ledger.get_charge('charge-001')['status'], 'pending')

    def test_cross_tenant_charge_is_not_visible_or_matched(self):
        self.ledger = SQLiteLedger()
        self.ledger.add_charge(
            'charge-other', 'store-002', 12500, 'NQ-001', '2026-10-13T13:55:00-05:00'
        )
        result = self.ledger.ingest(email_notice())
        self.assertEqual(result.match_status, 'unmatched')
        self.assertEqual(self.ledger.get_charge('charge-other')['status'], 'pending')
        self.assertEqual(self.ledger.payment_count('store-002'), 0)

    def test_unknown_sender_is_recorded_as_unparsed_not_as_payment(self):
        unknown = CaptureEnvelope.from_email(TENANT, {
            'message_id': 'unknown-001',
            'from': 'avisos@banco.fixture.invalid',
            'subject': 'Notificación sintética no reconocida',
            'body': 'Contenido de prueba sin formato registrado.',
            'received_at_utc': RECEIVED,
        })
        result = self.ledger.ingest(unknown)
        self.assertEqual(result.outcome, 'unparsed')
        self.assertEqual(self.ledger.payment_count(TENANT), 0)
        self.assertEqual(self.ledger.event_count(), 1)

    def test_distinct_transaction_references_do_not_collapse(self):
        self.ledger = SQLiteLedger()
        first = self.ledger.ingest(email_notice(reference='NQ-001', message_id='mail-a'))
        second = self.ledger.ingest(email_notice(reference='NQ-002', message_id='mail-b'))
        self.assertNotEqual(first.payment_key, second.payment_key)
        self.assertEqual(self.ledger.payment_count(TENANT), 2)

    def test_multiple_exact_charges_are_ambiguous(self):
        self.ledger.add_charge(
            'charge-002', TENANT, 12500, 'NQ-001', '2026-10-13T13:58:00-05:00'
        )
        result = self.ledger.ingest(email_notice())
        self.assertEqual(result.match_status, 'review')
        self.assertEqual(self.ledger.get_charge('charge-001')['status'], 'pending')
        self.assertEqual(self.ledger.get_charge('charge-002')['status'], 'pending')

    def test_exact_match_plus_candidate_without_reference_is_ambiguous(self):
        self.ledger.add_charge(
            'charge-002', TENANT, 12500, None, '2026-10-13T13:58:00-05:00'
        )
        result = self.ledger.ingest(email_notice())
        self.assertEqual(result.match_status, 'review')
        self.assertEqual(self.ledger.get_charge('charge-001')['status'], 'pending')
        self.assertEqual(self.ledger.get_charge('charge-002')['status'], 'pending')


if __name__ == '__main__':
    unittest.main()
