#!/usr/bin/env python3
"""
Test Scenario Generator - Creates test scenarios for Claude Code skills

Usage:
    python generate_tests.py --description "skill description" [--type TYPE] [--output FILE]
    python generate_tests.py --skill-path /path/to/skill

Examples:
    python generate_tests.py --description "PDF table extraction" --type document-processor
    python generate_tests.py --skill-path ~/.claude/skills/my-skill
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
import yaml

# Common synonyms for trigger word expansion
SYNONYMS = {
    # Actions
    'extract': ['get', 'pull', 'retrieve', 'export', 'obtain'],
    'create': ['make', 'generate', 'build', 'produce', 'write'],
    'convert': ['transform', 'change', 'translate', 'turn into'],
    'analyze': ['examine', 'review', 'check', 'inspect', 'look at'],
    'fix': ['repair', 'correct', 'resolve', 'solve', 'debug'],
    'deploy': ['release', 'push', 'publish', 'ship', 'launch'],
    'merge': ['combine', 'join', 'concatenate', 'unite'],

    # Objects
    'pdf': ['document', 'file', 'doc'],
    'table': ['spreadsheet', 'grid', 'data'],
    'code': ['program', 'script', 'source'],
    'test': ['spec', 'unit test', 'check'],
    'report': ['summary', 'analysis', 'overview'],
    'data': ['information', 'records', 'content'],
}

# Out of scope patterns by skill type
OUT_OF_SCOPE = {
    'document-processor': [
        ('Edit/modify instead of extract', 'Edit the text in this PDF'),
        ('Different file format', 'Work with this Excel file'),
        ('Create instead of process', 'Create a new PDF from scratch'),
    ],
    'code-automator': [
        ('Manual process', 'Walk me through how to test this'),
        ('Documentation', 'Write documentation for this code'),
        ('Different language', 'Convert this to a different language'),
    ],
    'data-analyzer': [
        ('Data entry', 'Add this new record to the database'),
        ('Data modification', 'Update these values in the table'),
        ('Different data source', 'Analyze this from a different source'),
    ],
    'workflow-orchestrator': [
        ('Single step', 'Just run this one command'),
        ('Planning only', 'Help me plan this deployment'),
        ('Rollback only', 'Undo the last deployment'),
    ],
    'domain-expert': [
        ('Create guidelines', 'Help me write new guidelines'),
        ('Compare standards', 'Compare our standards to industry'),
        ('Training', 'Teach me about these guidelines'),
    ],
}

def extract_keywords(description: str) -> List[str]:
    """Extract meaningful keywords from description."""
    # Remove common stop words
    stop_words = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
        'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'under', 'again', 'further', 'then', 'once',
        'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few',
        'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
        'own', 'same', 'so', 'than', 'too', 'very', 'just', 'and', 'but', 'if',
        'or', 'because', 'as', 'until', 'while', 'this', 'that', 'these', 'those',
        'use', 'user', 'using', 'mentions', 'working', 'support'
    }

    # Extract words
    words = re.findall(r'\b[a-z]+\b', description.lower())

    # Filter and deduplicate
    keywords = []
    seen = set()
    for word in words:
        if word not in stop_words and len(word) > 2 and word not in seen:
            keywords.append(word)
            seen.add(word)

    return keywords[:10]  # Top 10 keywords

def get_synonyms(keyword: str) -> List[str]:
    """Get synonyms for a keyword."""
    return SYNONYMS.get(keyword, [])

def generate_happy_path(keywords: List[str], skill_type: str) -> List[Dict]:
    """Generate happy path test scenarios."""
    scenarios = []

    # Direct keyword usage
    if len(keywords) >= 2:
        scenarios.append({
            'name': 'Direct Request with Keywords',
            'request': f"Please {keywords[0]} the {keywords[1]} from this file",
            'expected': 'Skill triggers and completes the primary task',
            'keywords_matched': keywords[:2],
        })

    # Full feature request
    if len(keywords) >= 3:
        scenarios.append({
            'name': 'Multi-keyword Request',
            'request': f"I need to {keywords[0]} and {keywords[2]} the {keywords[1]}",
            'expected': 'Skill triggers and handles compound request',
            'keywords_matched': keywords[:3],
        })

    # Simple command
    scenarios.append({
        'name': 'Simple Command',
        'request': f"{keywords[0].capitalize()} this",
        'expected': 'Skill triggers with minimal context',
        'keywords_matched': [keywords[0]] if keywords else [],
    })

    return scenarios

def generate_edge_cases(keywords: List[str], skill_type: str) -> List[Dict]:
    """Generate edge case test scenarios."""
    scenarios = []

    # Synonym usage
    if keywords:
        synonyms = get_synonyms(keywords[0])
        if synonyms:
            scenarios.append({
                'name': 'Synonym Usage',
                'request': f"Can you {synonyms[0]} the {keywords[1] if len(keywords) > 1 else 'content'}?",
                'expected': 'Skill triggers despite using synonym',
                'challenge': f'Uses "{synonyms[0]}" instead of "{keywords[0]}"',
            })

    # Indirect phrasing
    scenarios.append({
        'name': 'Indirect Phrasing',
        'request': f"I'm having trouble with this, can you help?",
        'expected': 'Skill may trigger with clarifying question',
        'challenge': 'No explicit keywords, relies on context',
    })

    # Partial information
    if len(keywords) >= 2:
        scenarios.append({
            'name': 'Partial Context',
            'request': f"Just do the {keywords[1]} thing",
            'expected': 'Skill triggers and asks for clarification',
            'challenge': 'Incomplete request, missing details',
        })

    # Typo tolerance
    if keywords:
        typo_word = keywords[0][:-1] + 'e' if keywords[0][-1] != 'e' else keywords[0][:-1]
        scenarios.append({
            'name': 'Minor Typo',
            'request': f"Please {typo_word} this document",
            'expected': 'Skill triggers despite typo',
            'challenge': f'Typo in keyword: "{typo_word}" vs "{keywords[0]}"',
        })

    return scenarios

def generate_out_of_scope(keywords: List[str], skill_type: str) -> List[Dict]:
    """Generate out of scope test scenarios."""
    scenarios = []

    # Get type-specific out of scope examples
    type_examples = OUT_OF_SCOPE.get(skill_type, OUT_OF_SCOPE['document-processor'])

    for reason, request in type_examples:
        scenarios.append({
            'name': reason,
            'request': request,
            'expected': 'Skill does NOT trigger',
            'reason': reason,
        })

    # Add a similar-sounding but wrong request
    if keywords:
        scenarios.append({
            'name': 'Similar Keywords, Wrong Intent',
            'request': f"Tell me about {keywords[0]} best practices",
            'expected': 'Skill does NOT trigger',
            'reason': 'Asking for information, not performing action',
        })

    return scenarios

def read_skill_description(skill_path: Path) -> Tuple[str, str]:
    """Read description from SKILL.md."""
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text()

    # Parse frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found")

    frontmatter = yaml.safe_load(match.group(1))

    name = frontmatter.get('name', skill_path.name)
    description = frontmatter.get('description', '')

    return name, description

def format_scenarios(name: str, happy_path: List[Dict],
                     edge_cases: List[Dict], out_of_scope: List[Dict]) -> str:
    """Format scenarios as markdown."""
    output = f"""# Test Scenarios for {name}

