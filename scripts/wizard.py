#!/usr/bin/env python3
"""
Skill Creation Wizard - Interactive CLI for creating Claude Code skills

Usage:
    python wizard.py [--output-dir PATH]

Examples:
    python wizard.py
    python wizard.py --output-dir ~/.claude/skills
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}\n")

def print_phase(phase_num: int, phase_name: str):
    print(f"\n{Colors.CYAN}{Colors.BOLD}Phase {phase_num}: {phase_name}{Colors.END}")
    print(f"{Colors.DIM}{'─' * 50}{Colors.END}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text: str):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def ask(question: str, default: str = "") -> str:
    """Ask a question and return the answer."""
    if default:
        prompt = f"{Colors.BOLD}{question}{Colors.END} [{default}]: "
    else:
        prompt = f"{Colors.BOLD}{question}{Colors.END}: "

    answer = input(prompt).strip()
    return answer if answer else default

def ask_choice(question: str, choices: List[str]) -> int:
    """Ask user to choose from a list of options."""
    print(f"\n{Colors.BOLD}{question}{Colors.END}")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")

    while True:
        try:
            choice = int(input(f"\nEnter choice (1-{len(choices)}): "))
            if 1 <= choice <= len(choices):
                return choice - 1
            print_error(f"Please enter a number between 1 and {len(choices)}")
        except ValueError:
            print_error("Please enter a valid number")

def ask_yes_no(question: str, default: bool = True) -> bool:
    """Ask a yes/no question."""
    default_str = "Y/n" if default else "y/N"
    answer = input(f"{Colors.BOLD}{question}{Colors.END} [{default_str}]: ").strip().lower()

    if not answer:
        return default
    return answer in ('y', 'yes', 'true', '1')

def validate_skill_name(name: str) -> Tuple[bool, str]:
    """Validate skill name follows conventions."""
    if not name:
        return False, "Name cannot be empty"
    if len(name) > 64:
        return False, f"Name too long ({len(name)}/64 chars)"
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Use only lowercase letters, digits, and hyphens"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, "Cannot start/end with hyphen or have consecutive hyphens"
    return True, "Valid"

def validate_description(desc: str) -> Tuple[bool, str]:
    """Validate description meets requirements."""
    if not desc:
        return False, "Description cannot be empty"
    if len(desc) > 1024:
        return False, f"Description too long ({len(desc)}/1024 chars)"
    if '<' in desc or '>' in desc:
        return False, "Description cannot contain angle brackets"
    if 'use when' not in desc.lower():
        return False, "Description should include 'Use when' section"
    return True, "Valid"

def generate_name_suggestions(purpose: str, skill_type: str) -> List[str]:
    """Generate skill name suggestions based on purpose and type."""
    # Extract key words from purpose
    words = purpose.lower().split()

    # Common action verbs
    actions = ['extract', 'convert', 'analyze', 'generate', 'process',
               'validate', 'deploy', 'review', 'format', 'create']

    # Find action word if present
    action = None
    for word in words:
        if word in actions:
            action = word
            break

    if not action:
        action = {
            'document-processor': 'process',
            'code-automator': 'automate',
            'data-analyzer': 'analyze',
            'workflow-orchestrator': 'orchestrate',
            'domain-expert': 'guide'
        }.get(skill_type, 'handle')

    # Find object/noun
    nouns = ['pdf', 'excel', 'docx', 'image', 'code', 'test', 'data',
             'report', 'deploy', 'brand', 'sales', 'api']
    obj = None
    for word in words:
        if word in nouns:
            obj = word
            break

    if not obj:
        obj = 'content'

    suggestions = [
        f"{obj}-{action}r",
        f"{action}-{obj}",
        f"{obj}-{skill_type.split('-')[0]}"
    ]

    return [s for s in suggestions if validate_skill_name(s)[0]][:3]

def generate_description_template(skill_type: str, purpose: str, examples: List[str]) -> str:
    """Generate a description template based on skill type and purpose."""
    # Extract keywords from purpose and examples
    all_text = purpose + " " + " ".join(examples)
    words = set(all_text.lower().split())

    templates = {
        'document-processor': (
            "{purpose} with support for {features}. "
            "Use when working with {format} files, {action}, "
            "or when user mentions {keywords}."
        ),
        'code-automator': (
            "Automated {purpose} with {features}. "
            "Use when {scenario}, debugging, "
            "or when user mentions {keywords}."
        ),
        'data-analyzer': (
            "{purpose} with {features}. "
            "Use when querying data, generating reports, "
            "or when user mentions {keywords}."
        ),
        'workflow-orchestrator': (
            "Multi-stage {purpose} with {features}. "
            "Use when {scenario}, managing processes, "
            "or when user mentions {keywords}."
        ),
        'domain-expert': (
            "{purpose} guidelines with {features}. "
            "Use when reviewing compliance, applying standards, "
            "or when user mentions {keywords}."
        )
    }

    template = templates.get(skill_type, templates['document-processor'])

    return template.format(
        purpose=purpose[:50],
        features="[key features]",
        format="[file format]",
        action="[primary action]",
        scenario="[trigger scenario]",
        keywords="[trigger keywords]"
    )

def create_skill_structure(skill_data: Dict, output_dir: Path) -> Path:
    """Create the skill directory and files."""
    skill_dir = output_dir / skill_data['name']

    if skill_dir.exists():
        if not ask_yes_no(f"Directory {skill_dir} exists. Overwrite?", False):
            print_error("Aborted")
            sys.exit(1)

    # Create directories
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / 'references').mkdir(exist_ok=True)
    (skill_dir / 'scripts').mkdir(exist_ok=True)

    if skill_data.get('needs_assets'):
        (skill_dir / 'assets').mkdir(exist_ok=True)

    # Create SKILL.md
    skill_md_content = generate_skill_md(skill_data)
    (skill_dir / 'SKILL.md').write_text(skill_md_content)

    # Create placeholder reference file
    if skill_data.get('needs_references'):
        ref_content = f"# Reference Documentation\n\n[Add detailed documentation here]"
        (skill_dir / 'references' / 'documentation.md').write_text(ref_content)

    # Create placeholder script
    if skill_data.get('needs_scripts'):
        script_content = f'''#!/usr/bin/env python3
"""
{skill_data['name']} helper script
"""

def main():
    print("TODO: Implement {skill_data['name']} logic")

if __name__ == "__main__":
    main()
'''
        script_path = skill_dir / 'scripts' / 'main.py'
        script_path.write_text(script_content)
        script_path.chmod(0o755)

    return skill_dir

def generate_skill_md(skill_data: Dict) -> str:
    """Generate SKILL.md content from collected data."""

    # Build frontmatter
    frontmatter = f"""---
