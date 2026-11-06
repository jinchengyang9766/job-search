# Job Search Agent: Blueprint and Progress

Last updated: 2026-11-05 (America/Toronto)

## Goal and Scope

Version 1 is a single-user, locally running personal background management tool that provides reliable facts for future job matching and resume generation.
Categories include project, education, experience, and skills. Establish the flow with project first, then extend one category at a time.
The reset milestone is complete. P1 is In progress: name and description reject blank input, project_type accepts five fixed English enum values, and organization is optional for personal projects but must contain non-whitespace text for other types. Remaining fields and date/list rules are not implemented.
Authentication, multiple users, job scraping, JD analysis, resume generation, and cover letters remain out of scope. Stage 5 is a future discussion only.

## Tentative Stack and Responsibilities

- Python + FastAPI: input validation, background data access, import review, and model SDK calls.
- SQLite: confirmed background facts, sources, and necessary processing state. Table structures are not decided yet.
- React + TypeScript + Vite: manual entry, retrieved data display, candidate review, and status feedback.
- P1 uses the existing Python 3.12.14 virtual environment and Pydantic 2.14.1. The new requirements.txt records only that direct dependency; no packages were installed. Other dependencies, data access approach, and AI model remain undecided.

Data flow: page input -> backend validation -> SQLite -> backend query -> page display.
AI import adds text reading -> SDK extraction -> output validation -> comparison -> user review and confirmation before confirmed persistence.
Summaries are derived after confirmed saves; they are not the complete source of facts.

## Agreed Product Flow

1. Background storage: define necessary project fields, stable IDs, sources, and update timestamps, then implement create, read, update, and delete separately.
2. Manual entry: fill in -> frontend submission -> backend validation -> database persistence -> fresh page retrieval. Verify real persistence before AI; keep the UI clear and usable.
3. Resume import: upload a text-based PDF or paste text -> backend reads text -> backend uses a model SDK to extract structured information -> compare against the existing database -> show candidates and suggested changes -> user edits, selects, and confirms -> backend validates and saves.
4. Background summary: after the user confirms database changes, regenerate the full summary from the latest complete data. Record data version, generation time, and status. Failures can be retried without affecting saved facts.
5. Later extensions: discuss JD analysis, background selection, and new resume generation only after these flows are stable. Do not implement them now.

## Small Tasks and Acceptance Criteria

Use only these statuses: Not started, In progress, Awaiting verification, Verified. R0 is Verified. P1 is In progress; P1.1, P1.2, P1.3a, P1.3b, and P1.3c below are Verified through agent-run checks. All other feature tasks are Not started.
Dependencies are prerequisites, not permission to execute tasks continuously. Complete one task, verify and update this file, then stop.
Future tasks may be divided further before implementation; never combine them into broad tasks such as "finish the backend."
The user requested slightly larger increments. Group related implementation, examples, verification, and explanation into one coherent feature per turn, rather than stopping at each line or concept. Continue to stop after the agreed feature; do not complete all of P1 at once.

### R0: Reset and Guidance Documents

- Status: Verified.
- Goal: confirm the root, remove the old backend, preserve other files, and create AGENTS.md and this file.
- Acceptance criteria: inspect the root again; backend is absent, both documents contain content, and preserved items remain.

### Stage 1: Project Structure and Basic Storage

| Task | Depends on | Observable acceptance criteria |
| --- | --- | --- |
| P1 Minimal project schema and local validation | R0; discuss fields first | One valid example passes and one invalid example produces a clear error. Explain required/optional fields and who supplies the stable ID, source, and update timestamp. |
| P2 Write and read one SQLite record | P1 | Write using a local command, exit, then restart and retrieve the same ID. Use an explicit new database path without touching the old database. |
| P3 Minimal FastAPI health endpoint | P2 | Start locally and receive a clear response from the health endpoint. Install only dependencies needed for this task. |
| P4 Create project endpoint | P3 | A valid request persists a record and returns its ID; invalid input leaves no record. |
| P5 Retrieve project by ID | P4 | Return stored content; an unknown ID produces a clear error. |
| P6 List projects endpoint | P5 | Return an empty list for an empty database and actual stored content when records exist. |
| P7 Update one project | P5 | Keep the ID stable and change the update timestamp. Invalid changes preserve the original content. |
| P8 Delete one project | P7 | The deleted record can no longer be retrieved. Define behavior for missing records and leave other records intact. |

Agreed project record design (implement incrementally):