Generated test scenarios to validate skill triggering behavior.

---

## Happy Path Tests

These requests should trigger the skill and complete successfully.

"""

    for i, scenario in enumerate(happy_path, 1):
        output += f"""### Test {i}: {scenario['name']}

- **Request**: "{scenario['request']}"
- **Expected**: {scenario['expected']}
- **Keywords matched**: {', '.join(scenario.get('keywords_matched', []))}

"""

    output += """---

## Edge Case Tests

These requests should trigger the skill but may require extra handling.

"""

    for i, scenario in enumerate(edge_cases, 1):
        output += f"""### Test {i}: {scenario['name']}

- **Request**: "{scenario['request']}"
- **Expected**: {scenario['expected']}
- **Challenge**: {scenario.get('challenge', 'N/A')}

"""

    output += """---

## Out of Scope Tests

These requests should NOT trigger the skill.

"""

    for i, scenario in enumerate(out_of_scope, 1):
        output += f"""### Test {i}: {scenario['name']}

- **Request**: "{scenario['request']}"
- **Expected**: {scenario['expected']}
- **Reason**: {scenario.get('reason', 'Outside skill capabilities')}

"""

    output += """---

## Running These Tests

1. Start a new Claude conversation
2. Enter each request exactly as shown
3. Verify skill triggers (or doesn't) as expected
4. Note any failures for description refinement

### If Tests Fail

| Issue | Fix |
|-------|-----|
| Happy path doesn't trigger | Add missing keywords to description |
| Edge case doesn't trigger | Add synonyms to description |
| Out of scope triggers | Narrow description scope |

"""

    return output

def main():
    parser = argparse.ArgumentParser(
        description='Generate test scenarios for Claude Code skills'
    )
    parser.add_argument(
        '--description', '-d',
        help='Skill description to generate tests for'
    )
    parser.add_argument(
        '--type', '-t',
        choices=['document-processor', 'code-automator', 'data-analyzer',
                 'workflow-orchestrator', 'domain-expert'],
        default='document-processor',
        help='Skill type for specialized scenarios'
    )
    parser.add_argument(
        '--skill-path', '-s',
        type=Path,
        help='Path to skill directory (reads SKILL.md)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '--name', '-n',
        default='skill',
        help='Skill name for output header'
    )

    args = parser.parse_args()

    # Get description
    if args.skill_path:
        try:
            name, description = read_skill_description(args.skill_path)
            skill_type = args.type
        except Exception as e:
            print(f"Error reading skill: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.description:
        name = args.name
        description = args.description
        skill_type = args.type
    else:
        print("Error: Provide --description or --skill-path", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Extract keywords
    keywords = extract_keywords(description)

    if not keywords:
        print("Warning: No keywords extracted from description", file=sys.stderr)
        keywords = ['process', 'handle']

    # Generate scenarios
    happy_path = generate_happy_path(keywords, skill_type)
    edge_cases = generate_edge_cases(keywords, skill_type)
    out_of_scope = generate_out_of_scope(keywords, skill_type)

    # Format output
    output = format_scenarios(name, happy_path, edge_cases, out_of_scope)

    # Write output
    if args.output:
        args.output.write_text(output)
        print(f"Test scenarios written to: {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
