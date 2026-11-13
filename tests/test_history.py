import unittest
from scripts.history import parse_history

class HistoryTests(unittest.TestCase):
    def test_tracking_date_and_region_classification(self):
        html = """<html><body>
        <h2>September 2026</h2><p>09/30/2026</p>
        <h3>Post Incident Review (PIR) – Gateway service degradation</h3>
        <p>Tracking ID: 7Q30-010</p><h4>What happened?</h4>
        <p>Incident in Germany West Central and other regions.</p>
        <h4>What went wrong and why?</h4><p>Details.</p>
        <p>09/29/2026</p><h3>Post Incident Review (PIR) – AI outage</h3>
        <p>Tracking ID: 7QL5-Z50</p><h4>What happened?</h4>
        <p>Sweden Central was impacted.</p></body></html>"""
        items = parse_history(html)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["id"], "pir:7Q30-010")
        self.assertEqual(items[0]["when"], "2026-09-30T00:00:00Z")
        self.assertTrue(items[0]["germany"])
        self.assertFalse(items[0]["italy"])
        self.assertIsNone(items[0]["impact_minutes"])
        self.assertFalse(items[1]["germany"])

    def test_html_without_pirs(self):
        self.assertEqual(parse_history("<html><body>No incidents</body></html>"), [])

if __name__ == "__main__":
    unittest.main()