| Field | Agreed rule |
| --- | --- |
| name | Required string; must contain non-whitespace text. |
| project_type | Required project category using fixed English values: personal, course, company, competition, or other. The user explicitly chose English values. |
| organization | School, company, or organizer; project affiliation, not a geographic address. May be empty for personal projects; required otherwise. |
| start_date | Required valid year-month in YYYY-MM format; do not invent a day. |
| end_date | Valid year-month in YYYY-MM format when present. Must be absent for ongoing projects and present for ended projects. Must not precede start_date. |
| is_ongoing | Required boolean; must be consistent with end_date. |
| description | Required string describing the project's purpose and functionality; must contain non-whitespace text. |
| contributions | Required list of strings describing the user's own work; at least one item, with no blank items. |
| tech_stack | Required list of strings naming technologies and tools actually used; at least one item, with no blank items. |

P1 small steps:

| Step | Status | Scope and verification |
| --- | --- | --- |
| P1.1 Two-field model and fictional example | Verified | project.py defines Project(BaseModel) with only name: str and description: str. demo_project.py creates and prints a fictional record in memory. The agent ran it successfully; the user's rerun is pending. |
| P1.2 Nonblank name and description | Verified | Both fields use Field(min_length=1, pattern=r"\S"). Empty and whitespace-only strings are rejected; valid text is preserved without trimming. The fictional example shows validation errors. Agent-run checks passed; the user's rerun is pending. |
| P1.3a Project type | Verified | Added ProjectType(str, Enum) with five user-approved English values and required project_type: ProjectType. Agent-run checks accepted all five values, rejected an unsupported value and a missing field, and confirmed conversion to enum members. The fictional demo shows the value and an invalid-type error; the user's rerun is pending. |
| P1.3b Organization field | Verified | Added organization: str \| None = None for affiliation. Omission and explicit None were accepted, a fictional school name was preserved, and an integer was rejected. Missing/blank affiliation for non-personal projects was an intermediate limitation, now resolved by P1.3c. |
| P1.3c Conditional organization requirement | Verified | Added an after-model validator: personal projects allow missing/blank affiliation, while course/company/competition/other require nonblank affiliation. All branches were checked in memory; the fictional demo shows missing and whitespace-only failures. Text is checked without normalization. |
| P1.4 Contributions and technology lists | Not started | Add the two related list fields and their nonempty-list/nonblank-item rules as one coherent feature, with meaningful valid and invalid examples. |
| P1.5 Month-only dates and ongoing flag | Not started | Add fields incrementally, validate real YYYY-MM values, and preserve month precision. |
| P1.6 Cross-field consistency | Not started | Check ongoing/end-date consistency and date ordering, one rule at a time. |
| P1.7 Review P1 acceptance criteria | Not started | Verify the complete agreed rules and clarify stable ID, source, and update timestamp responsibilities before storage. Do not add metadata to P1.1 or begin P2 automatically. |

Current files are deliberately small: project.py defines the schema and one after-model validator, demo_project.py prints fictional valid instances and catches expected ValidationErrors, and requirements.txt records Pydantic. No persistence, HTTP, frontend, AI, or test framework has been added.
Validation checks structure and consistency, not whether a claimed achievement actually happened. After each small step, explain the result, update this plan, and stop for user feedback.

### Stage 2: Basic Pages and Manual Entry

| Task | Depends on | Observable acceptance criteria |
| --- | --- | --- |
| U1 Minimal React page | P8 | Open locally and see static entry and list areas without expanding business scope. |
| U2 Retrieve project list on the page | U1, P6 | Display database content, with clear empty and request-failure states. |
| U3 Submit form and retrieve saved data | U2, P4 | Fill in -> submit -> validate -> save -> retrieve again. Data survives a page refresh; invalid input is not stored. |
| U4 Edit project on the page | U3, P7 | Retrieve the updated content after saving. Validation errors preserve the user's input and explain the problem. |
| U5 Delete project on the page | U4, P8 | Delete after an explicit user action; it remains absent after refresh. Canceling does not delete anything. |

After project is stable, extend to education, experience, and skills one at a time. For each category, repeat field discussion and validation -> storage -> individual CRUD endpoints -> individual page operations. List those specific tasks here before starting; do not implement a whole category in one step. Complete the necessary categories before full resume import; early extraction exercises may cover project only if the limited scope is explicit.

### Stage 3: Resume Import and Human Review

