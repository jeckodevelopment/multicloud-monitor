import unittest
from scripts.update_feed import parse_feed

class FeedParsingTests(unittest.TestCase):
    def test_regions_and_stable_ids(self):
        xml = b"""<rss><channel><item><title>Inter-region issue</title>
        <guid>incident-123</guid><description>Italy North and Germany West Central impacted</description>
        <pubDate>Fri, 13 Nov 2026 08:00:00 GMT</pubDate>
        <link>https://azure.status.microsoft/en-us/status/history/</link>
        </item></channel></rss>"""
        result = parse_feed(xml)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "incident-123")
        self.assertTrue(result[0]["italy"])
        self.assertTrue(result[0]["germany"])
        self.assertEqual(result[0]["when"], "2026-11-13T08:00:00Z")

    def test_unlocalized_event_not_attributed(self):
        xml = b"<rss><channel><item><title>Global event</title><guid>g2</guid></item></channel></rss>"
        item = parse_feed(xml)[0]
        self.assertFalse(item["italy"])
        self.assertFalse(item["germany"])

if __name__ == "__main__":
    unittest.main()
