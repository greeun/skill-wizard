# Description Writing Guide

The description field is the **most critical element** of any skill. It's the only information Claude sees when deciding whether to activate a skill.

## Why Description Matters

```
User Request → Claude scans all skill descriptions → Matches? → Loads SKILL.md
                         ↑
              THIS IS THE ONLY GATE
```

- Claude reads ~100 descriptions to find the right skill
- A vague description = skill never triggers
- An overly specific description = skill triggers too rarely
- A well-crafted description = skill triggers at the right moments

## The Formula

```
[Primary Function] + [Key Capabilities] + [Trigger Scenarios/Keywords]
```

### Template

```
[What it does] with support for [2-3 key features].
Use when [scenario 1], [scenario 2], or when user mentions [trigger keywords].
```

### Character Limit

- Maximum: 1024 characters
- Recommended: 150-300 characters
- Too short = misses triggers
- Too long = dilutes signal

## Good vs Bad Examples

### Document Processor

**Bad** (too vague):
```
Helps with PDF files.
```

**Bad** (missing triggers):
```
Comprehensive PDF manipulation toolkit for extracting text, tables,
and form fields from PDF documents.
```

**Good**:
```
PDF text and table extraction, form filling, and document merging.
Use when working with PDF files, extracting data from documents,
filling forms, or when user mentions PDF, tables, or document extraction.
```

### Code Automator

**Bad**:
```
Runs tests.
```

**Good**:
```
Automated test execution with failure analysis and fix suggestions.
Use when running tests, debugging test failures, or when user mentions
pytest, jest, test suite, or CI pipeline issues.
```

### Data Analyzer

**Bad**:
```
Analyzes data from databases.
```

**Good**:
```
BigQuery data analysis with schema discovery, query generation, and
report creation. Use when querying BigQuery, analyzing metrics,
generating reports, or when user mentions SQL, data warehouse, or analytics.
```

### Workflow Orchestrator

**Bad**:
```
Deploys applications.
```

**Good**:
```
Multi-stage deployment pipeline with rollback support and health checks.
Use when deploying to staging/production, managing releases, or when
user mentions deploy, rollback, release, or CI/CD.
```

### Domain Expert

**Bad**:
```
Applies brand guidelines.
```

**Good**:
```
Brand consistency enforcement for documents and presentations with
color, typography, and logo guidelines. Use when reviewing brand
compliance, styling documents, or when user mentions branding,
style guide, or corporate identity.
```

## Trigger Keyword Categories

Include keywords from multiple categories:

### Action Keywords
- Verbs: extract, convert, analyze, generate, review, deploy, validate
- Commands: run, execute, create, build, process, transform

### Object Keywords
- File types: PDF, DOCX, Excel, JSON, CSV, image
- Domains: database, API, report, document, code, test

### Context Keywords
- Tools: pytest, BigQuery, Slack, GitHub, Docker
- Scenarios: debugging, reviewing, deploying, migrating

### Problem Keywords
- Issues: error, failure, bug, issue, broken
- Needs: help with, how to, need to, want to

## Writing Process

### Step 1: List Core Functions

What does your skill actually do? List 3-5 main capabilities:
```
1. Extract text from PDF
2. Extract tables from PDF
3. Fill PDF forms
4. Merge multiple PDFs
```

### Step 2: Identify Trigger Scenarios

When should Claude think of this skill?
```
- User has a PDF file
- User wants data from a document
- User mentions forms or tables
- User needs to combine documents
```

### Step 3: Extract Keywords

What words appear in user requests?
```
PDF, document, extract, table, form, merge, combine, text, data
```

### Step 4: Compose Description

Combine into formula:
```
PDF text and table extraction, form filling, and document merging.
Use when working with PDF files, extracting document data, filling
forms, merging documents, or when user mentions PDF, tables, or forms.
```

### Step 5: Test Coverage

Does your description trigger for these requests?
- "Extract the table from this PDF" → ✓ (PDF, table, extract)
- "I need to fill out this form" → ✓ (form, fill)
- "Combine these documents" → ✓ (merge/combine, documents)
- "Parse this spreadsheet" → ✗ (not PDF - correctly doesn't trigger)

## Common Mistakes

### 1. Missing "Use when" Section

```
# Wrong
PDF processing toolkit for documents.

# Right
PDF processing toolkit for documents.
Use when working with PDF files or extracting document data.
```

### 2. Too Technical

```
# Wrong
Implements RFC 3778 PDF/A-3 compliant document processing
with XMP metadata extraction using pypdf library.

# Right
PDF processing with text extraction and metadata reading.
Use when working with PDF files or extracting document information.
```

### 3. Listing Features Without Context

```
# Wrong
Supports: text extraction, OCR, form filling, digital signatures,
watermarking, page rotation, document merging, splitting...

# Right
PDF manipulation including text extraction, form filling, and merging.
Use when editing PDFs, filling forms, or combining documents.
```

### 4. Forgetting Synonyms

```
# Wrong (only one word for each concept)
PDF merging tool.

# Right (includes synonyms)
PDF merging and combining tool. Use when merging, combining,
or joining PDF documents together.
```

## Validation Checklist

Before finalizing your description:

- [ ] Under 1024 characters
- [ ] Includes primary function
- [ ] Has "Use when" section
- [ ] Contains 3+ trigger keywords
- [ ] Covers common synonyms
- [ ] Written in third person
- [ ] No angle brackets (< >)
- [ ] Tested against sample requests

## Pro Tips

### 1. Use Semantic Grouping

Group related triggers together:
```
Use when working with spreadsheets (Excel, XLSX, CSV, Google Sheets)...
```

### 2. Include Negative Signals (Sparingly)

If similar skills exist, differentiate:
```
PDF reading and extraction (not editing).
Use for extracting data, not modifying PDFs.
```

### 3. Mirror User Language

Users say "fix" not "remediate", "combine" not "concatenate":
```
# Match natural language
fix, combine, change, get data from
# Not technical jargon
remediate, concatenate, mutate, extract
```

### 4. Update Based on Usage

After real usage, note:
- Requests that should have triggered but didn't → Add keywords
- Requests that triggered incorrectly → Refine scope
