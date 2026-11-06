import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = (
    "Personal_Assistant.json",
    "CalendarAgent.JSON",
    "EmailAgent.json",
    "PhoneCallAgent.json",
)


class ExportedWorkflowTests(unittest.TestCase):
    def test_all_exports_are_valid_n8n_workflow_json(self):
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                path = ROOT / relative_path
                self.assertTrue(path.is_file(), f"Missing workflow export: {relative_path}")
                workflow = json.loads(path.read_text(encoding="utf-8"))

                self.assertIsInstance(workflow, dict)
                self.assertIsInstance(workflow.get("nodes"), list)
                self.assertIsInstance(workflow.get("connections"), dict)
                self.assertIsInstance(workflow.get("name"), str)
                self.assertTrue(workflow["name"].strip())
                self.assertFalse(
                    workflow.get("active", False),
                    "Export files must remain inactive until reviewed in the target n8n instance.",
                )

    def test_node_names_and_ids_are_unique(self):
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                workflow = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
                nodes = workflow["nodes"]
                names = [node.get("name") for node in nodes]
                ids = [node.get("id") for node in nodes]

                self.assertTrue(all(isinstance(name, str) and name for name in names))
                self.assertEqual(len(names), len(set(names)))
                self.assertTrue(all(isinstance(node_id, str) and node_id for node_id in ids))
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(all(node.get("type") for node in nodes))
                self.assertTrue(all(isinstance(node.get("typeVersion"), (int, float)) for node in nodes))

    def test_connection_sources_and_targets_exist(self):
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                workflow = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
                node_names = {node["name"] for node in workflow["nodes"]}

                for source, outputs in workflow["connections"].items():
                    self.assertIn(source, node_names, f"Unknown connection source: {source}")
                    self.assertIsInstance(outputs, dict)
                    for output_groups in outputs.values():
                        self.assertIsInstance(output_groups, list)
                        for group in output_groups:
                            self.assertIsInstance(group, list)
                            for edge in group:
                                self.assertIn(edge.get("node"), node_names)

    def test_exports_do_not_contain_common_live_secret_formats(self):
        patterns = (
            re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            re.compile(r"\bBearer\s+[A-Za-z0-9._-]{24,}", re.IGNORECASE),
        )
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                content = (ROOT / relative_path).read_text(encoding="utf-8")
                for pattern in patterns:
                    self.assertIsNone(
                        pattern.search(content),
                        f"Potential live credential material found in {relative_path}.",
                    )


if __name__ == "__main__":
    unittest.main()