| Task | Depends on | Observable acceptance criteria |
| --- | --- | --- |
| I1 Accept pasted text | U3 | The backend accepts nonempty text and records its source. Empty input produces a clear error; confirmed background data stays unchanged. |
| I2 Read text-based PDFs | I1 | Read text from a text-based PDF. Corrupt, textless, or unsupported files produce clear messages; do not claim OCR support. |
| I3 Candidate schema and mock extraction | P1, I1 | Valid candidates pass structural validation and invalid ones are rejected. Responses are explicitly labeled mock; confirmed data stays unchanged. |
| I4 Real SDK extraction and call records | I3 | Separately managed prompts extract verifiable facts. Verify real calls only with complete configuration; missing configuration fails explicitly. Record usage, duration, outcome, and cost basis at the same time. |
| I5 Compare candidates with existing data | I3; necessary categories support storage | A few examples distinguish additions, supplements, duplicates, and conflicts. Preserve existing values, proposed values, and sources without automatically writing confirmed data. |
| I6 Display candidates on the page | I5, U2 | Show existing content, proposed content, sources, comparison types, and visible mock labels where applicable. |
| I7 Edit and select candidates | I6 | Users can edit, accept, or reject candidates. Confirmed data stays unchanged before confirmation. |
| I8 Confirm and save | I7 | Save transactionally only after explicit confirmation and backend validation. Invalid content causes no partial writes; rejected items are not saved. If data changes during review, compare again or require another review. |
| I9 Prevent duplicate submissions | I8 | Repeating the same confirmation request or retrying after a timeout creates no duplicate records. Discuss the idempotency rules first. |
| I10 Status, failures, and retries | I4, I8, I9 | Extraction, validation, and save failures can be diagnosed. The page shows status and retry options without false success or duplicate persistence. |

I4 call records include purpose, model, time, input/output tokens, provider-reported cached tokens, duration, success/failure, and error details. Estimate cost and record its basis only with reliable pricing; otherwise mark it unknown. Usage the provider does not report is unknown, not zero. Label mock runs separately and do not count them as real calls. Error logs must not expose secrets.
Extraction must preserve dates, technologies, numbers, and concrete achievements without inventing details. Invalid model output cannot enter confirmed persistence. AI cannot bypass human confirmation. Processing states must at least distinguish pending, processing, awaiting review, saved, and failed; discuss the exact state model before implementation.

### Stage 4: Background Summary

| Task | Depends on | Observable acceptance criteria |
| --- | --- | --- |
| S1 Confirmed background data version | I10 | Successful fact changes advance the version; failures and repeated submissions do not create false new versions. Discuss version rules first. |
| S2 Generate and record a full summary | S1, I4 | Regenerate from a complete fact snapshot and record its version, generation time, and update status. Distinguish mock and real results. |
| S3 Trigger after save and isolate failures | S2 | A successful confirmed save triggers summary generation. When summary generation fails, background facts remain saved and retrievable. |
| S4 Retry summaries and detect stale results | S3 | Retry for the current data version; old results are not treated as current. Show status and time on the page. |

Every later model call must explicitly receive necessary background rather than assume permanent memory. Summaries never overwrite or replace database facts.

### Stage 5: Discuss Future Directions Only

Prerequisite: background storage, manual entry, import review, and summaries have been verified as stable. Then discuss JD analysis, background selection, and new resume generation with the user and define separate tasks. There are no implementation tasks for this stage now.

## Confirmed Design Decisions

- Single-user and local first. Start with project, complete the manual flow, then add AI. Avoid premature architecture.
- Project categories use fixed English enum values: personal, course, company, competition, other. Any future display labels can be separate from these values; no UI has been implemented.
- organization is affiliation, not a geographic address. It defaults to None when omitted. Personal projects may omit it or supply None/blank text; all other project types require nonblank text. An after-model validator checks the relationship after field validation. strip() is used only to detect blank text, without changing the original value.
- Stable IDs do not depend on editable project names. Distinguish background event dates from system update timestamps; formats remain undecided.
- Confirmed facts, AI candidates, and derived summaries have separate responsibilities. Sources help users verify facts.
- User confirmation is the boundary for writing confirmed data; backend validation is mandatory.
- Use the model SDK only on the backend. Manage prompts separately, label mock results, and report missing real configuration explicitly.
- Rebuild summaries from the latest complete data. Summary failures do not roll back successfully saved background facts.

## Open Questions

