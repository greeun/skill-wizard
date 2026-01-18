# Output Patterns

Patterns for skills that need consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match strictness to requirements.

### Strict Requirements (API responses, data formats)

```markdown
## Report structure

ALWAYS use this exact template:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

### Flexible Guidance (when adaptation is useful)

```markdown
## Report structure

Sensible default format, use your judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
```

## Why Examples Work

Examples help Claude understand:
- Desired style and tone
- Level of detail expected
- Format conventions
- Edge case handling

One good example is worth many paragraphs of description.

## Combining Patterns

For complex output needs, combine templates with examples:

```markdown
## Response Format

Use this structure:

### Summary
[1-2 sentences]

### Details
[Bullet points]

### Example Response

Summary: The API returns user data in JSON format with pagination.

Details:
- Endpoint: GET /users
- Auth: Bearer token required
- Rate limit: 100 req/min
```
