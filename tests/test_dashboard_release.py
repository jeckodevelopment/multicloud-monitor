"""Release-gate statico per dashboard HTML autonoma. Nessuna dipendenza pip."""
import hashlib
import json
import pathlib
import re
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "dashboard/cloud_service_monitor_multicloud_v3_1_10.html"
GCP_SCRIPT_SHA256 = "8e16759e77f24c59f91fa78a32330fefa7ec80c80594cc47aa8beb8eee3315b7"

class DashboardReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML.read_text(encoding="utf-8")
        cls.scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", cls.html, re.S | re.I)
        m = re.search(r"const AZURE_SLA_CATALOG\s*=\s*(\[.*?\]);", cls.html, re.S)
        if m is None:
            raise AssertionError("Azure SLA catalog missing")
        cls.catalog = json.loads(m.group(1))

    def test_single_file_contains_two_providers(self):
        for marker in ('id="googlePane"', 'id="azurePane"', 'id="pdfReport"', 'id="azPdf"'):
            self.assertIn(marker, self.html)
        self.assertEqual(len(self.scripts), 4)

    def test_google_script_regression_guard(self):
        self.assertEqual(hashlib.sha256(self.scripts[0].encode()).hexdigest(), GCP_SCRIPT_SHA256)

    def test_azure_inventory_coverage_is_accounted_for(self):
        self.assertEqual(len(self.catalog), 72)
        status = {e["status"] for e in self.catalog}
        self.assertEqual(status, {"varianti_documentate", "da_qualificare", "fuori_perimetro_sla_azure"})
        self.assertEqual(sum(e["status"] == "varianti_documentate" for e in self.catalog), 20)
        self.assertEqual(sum(e["status"] == "da_qualificare" for e in self.catalog), 42)
        self.assertEqual(sum(e["status"] == "fuori_perimetro_sla_azure" for e in self.catalog), 10)
        for x in self.catalog:
            self.assertIn("canonical", x)
            for variant in x["variants"]:
                self.assertTrue(0 < variant["target"] <= 100)
                self.assertIn("id", variant)

    def test_azure_pdf_regions_and_estimates(self):
        for phrase in ("Italy North", "Germany West Central", "Disponibilità stimata*", "Non calc."):
            self.assertIn(phrase, self.html)
        self.assertNotIn("Il registro incidenti della region è riportato nella pagina successiva", self.html)

    def test_azure_refresh_matches_periodic_cadence(self):
        self.assertIn("age>5760", self.html)
        self.assertNotIn("age>120;", self.html)
        self.assertIn("fonte non recente", self.html)

    def test_node_syntax_for_embedded_scripts(self):
        with tempfile.TemporaryDirectory() as tmp:
            for index, script in enumerate(self.scripts, 1):
                p = pathlib.Path(tmp) / f"script-{index}.js"
                p.write_text(script, encoding="utf-8")
                with self.subTest(script=index):
                    result = subprocess.run(["node", "--check", str(p)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)

if __name__ == "__main__":
    unittest.main()