- The user has supplied the agreed fields above. Do not reopen those decisions without a concrete reason; introduce their rules one small step at a time.
- Month-only date precision is agreed. Stable ID generation, source granularity, and system update timestamps remain to be discussed before storage, outside P1.1.
- Discuss category fields, duplicate/conflict detection, and confirmation-request idempotency before their respective tasks.
- Choose the data access approach, database change approach, model and SDK, summary format, and version rules when needed rather than deciding in advance.

## Current Status and Actual Verification

- Confirmed root: `E:\桌面\job-search`. During the initial inspection, no AGENTS.md was found in the project or checked parent directories, and no existing PLAN.md was found.
- The old backend was deleted. Its absolute path and directory links were checked before deletion, and its absence was verified afterward.
- Preserved data (including old SQLite files), .venv, .env.example, and .gitignore. Personal source content was not read and secret values were not printed.
- Existing data is not automatically reused. Decide the new database location in P2. The virtual environment has been verified only for this Pydantic example; environment configuration and the full future stack remain unverified.
- R0 verification passed: correct root, backend absent, both documents nonempty, and all four preserved items present. Verification used PowerShell path/nonempty assertions and document readback.
- Documentation remains in English. The user explicitly requested Chinese conversation for the current learning work; follow that request.
- Initial inspection for P1.1 found no application code or dependency manifest. Reused .venv (Python 3.12.14, Pydantic 2.14.1); pip is not installed there. No installation was needed or performed.
- Added project.py, demo_project.py, and requirements.txt at the root. Preserved all existing work, personal data, environment files, and the virtual environment; no deletions or git commits.
- The user confirmed the class/instance explanation and requested the next small step. A local user-run result has not been reported; do not assume it was executed.
- P1.2 changes: imported Field and added min_length=1 plus pattern=r"\S" to name and description. Neither field has a default. Leading/trailing whitespace in otherwise valid text is preserved. No fields, dependencies, or custom validators were added.
- P1.2 checks passed at that step: both text fields reject empty strings and whitespace-only strings containing spaces, tabs, and newlines; valid text is preserved. No test files or test framework were added.
- The user requested continuation after P1.2. P1.3 was divided into project type, organization, and the conditional organization rule so that each turn remains small.
- The user chose fixed English category values. P1.3a added ProjectType in project.py and the required project_type field. demo_project.py supplies a valid type in previous examples and adds an unsupported-type example. requirements.txt is unchanged; no packages were installed.
- P1.3a checks passed at that step: all five English values are accepted and converted to ProjectType members; unsupported and missing types produce the expected field-specific errors.
- The user confirmed understanding of enum members and values, then requested continuation. P1.3b adds only organization: str | None = None. The demo retains earlier examples, prints the default None, and adds a fictional course project with a fictional school. No dependencies or other fields were added.
- P1.3b checks passed at that step: omitted organization and explicit None yielded None; a fictional organization string was preserved; an integer was rejected with a field error. The conditional requirement was deliberately deferred until P1.3c.
- The user requested slightly larger increments. Updated AGENTS.md to group related edits, examples, checks, and explanation into one coherent feature. README.md and the existing Git repository were inspected and preserved; no files were deleted and no commits were made.
- P1.3c added @model_validator(mode="after") and require_organization(self). For non-personal types, None or an empty result from strip() raises ValueError with an organization-specific message. Successful validation returns self; values are not rewritten.
- Latest verification command from the root: `.\.venv\Scripts\python.exe -B .\demo_project.py`. Exit code 0; valid personal/course examples succeeded, missing company affiliation and blank course affiliation produced expected model-level errors, and previous text/type examples still produced expected field errors. Demonstrations remain fictional and in memory.
- Additional in-memory checks passed: each of the five types accepts named affiliation unchanged; personal projects accept omission, None, empty text, and spaces/tabs/newlines; each of the four non-personal types rejects those missing/blank cases. Invalid integer affiliation still produces a field error, and the model still has exactly four fields.
- Feature progress: R0, P1.1, P1.2, P1.3a, P1.3b, and P1.3c are Verified through agent-run checks; P1 overall remains In progress. P1.4 and later tasks are Not started. No dependencies, database, API, frontend, or AI functionality were added.
- Session checkpoint: the user ended today's development session after P1.3c and requested a Git commit and push of the current work. No additional features are authorized for this session.
- Next development session: resume with P1.4, covering contributions and tech_stack together with their list and item rules, following the user's preference for slightly larger increments. User-run verification has not been reported.
