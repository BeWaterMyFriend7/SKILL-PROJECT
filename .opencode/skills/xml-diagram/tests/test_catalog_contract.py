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
        templates = sorted((ROOT / "templates").glob("*.drawio"))
        examples = sorted((ROOT / "examples").glob("*.drawio"))

        self.assertEqual(19, len(templates))
        self.assertEqual(19, len(examples))
        for files in (templates, examples):
            diagram_types = set()
            for path in files:
                diagram = ET.parse(path).getroot().find("diagram")
                self.assertIsNotNone(diagram, path.name)
                self.assertEqual("enterprise-v2", diagram.get("visualContract"), path.name)
                self.assertEqual("fresh-catalog-v1", diagram.get("generation"), path.name)
                diagram_types.add(diagram.get("diagramType"))
            self.assertEqual(EXPECTED_TYPES, diagram_types)


if __name__ == "__main__":
    unittest.main()
