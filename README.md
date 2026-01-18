# Skill Wizard

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE.txt)

> Interactive wizard for creating Claude Code skills through guided questions.

[한국어 문서](README.ko.md)

## Overview

Skill Wizard is a Claude Code skill that guides users through creating effective skills via a 6-phase interactive workflow. Instead of reading documentation and figuring out the structure yourself, the wizard asks targeted questions and generates optimized skill scaffolding.

## Features

- **6-Phase Guided Workflow**: Step-by-step process from purpose discovery to skill generation
- **Description Optimization**: Comprehensive guide for writing effective trigger descriptions
- **Type-Specific Templates**: Ready-to-use templates for 5 skill types
- **Test Scenario Generation**: Automated creation of validation test cases
- **CLI Wizard**: Interactive command-line tool for skill creation

## Installation

### As a Claude Code Skill

```bash
# Clone to your Claude Code skills directory
git clone https://github.com/greeun/skill-wizard.git ~/.claude/skills/skill-wizard
```

### Verify Installation

The skill will automatically activate when you mention creating a new skill in Claude Code.

## Usage

### Automatic Activation

Simply ask Claude to help create a skill:

```
"I want to create a new skill for PDF processing"
"Help me build a skill that automates code reviews"
"Create a skill for tracking work in Linear"
```

The wizard will guide you through:

1. **Purpose Discovery** - Understanding what problem you're solving
2. **Type Selection** - Choosing from 5 skill archetypes
3. **Metadata Design** - Crafting optimal name and description
4. **Content Architecture** - Designing the skill structure
5. **Resource Planning** - Identifying scripts, references, and assets
6. **Validation & Generation** - Creating and testing the skill

### CLI Wizard

For direct command-line usage:

```bash
python ~/.claude/skills/skill-wizard/scripts/wizard.py
```

Options:
```bash
python wizard.py --output-dir ~/.claude/skills
```

### Test Scenario Generator

Generate test scenarios for any skill:

```bash
# From skill path
python scripts/generate_tests.py --skill-path /path/to/skill

# From description
python scripts/generate_tests.py \
  --description "PDF table extraction tool" \
  --type document-processor \
  --output tests.md
```

## Skill Types

| Type | Best For | Example |
|------|----------|---------|
| **Document Processor** | File format manipulation | PDF, DOCX, image processing |
| **Code Automator** | Development workflows | Testing, reviewing, refactoring |
| **Data Analyzer** | Data operations | Queries, reports, transformations |
| **Workflow Orchestrator** | Multi-step processes | Deployments, migrations |
| **Domain Expert** | Specialized knowledge | Guidelines, standards, policies |

## Project Structure

```
skill-wizard/
├── SKILL.md                          # Main wizard guide (with skill-creator content)
├── LICENSE.txt                       # Apache 2.0 license
├── references/
│   ├── description-guide.md          # How to write effective descriptions
│   ├── type-templates.md             # Templates for each skill type
│   ├── test-scenarios.md             # Test scenario writing guide
│   ├── workflows.md                  # Sequential/conditional workflow patterns
│   └── output-patterns.md            # Template/example output patterns
└── scripts/
    ├── wizard.py                     # Interactive CLI wizard
    └── generate_tests.py             # Test scenario generator
```

## Reference Documentation

### Description Guide

The `references/description-guide.md` provides:
- The description formula: `[Function] + [Trigger Keywords]`
- Good vs bad examples for each skill type
- Keyword categories (actions, objects, contexts)
- Validation checklist

### Type Templates

The `references/type-templates.md` includes complete SKILL.md templates for:
- Document Processor (PDF example)
- Code Automator (Test runner example)
- Data Analyzer (Sales analytics example)
- Workflow Orchestrator (Deployment example)
- Domain Expert (Brand guidelines example)

## Integration with skill-creator

Skill Wizard complements the existing `skill-creator` skill:

| Feature | skill-creator | skill-wizard |
|---------|---------------|--------------|
| Approach | Documentation-based | Question-driven |
| Description Help | Basic mention | Comprehensive guide |
| Templates | Generic template | 5 type-specific templates |
| Test Generation | None | Automated tool |
| Target Users | Experienced | Beginners to experts |

Use together:
1. **skill-wizard** → Plan and design the skill
2. **skill-creator** → Initialize (`init_skill.py`) and package (`package_skill.py`)

## Requirements

- Claude Code CLI
- Python 3.8+ (for scripts)
- **skill-creator** (for `init_skill.py` and `package_skill.py`)

### Installing skill-creator (Required Dependency)

skill-wizard uses `init_skill.py` and `package_skill.py` from skill-creator. Install it first:

```bash
# Clone skill-creator to your Claude Code skills directory
git clone https://github.com/anthropics/skill-creator.git ~/.claude/skills/skill-creator
```

Verify installation:
```bash
ls ~/.claude/skills/skill-creator/scripts/
# Should show: init_skill.py  package_skill.py
```

> **Note**: Without skill-creator, you can still use skill-wizard for planning and design, but you'll need to manually create the skill directory structure.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache License 2.0 - see [LICENSE.txt](LICENSE.txt) for details.

## Related

- [skill-creator](https://github.com/anthropics/skills) - Official skill creation toolkit
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
