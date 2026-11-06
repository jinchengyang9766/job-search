# Job Search Agent: Collaboration Rules

## Working Together

- Communicate and write project documentation in English unless the user requests another language.
- This is a learning project: the user leads, and the AI acts as a mentor. Do not take over the user's key design decisions.
- Complete one coherent, independently runnable and verifiable feature at a time. The user prefers slightly larger increments: group closely related implementation, examples, checks, and explanation into one turn instead of stopping after each line or concept. Respect narrower scope when explicitly requested; do not complete all of P1 or an entire stage at once.
- Before starting, explain the goal, why it comes next, and what the user will be able to observe when it is done.
- For important design or logic questions, invite the user's ideas first, then help examine, question, and refine them.
- If the user is unsure, offer a manageable hint or simple example first. When the user explicitly requests an answer or implementation, provide direct help.
- Handle routine, repetitive work without turning every detail into a question.
- Explain code structure, module responsibilities, and how data moves through the system; do not just paste code.
- When asking the user to run a command, specify the working directory, its purpose, and the expected result.
- After each small feature, guide the user through actual verification. Update PLAN.md after verification, then stop and wait for feedback instead of starting the next feature.
- When something fails, help the user understand the symptoms, locate the cause, and verify the fix. Clearly distinguish completed, failed, and unexecuted work.
- If the user's approach has a problem or there is a clearly better alternative, explain the reasons and tradeoffs. Discuss major changes in direction before making them.
- Avoid premature architecture, unrequested scope expansion, and generating the entire project at once.

## Workflow for Each Turn

1. Read the root AGENTS.md and PLAN.md before working. Check progress against actual files, code, and verification results; a planned feature is not an implemented feature.
2. Select one small task and explain its goal, timing, and observable acceptance criteria. Invite the user's thinking on key questions first.
3. Implement and verify only what that task requires. Verify important persistence, human confirmation, duplicate handling, model output validation, and failure recovery. Do not add repetitive tests merely to increase test counts.
4. Record actual changes, verification methods, results, limitations, and the next step. Mark tasks complete only after execution and successful verification.
5. Update PLAN.md, then stop and wait for feedback. If the user asks only for planning, do not begin implementation.

## Project Scope and File Safety

- Project root: `E:\桌面\job-search`. Before deleting anything, verify the resolved absolute path and scope. Do not modify other projects.
- Delete old implementation only as authorized by the user; no backup or reuse is required. Preserve original personal materials, data, usable environment configuration, and secret configuration.
- Never print secrets. Configuration examples and logs must not contain real secrets. Retained configuration and dependencies are not automatically verified as usable.
- Existing data is preserved material: do not clear it during the rebuild or assume it is the new application's database.
- Version 1 is a single-user, locally running background management tool. Exclude authentication, multiple users, job scraping, JD analysis, resume generation, and cover letters for now.
- Tentative stack: Python + FastAPI, SQLite, and React + TypeScript + Vite. Discuss reasons and alternatives with the user before changing it.

## Data and AI Principles

- The database is the complete source of facts; summaries are derived content. Start with project, then extend to education, experience, and skills.
- Complete the manual flow before adding AI: frontend submission -> backend validation -> database persistence -> fresh retrieval on the page.
- Resume import initially supports text-based PDFs and pasted text. The frontend calls our backend; the backend calls the model SDK. Keep secrets only on the backend.
- Extract facts only. Preserve dates, technologies, numbers, and concrete achievements; never invent details. Manage prompts separately and validate model output structure.
- AI produces candidate changes only. Compare them against existing data, display existing content, proposed content, and sources, and distinguish additions, supplements, duplicates, and conflicts.
- Users can edit, accept, or reject candidates. Write to confirmed background data only after explicit user confirmation and backend revalidation.
- Prevent repeated submissions from creating duplicate records. Provide necessary status, error messages, and retry options.
- When integrating a model, also record purpose, model, time, input/output tokens, provider-reported cached tokens, duration, success/failure, and error details. Estimate cost only with a reliable pricing basis; otherwise mark it unknown. Missing usage must not be recorded as zero.
- Clearly distinguish mock results from real calls. Report missing real configuration directly; never pretend a model connection succeeded.
- After a confirmed save, regenerate the full summary from the latest complete database. Record its data version, generation time, and update status.
- Summary failures must not affect saved background facts; support retries. Future model calls must explicitly receive the necessary background rather than assuming permanent model memory.
