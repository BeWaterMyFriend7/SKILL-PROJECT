from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TYPES = {
    "architecture-application",
    "architecture-business",
    "architecture-data",
    "architecture-deployment",
    "architecture-technical",
    "comparison",
    "decision-matrix",
    "flow-branching",
    "flow-linear",
    "lifecycle",
    "relationship-dependency",
    "relationship-er",
    "relationship-knowledge",
    "roadmap",
    "sequence",
    "state",
    "summary",
    "swot",
    "timeline",
}


class CatalogContractTests(unittest.TestCase):
    def test_templates_and_examples_are_fresh_complete_catalogs(self):
        templates = sorted((ROOT / "templates").glob("*.svg"))
        examples = sorted((ROOT / "examples").glob("*.svg"))

        self.assertEqual(19, len(templates))
        self.assertEqual(19, len(examples))
        for files in (templates, examples):
            diagram_types = set()
            for path in files:
                root = ET.parse(path).getroot()
                self.assertEqual("enterprise-v2", root.get("data-visual-contract"), path.name)
                self.assertEqual("fresh-catalog-v1", root.get("data-generation"), path.name)
                diagram_types.add(root.get("data-diagram-type"))
            self.assertEqual(EXPECTED_TYPES, diagram_types)


if __name__ == "__main__":
    unittest.main()