name: {skill_data['name']}
description: {skill_data['description']}
---"""

    # Build body based on skill type
    type_structures = {
        'document-processor': """
# {title}

## Quick Start

[Add quick start example here]

```python
# Example code
```

## Supported Operations

### Operation 1

[Description + code example]

### Operation 2

[Description + code example]

## Requirements

```bash
pip install [required-packages]
```
""",
        'code-automator': """
# {title}

## Workflow

```
Step 1 → Step 2 → Step 3 → Output
```

## Decision Tree

1. **Scenario A?** → Follow Section A
2. **Scenario B?** → Follow Section B

## Section A

### Step 1

```bash
# command
```

### Step 2

[Instructions]

## Section B

[Similar structure]

## Common Issues

| Issue | Solution |
|-------|----------|
| Problem 1 | Fix 1 |
""",
        'data-analyzer': """
# {title}

## Overview

[What this skill analyzes and produces]

## Data Sources

### Primary Source

**Connection:**
```python
# connection example
```

**Available data:**
- `item_1`: description
- `item_2`: description

## Common Queries

### Query Type 1

```sql
SELECT ...
```

## Report Templates

### Report 1

[Format and sections]
""",
        'workflow-orchestrator': """
# {title}

## Prerequisites

- [ ] Requirement 1
- [ ] Requirement 2

## Process Overview

```
Phase 1: Name
    ↓
Phase 2: Name
    ↓
Phase 3: Name
```

## Phase 1: [Name]

**Goal:** [What this phase accomplishes]

### Steps

1. Step 1
   ```bash
   command
   ```

2. Step 2

### Validation

```bash
validation command
```

## Rollback Procedures

[If something fails...]
""",
        'domain-expert': """
# {title}

## Core Principles

1. **Principle 1**: Description
2. **Principle 2**: Description
3. **Principle 3**: Description

## Standards

### Category 1

| Element | Specification |
|---------|--------------|
| Item 1 | Spec |
| Item 2 | Spec |

## Application Guidelines

### When Scenario 1

