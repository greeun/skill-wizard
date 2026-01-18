# Skill Wizard

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 대화형 질문을 통해 Claude Code 스킬을 생성하는 위저드

[English Documentation](README.md)

## 개요

Skill Wizard는 6단계 대화형 워크플로우를 통해 효과적인 스킬 생성을 안내하는 Claude Code 스킬입니다. 문서를 읽고 구조를 직접 파악하는 대신, 위저드가 핵심 질문을 하고 최적화된 스킬 구조를 생성합니다.

## 주요 기능

- **6단계 가이드 워크플로우**: 목적 파악부터 스킬 생성까지 단계별 프로세스
- **Description 최적화**: 효과적인 트리거 설명 작성을 위한 종합 가이드
- **유형별 템플릿**: 5가지 스킬 유형에 맞는 즉시 사용 가능한 템플릿
- **테스트 시나리오 생성**: 검증 테스트 케이스 자동 생성
- **CLI 위저드**: 스킬 생성을 위한 대화형 커맨드라인 도구

## 설치

### Claude Code 스킬로 설치

```bash
# Claude Code 스킬 디렉토리에 클론
git clone https://github.com/greeun/skill-wizard.git ~/.claude/skills/skill-wizard
```

### 설치 확인

Claude Code에서 스킬 생성을 언급하면 자동으로 활성화됩니다.

## 사용법

### 자동 활성화

Claude에게 스킬 생성을 요청하세요:

```
"PDF 처리를 위한 새 스킬을 만들고 싶어"
"코드 리뷰를 자동화하는 스킬을 만들어줘"
"Linear에서 작업을 추적하는 스킬을 생성해줘"
```

위저드가 다음 단계를 안내합니다:

1. **목적 파악** - 해결하려는 문제 이해
2. **유형 선택** - 5가지 스킬 유형 중 선택
3. **메타데이터 설계** - 최적의 이름과 설명 작성
4. **콘텐츠 구조** - 스킬 구조 설계
5. **리소스 계획** - 스크립트, 참조문서, 에셋 식별
6. **검증 및 생성** - 스킬 생성 및 테스트

### CLI 위저드

커맨드라인에서 직접 사용:

```bash
python ~/.claude/skills/skill-wizard/scripts/wizard.py
```

옵션:
```bash
python wizard.py --output-dir ~/.claude/skills
```

### 테스트 시나리오 생성기

모든 스킬에 대한 테스트 시나리오 생성:

```bash
# 스킬 경로에서
python scripts/generate_tests.py --skill-path /path/to/skill

# 설명에서
python scripts/generate_tests.py \
  --description "PDF 테이블 추출 도구" \
  --type document-processor \
  --output tests.md
```

## 스킬 유형

| 유형 | 용도 | 예시 |
|------|------|------|
| **Document Processor** | 파일 형식 처리 | PDF, DOCX, 이미지 처리 |
| **Code Automator** | 개발 워크플로우 | 테스트, 리뷰, 리팩토링 |
| **Data Analyzer** | 데이터 작업 | 쿼리, 보고서, 변환 |
| **Workflow Orchestrator** | 다단계 프로세스 | 배포, 마이그레이션 |
| **Domain Expert** | 전문 지식 | 가이드라인, 표준, 정책 |

## 프로젝트 구조

```
skill-wizard/
├── SKILL.md                          # 메인 위저드 가이드
├── references/
│   ├── description-guide.md          # 효과적인 설명 작성법
│   ├── type-templates.md             # 유형별 템플릿
│   └── test-scenarios.md             # 테스트 시나리오 작성 가이드
└── scripts/
    ├── wizard.py                     # 대화형 CLI 위저드
    └── generate_tests.py             # 테스트 시나리오 생성기
```

## 참조 문서

### Description 가이드

`references/description-guide.md` 제공 내용:
- Description 공식: `[기능] + [트리거 키워드]`
- 유형별 좋은/나쁜 예시
- 키워드 카테고리 (액션, 객체, 컨텍스트)
- 검증 체크리스트

### 유형별 템플릿

`references/type-templates.md`에 포함된 완전한 SKILL.md 템플릿:
- Document Processor (PDF 예시)
- Code Automator (테스트 러너 예시)
- Data Analyzer (영업 분석 예시)
- Workflow Orchestrator (배포 예시)
- Domain Expert (브랜드 가이드라인 예시)

## skill-creator와의 연동

Skill Wizard는 기존 `skill-creator` 스킬을 보완합니다:

| 기능 | skill-creator | skill-wizard |
|------|---------------|--------------|
| 접근 방식 | 문서 기반 | 질문 기반 |
| Description 지원 | 기본 언급 | 종합 가이드 |
| 템플릿 | 일반 템플릿 | 5가지 유형별 템플릿 |
| 테스트 생성 | 없음 | 자동화 도구 |
| 대상 사용자 | 경험자 | 초보자~전문가 |

함께 사용하기:
1. **skill-wizard** → 스킬 계획 및 설계
2. **skill-creator** → 초기화 (`init_skill.py`) 및 패키징 (`package_skill.py`)

## 요구사항

- Claude Code CLI
- Python 3.8+ (스크립트용)

## 기여

기여를 환영합니다! Pull Request를 자유롭게 제출해주세요.

## 라이선스

MIT 라이선스 - 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

## 관련 링크

- [skill-creator](https://github.com/anthropics/skills) - 공식 스킬 생성 도구
- [Claude Code 문서](https://docs.anthropic.com/claude-code)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
