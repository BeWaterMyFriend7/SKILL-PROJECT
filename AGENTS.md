# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project overview

This is a collection of OpenCode agent skills — reusable prompt templates that extend AI coding agents with specialized capabilities. Each skill is defined by a `SKILL.md` file following the OpenCode skill format (YAML frontmatter with `name` and `description`, plus markdown instructions).

Skills are installed into OpenCode and invoked conversationally (e.g., "请使用 svg-generator skill 为我生成一个架构图").

## Repository structure

```
.opencode/
  skills/           # All agent skills (9 skills)
    svg-generator/       # Generate SVG diagrams (flowcharts, architecture, ER, sequence, etc.)
    xml-diagram/         # Generate drawio XML files (editable in draw.io)
    mermaid-gen/         # Generate Mermaid syntax for various diagram types
    requirements-analysis/   # Analyze requirements → output/doc/requirements-analysis.md
    requirements-review/     # Review requirements doc → output/doc/requirements-analysis-review.md
    technical-design/        # Technical design from requirements → output/doc/technical-design.md
    prototype-design-html/   # Interactive HTML prototypes → output/design-output/
    prototype-design-xml/    # Drawio XML prototypes → output/design-output/
  package.json        # @opencode-ai/plugin dependency
output/               # Example outputs from SE workflow skills
  doc/                # Requirements docs, technical design docs
  design-output/      # HTML prototypes and drawio prototypes
img-output/           # Rendered diagram images
image/                # Screenshots for README
```

## Skill categories

**Diagram skills** (generate visual output files):
- `svg-generator` and `xml-diagram` share a unified color/design system (same hex codes, same layout rules). `xml-diagram` output can be further edited in draw.io; `svg-generator` output renders directly in a browser.
- `mermaid-gen` outputs Mermaid code blocks for documentation.

**Software engineering workflow skills** (consume docs from `output/doc/`, produce more docs):
- `requirements-analysis` → `requirements-review` → `technical-design` → `prototype-design-html` or `prototype-design-xml`
- Each step reads the output of the previous step by default.

## Shared visual design system

svg-generator and xml-diagram use identical color palettes:

| Role | Color |
|------|-------|
| Primary (blue) | `#3498db` |
| Success (green) | `#2ecc71` |
| Warning (orange) | `#e67e22` |
| Error (red) | `#e74c3c` |
| Purple (async/queues) | `#9b59b6` |

Light mode: background `#f8f9fa`, cards `#ffffff`, borders `#e0e0e0`, text `#333333`/`#666666`
Dark mode: background `#1a1a2e`, cards `#16213e`, borders `#333333`, text `#ffffff`/`#aaaaaa`

**Critical rules** (enforced in both skills):
- Error branches MUST use red solid lines (never dashed)
- Dashed lines are ONLY for async/callback flows (purple `#9b59b6` or gray)
- Arrows must not cross; use orthogonal paths with L-shaped bends for branches
- Canvas utilization should be 60-80%; keep margins ≥30px on all sides

## Skill file format

Every skill must have YAML frontmatter:
```yaml
---
name: skill-name
description: What it does and when to trigger it.
---
```

The `description` field is used by OpenCode for skill routing — include trigger keywords the user might say.

## Adding or modifying skills

1. Each skill lives in its own directory under `.opencode/skills/<skill-name>/`
2. The main file is always `SKILL.md`
3. Examples go in an `examples/` subdirectory
4. Style guides and reference docs go in `assets/` or `reference/`
5. When editing a SKILL.md, keep the frontmatter `description` in sync with the actual capabilities
6. Diagram skills: when adding new diagram types, add at least one example SVG/drawio file in `examples/`