[Instructions and examples]

## Review Checklist

- [ ] Check 1
- [ ] Check 2
- [ ] Check 3
"""
    }

    body_template = type_structures.get(
        skill_data['type'],
        type_structures['document-processor']
    )

    title = ' '.join(word.capitalize() for word in skill_data['name'].split('-'))
    body = body_template.format(title=title)

    # Add resources section if needed
    resources = []
    if skill_data.get('needs_scripts'):
        resources.append("- Scripts: [scripts/](scripts/)")
    if skill_data.get('needs_references'):
        resources.append("- Documentation: [references/](references/)")
    if skill_data.get('needs_assets'):
        resources.append("- Assets: [assets/](assets/)")

    if resources:
        body += "\n\n## Resources\n\n" + "\n".join(resources)

    return frontmatter + body

def generate_test_scenarios(skill_data: Dict) -> str:
    """Generate test scenarios based on skill data."""
    name = skill_data['name']
    desc = skill_data['description']

    # Extract keywords from description
    keywords = []
    for word in desc.split():
        word = word.strip('.,()').lower()
        if len(word) > 3 and word not in ['with', 'when', 'from', 'that', 'this', 'user']:
            keywords.append(word)

    keywords = list(set(keywords))[:5]

    return f"""
## Test Scenarios for {name}

### Happy Path Tests

**Test 1: Direct Request**
- Request: "Please {skill_data.get('purpose', 'help with this task')[:50]}"
- Expected: Skill triggers and completes task
- Keywords matched: {', '.join(keywords[:2])}

**Test 2: Keyword Match**
- Request: "[Request using {keywords[0] if keywords else 'keyword'}]"
- Expected: Skill triggers
- Keywords matched: {keywords[0] if keywords else 'keyword'}

### Edge Case Tests

**Test 1: Synonym Usage**
- Request: "[Request using synonym instead of exact keyword]"
- Expected: Skill triggers
- Challenge: Tests semantic understanding

**Test 2: Partial Context**
- Request: "[Vague request that should still trigger]"
- Expected: Skill triggers with clarifying questions
- Challenge: Incomplete information

### Out of Scope Tests

**Test 1: Similar but Different**
- Request: "[Request that sounds related but isn't]"
- Expected: Skill does NOT trigger
- Reason: Outside skill's capabilities

