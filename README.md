# CTons JARVIS (CTons AMY)

AI-Powered LinkedIn Marketing & Research Agent Operating System.

## Purpose

CTons AMY is a local AI command center for CTons Solutions, combining a voice
assistant (AMY), multi-agent orchestration, LinkedIn automation, research and
content tooling into a single operating system.

## Folder Structure

See `PROJECT_STRUCTURE.md` for the complete repository tree.

- `backend/` - FastAPI backend, agents, orchestrator, services, database models
- `frontend/` - React dashboard
- `prompts/` - Agent and system prompt templates
- `database/` - Database migrations, seeds, schema docs
- `storage/` - Local file storage (generated assets, uploads, logs)
- `scripts/` - Setup, start/stop, and database utility scripts
- `docs/` - Architecture, API, agent, and deployment documentation
- `tests/` - End-to-end tests and fixtures
- `docker/` - Container definitions

## Future Implementation Phases

1. Backend foundation (FastAPI app, config, database models, migrations)
2. Agent framework (base agent, registry, orchestrator, task manager)
3. Individual agents (research, competitor, keyword, content, creative, linkedin, analytics)
4. Provider integrations (OpenAI, LinkedIn, search, voice, wake word, storage)
5. Voice pipeline (wake word, STT, TTS, voice session management)
6. Scheduler and workflow engine
7. Frontend dashboard (pages, components, hooks, stores, API clients)
8. WebSocket real-time updates and agent activity visualization
9. Human approval workflows and audit logging
10. Analytics and memory subsystems

This repository currently contains only the project skeleton. No application
functionality has been implemented yet.