**Test 2: Wrong Domain**
- Request: "[Request from different domain]"
- Expected: Skill does NOT trigger
- Reason: Different skill should handle this
"""

def main():
    print_header("Skill Creation Wizard")
    print("This wizard will guide you through creating a new Claude Code skill.\n")

    # Parse arguments
    output_dir = Path.home() / '.claude' / 'skills'
    for i, arg in enumerate(sys.argv):
        if arg == '--output-dir' and i + 1 < len(sys.argv):
            output_dir = Path(sys.argv[i + 1])

    skill_data = {}

    # Phase 1: Purpose Discovery
    print_phase(1, "Purpose Discovery")

    skill_data['purpose'] = ask(
        "What repetitive task do you want to automate with this skill?"
    )

    frequency = ask("How many times have you done this task manually?", "5")
    try:
        freq_num = int(frequency)
        if freq_num < 5:
            print_warning(
                "Skills work best for tasks you've done 5+ times. "
                "Consider waiting until you have more experience with this task."
            )
            if not ask_yes_no("Continue anyway?"):
                print_info("Come back when you have more experience with this task!")
                sys.exit(0)
    except ValueError:
        pass

    examples = []
    print("\nGive 2-3 concrete examples of how you'd use this skill:")
    for i in range(3):
        example = ask(f"  Example {i+1}")
        if example:
            examples.append(example)
        if i >= 1 and not example:
            break
    skill_data['examples'] = examples

    skill_data['success_criteria'] = ask(
        "What does a successful outcome look like?"
    )

    print_success("Purpose captured!")

    # Phase 2: Type Selection
    print_phase(2, "Type Selection")

    skill_types = [
        "Document Processor - File format manipulation (PDF, DOCX, images)",
        "Code Automator - Development workflows (test, review, refactor)",
        "Data Analyzer - Queries, reports, data transformation",
        "Workflow Orchestrator - Multi-step processes with dependencies",
        "Domain Expert - Specialized knowledge, guidelines, standards"
    ]

    type_choice = ask_choice("Which type best matches your skill's purpose?", skill_types)
    type_keys = ['document-processor', 'code-automator', 'data-analyzer',
                 'workflow-orchestrator', 'domain-expert']
    skill_data['type'] = type_keys[type_choice]

    print_success(f"Selected type: {skill_types[type_choice].split(' - ')[0]}")

    # Phase 3: Metadata Design
    print_phase(3, "Metadata Design")

    # Name
    print("\n" + Colors.BOLD + "Skill Name" + Colors.END)
    suggestions = generate_name_suggestions(skill_data['purpose'], skill_data['type'])
    if suggestions:
        print(f"Suggestions: {', '.join(suggestions)}")

    while True:
        name = ask("Enter skill name (lowercase, hyphens)")
        valid, msg = validate_skill_name(name)
        if valid:
            skill_data['name'] = name
            print_success(f"Name: {name}")
            break
        print_error(msg)

    # Description
    print("\n" + Colors.BOLD + "Skill Description" + Colors.END)
    print_info("Formula: [What it does] + [When to use - trigger keywords]")

    template = generate_description_template(
        skill_data['type'],
        skill_data['purpose'],
        skill_data['examples']
    )
    print(f"\nTemplate: {Colors.DIM}{template}{Colors.END}")

    while True:
        desc = ask("\nEnter description")
        valid, msg = validate_description(desc)
        if valid:
            skill_data['description'] = desc
            print_success("Description validated!")
            break
        print_error(msg)

    # Phase 4: Content Architecture
    print_phase(4, "Content Architecture")

    freedom_levels = [
        "High (guidelines) - Multiple valid approaches, context-dependent",
        "Medium (patterns) - Preferred method with flexibility",
        "Low (scripts) - Exact sequence required, consistency critical"
    ]
    freedom_choice = ask_choice(
        "How strict should the skill's instructions be?",
        freedom_levels
    )
    skill_data['freedom_level'] = ['high', 'medium', 'low'][freedom_choice]

    print_success(f"Freedom level: {freedom_levels[freedom_choice].split(' - ')[0]}")

    # Phase 5: Resource Planning
    print_phase(5, "Resource Planning")

    skill_data['needs_scripts'] = ask_yes_no(
        "Does this skill need executable scripts (Python/Bash)?",
        skill_data['freedom_level'] == 'low'
    )

    skill_data['needs_references'] = ask_yes_no(
        "Does this skill need reference documentation?",
        True
    )

    skill_data['needs_assets'] = ask_yes_no(
        "Does this skill need asset files (templates, images)?",
        skill_data['type'] == 'domain-expert'
    )

    print_success("Resources planned!")

    # Phase 6: Validation & Generation
    print_phase(6, "Validation & Generation")

    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  Name: {skill_data['name']}")
    print(f"  Type: {skill_data['type']}")
    print(f"  Description: {skill_data['description'][:80]}...")
    print(f"  Freedom: {skill_data['freedom_level']}")
    print(f"  Scripts: {'Yes' if skill_data['needs_scripts'] else 'No'}")
    print(f"  References: {'Yes' if skill_data['needs_references'] else 'No'}")
    print(f"  Assets: {'Yes' if skill_data['needs_assets'] else 'No'}")
    print(f"  Output: {output_dir}")

    if not ask_yes_no("\nCreate this skill?"):
        print_info("Aborted")
        sys.exit(0)

    # Create skill
    try:
        skill_dir = create_skill_structure(skill_data, output_dir)
        print_success(f"Created skill at: {skill_dir}")

        # Generate test scenarios
        tests = generate_test_scenarios(skill_data)
        tests_file = skill_dir / 'TEST_SCENARIOS.md'
        tests_file.write_text(tests)
        print_success(f"Generated test scenarios: {tests_file}")

        print(f"\n{Colors.GREEN}{Colors.BOLD}Skill created successfully!{Colors.END}")
        print(f"\nNext steps:")
        print(f"  1. Edit {skill_dir}/SKILL.md to complete the template")
        if skill_data['needs_scripts']:
            print(f"  2. Implement scripts in {skill_dir}/scripts/")
        if skill_data['needs_references']:
            print(f"  3. Add documentation to {skill_dir}/references/")
        print(f"  4. Test with scenarios in {tests_file}")
        print(f"  5. Package when ready:")
        print(f"     python ~/.claude/skills/skill-creator/scripts/package_skill.py {skill_dir}")

    except Exception as e:
        print_error(f"Failed to create skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
