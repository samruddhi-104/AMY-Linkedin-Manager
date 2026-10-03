# CTons AMY - Project Structure

Complete repository tree (skeleton only, no implementation).

```
ctons-amy/
├── .github/
│   └── workflows/
│       ├── backend-tests.yml
│       └── frontend-tests.yml
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── .gitkeep
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── agents/
│   │   │   ├── analytics_agent/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── schemas.py
│   │   │   ├── competitor_agent/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── schemas.py
│   │   │   ├── content_agent/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── schemas.py
│   │   │   ├── creative_agent/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── schemas.py
│   │   │   ├── keyword_agent/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── schemas.py
│   │   │   ├── linkedin_agent/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── schemas.py
│   │   │   ├── research_agent/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── schemas.py
│   │   │   ├── __init__.py
│   │   │   ├── agent_registry.py
│   │   │   └── base_agent.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agents.py
│   │   │   │   ├── amy.py
│   │   │   │   ├── analytics.py
│   │   │   │   ├── calendar.py
│   │   │   │   ├── competitors.py
│   │   │   │   ├── content.py
│   │   │   │   ├── creative.py
│   │   │   │   ├── health.py
│   │   │   │   ├── keywords.py
│   │   │   │   ├── linkedin.py
│   │   │   │   ├── memory.py
│   │   │   │   ├── research.py
│   │   │   │   ├── settings.py
│   │   │   │   ├── tasks.py
│   │   │   │   └── voice.py
│   │   │   ├── __init__.py
│   │   │   └── websocket.py
│   │   ├── database/
│   │   │   ├── migrations/
│   │   │   │   └── .gitkeep
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── authentication.py
│   │   │   ├── cors.py
│   │   │   ├── error_handler.py
│   │   │   └── rate_limit.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── agent_log.py
│   │   │   ├── agent_run.py
│   │   │   ├── asset.py
│   │   │   ├── audit_log.py
│   │   │   ├── company.py
│   │   │   ├── competitor.py
│   │   │   ├── content_pillar.py
│   │   │   ├── conversation.py
│   │   │   ├── hashtag.py
│   │   │   ├── integration.py
│   │   │   ├── keyword.py
│   │   │   ├── linkedin_account.py
│   │   │   ├── memory.py
│   │   │   ├── post.py
│   │   │   ├── post_variant.py
│   │   │   ├── research_report.py
│   │   │   ├── research_source.py
│   │   │   ├── scheduled_post.py
│   │   │   ├── task.py
│   │   │   ├── task_step.py
│   │   │   ├── tool_call.py
│   │   │   └── user.py
│   │   ├── orchestrator/
│   │   │   ├── __init__.py
│   │   │   ├── agent_manager.py
│   │   │   ├── execution_context.py
│   │   │   ├── permissions.py
│   │   │   ├── planner.py
│   │   │   ├── router.py
│   │   │   ├── task_manager.py
│   │   │   └── workflow_engine.py
│   │   ├── providers/
│   │   │   ├── linkedin/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   ├── exceptions.py
│   │   │   │   ├── media.py
│   │   │   │   ├── oauth.py
│   │   │   │   └── posts.py
│   │   │   ├── openai/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   ├── exceptions.py
│   │   │   │   └── models.py
│   │   │   ├── search/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   ├── exceptions.py
│   │   │   │   └── search.py
│   │   │   ├── storage/
│   │   │   │   ├── __init__.py
│   │   │   │   └── provider.py
│   │   │   ├── voice/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── realtime.py
│   │   │   │   ├── stt.py
│   │   │   │   └── tts.py
│   │   │   ├── wakeword/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── listener.py
│   │   │   │   └── provider.py
│   │   │   └── __init__.py
│   │   ├── scheduler/
│   │   │   ├── __init__.py
│   │   │   ├── jobs.py
│   │   │   ├── registry.py
│   │   │   ├── scheduler.py
│   │   │   └── timezone.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── amy.py
│   │   │   ├── analytics.py
│   │   │   ├── calendar.py
│   │   │   ├── common.py
│   │   │   ├── competitor.py
│   │   │   ├── content.py
│   │   │   ├── creative.py
│   │   │   ├── keyword.py
│   │   │   ├── linkedin.py
│   │   │   ├── memory.py
│   │   │   ├── research.py
│   │   │   ├── task.py
│   │   │   └── voice.py
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── encryption.py
│   │   │   ├── permissions.py
│   │   │   ├── secrets.py
│   │   │   └── tokens.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── analytics_service.py
│   │   │   ├── competitor_service.py
│   │   │   ├── content_service.py
│   │   │   ├── creative_service.py
│   │   │   ├── keyword_service.py
│   │   │   ├── linkedin_service.py
│   │   │   ├── memory_service.py
│   │   │   ├── notification_service.py
│   │   │   └── research_service.py
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── task_events.py
│   │   │   ├── task_states.py
│   │   │   └── task_types.py
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── competitor_research.py
│   │   │   ├── content_extractor.py
│   │   │   ├── database_tools.py
│   │   │   ├── image_generation.py
│   │   │   ├── keyword_research.py
│   │   │   ├── linkedin_tools.py
│   │   │   ├── memory_tools.py
│   │   │   ├── web_fetch.py
│   │   │   └── web_search.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── datetime.py
│   │   │   ├── files.py
│   │   │   ├── ids.py
│   │   │   ├── logging.py
│   │   │   └── validation.py
│   │   ├── voice/
│   │   │   ├── __init__.py
│   │   │   ├── audio_manager.py
│   │   │   ├── speech_to_text.py
│   │   │   ├── text_to_speech.py
│   │   │   ├── voice_session.py
│   │   │   └── wake_word.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── tests/
│   │   ├── api/
│   │   │   └── .gitkeep
│   │   ├── integration/
│   │   │   └── .gitkeep
│   │   ├── unit/
│   │   │   ├── agents/
│   │   │   │   └── .gitkeep
│   │   │   ├── orchestrator/
│   │   │   │   └── .gitkeep
│   │   │   ├── scheduler/
│   │   │   │   └── .gitkeep
│   │   │   ├── services/
│   │   │   │   └── .gitkeep
│   │   │   └── tools/
│   │   │       └── .gitkeep
│   │   └── __init__.py
│   ├── alembic.ini
│   ├── pyproject.toml
│   ├── requirements-dev.txt
│   └── requirements.txt
├── database/
│   ├── migrations/
│   │   └── .gitkeep
│   ├── schemas/
│   │   └── README.md
│   ├── seeds/
│   │   └── README.md
│   └── README.md
├── docker/
│   ├── backend/
│   │   └── Dockerfile
│   ├── frontend/
│   │   └── Dockerfile
│   └── postgres/
│       └── README.md
├── docs/
│   ├── agents/
│   │   ├── analytics_agent.md
│   │   ├── competitor_agent.md
│   │   ├── content_agent.md
│   │   ├── creative_agent.md
│   │   ├── keyword_agent.md
│   │   ├── linkedin_agent.md
│   │   └── research_agent.md
│   ├── api/
│   │   └── api_reference.md
│   ├── architecture/
│   │   ├── agent_architecture.md
│   │   ├── system_architecture.md
│   │   ├── voice_architecture.md
│   │   └── workflow_architecture.md
│   ├── database/
│   │   ├── database_schema.md
│   │   └── relationships.md
│   ├── deployment/
│   │   ├── docker.md
│   │   └── windows.md
│   ├── development/
│   │   ├── development_guide.md
│   │   └── troubleshooting.md
│   ├── integrations/
│   │   ├── linkedin.md
│   │   ├── openai.md
│   │   ├── search.md
│   │   └── voice.md
│   └── security/
│       └── security.md
├── frontend/
│   ├── public/
│   │   ├── fonts/
│   │   │   └── .gitkeep
│   │   ├── icons/
│   │   │   └── .gitkeep
│   │   └── images/
│   │       └── .gitkeep
│   ├── src/
│   │   ├── assets/
│   │   │   └── .gitkeep
│   │   ├── components/
│   │   │   ├── agents/
│   │   │   │   └── .gitkeep
│   │   │   ├── analytics/
│   │   │   │   └── .gitkeep
│   │   │   ├── calendar/
│   │   │   │   └── .gitkeep
│   │   │   ├── command/
│   │   │   │   └── .gitkeep
│   │   │   ├── common/
│   │   │   │   └── .gitkeep
│   │   │   ├── competitors/
│   │   │   │   └── .gitkeep
│   │   │   ├── content/
│   │   │   │   └── .gitkeep
│   │   │   ├── creative/
│   │   │   │   └── .gitkeep
│   │   │   ├── keywords/
│   │   │   │   └── .gitkeep
│   │   │   ├── layout/
│   │   │   │   └── .gitkeep
│   │   │   ├── linkedin/
│   │   │   │   └── .gitkeep
│   │   │   ├── memory/
│   │   │   │   └── .gitkeep
│   │   │   ├── navigation/
│   │   │   │   └── .gitkeep
│   │   │   ├── research/
│   │   │   │   └── .gitkeep
│   │   │   ├── settings/
│   │   │   │   └── .gitkeep
│   │   │   ├── tasks/
│   │   │   │   └── .gitkeep
│   │   │   └── voice/
│   │   │       └── .gitkeep
│   │   ├── config/
│   │   │   └── .gitkeep
│   │   ├── constants/
│   │   │   └── .gitkeep
│   │   ├── hooks/
│   │   │   ├── useAgents.ts
│   │   │   ├── useAmy.ts
│   │   │   ├── useContent.ts
│   │   │   ├── useCreative.ts
│   │   │   ├── useLinkedIn.ts
│   │   │   ├── useResearch.ts
│   │   │   ├── useTasks.ts
│   │   │   ├── useVoice.ts
│   │   │   └── useWebSocket.ts
│   │   ├── pages/
│   │   │   ├── Agents/
│   │   │   │   └── .gitkeep
│   │   │   ├── Analytics/
│   │   │   │   └── .gitkeep
│   │   │   ├── Calendar/
│   │   │   │   └── .gitkeep
│   │   │   ├── Competitors/
│   │   │   │   └── .gitkeep
│   │   │   ├── Content/
│   │   │   │   └── .gitkeep
│   │   │   ├── Creative/
│   │   │   │   └── .gitkeep
│   │   │   ├── Dashboard/
│   │   │   │   └── .gitkeep
│   │   │   ├── History/
│   │   │   │   └── .gitkeep
│   │   │   ├── Keywords/
│   │   │   │   └── .gitkeep
│   │   │   ├── LinkedIn/
│   │   │   │   └── .gitkeep
│   │   │   ├── Memory/
│   │   │   │   └── .gitkeep
│   │   │   ├── Research/
│   │   │   │   └── .gitkeep
│   │   │   └── Settings/
│   │   │       └── .gitkeep
│   │   ├── services/
│   │   │   ├── api/
│   │   │   │   ├── agents.ts
│   │   │   │   ├── amy.ts
│   │   │   │   ├── analytics.ts
│   │   │   │   ├── calendar.ts
│   │   │   │   ├── client.ts
│   │   │   │   ├── competitors.ts
│   │   │   │   ├── content.ts
│   │   │   │   ├── creative.ts
│   │   │   │   ├── keywords.ts
│   │   │   │   ├── linkedin.ts
│   │   │   │   ├── memory.ts
│   │   │   │   ├── research.ts
│   │   │   │   ├── settings.ts
│   │   │   │   └── tasks.ts
│   │   │   └── websocket.ts
│   │   ├── stores/
│   │   │   ├── agentStore.ts
│   │   │   ├── appStore.ts
│   │   │   ├── settingsStore.ts
│   │   │   ├── taskStore.ts
│   │   │   └── voiceStore.ts
│   │   ├── types/
│   │   │   ├── agents.ts
│   │   │   ├── analytics.ts
│   │   │   ├── api.ts
│   │   │   ├── calendar.ts
│   │   │   ├── competitors.ts
│   │   │   ├── content.ts
│   │   │   ├── creative.ts
│   │   │   ├── keywords.ts
│   │   │   ├── linkedin.ts
│   │   │   ├── research.ts
│   │   │   └── tasks.ts
│   │   ├── utils/
│   │   │   └── .gitkeep
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
├── prompts/
│   ├── analytics/
│   │   └── analytics_agent_prompt.md
│   ├── competitor/
│   │   └── competitor_agent_prompt.md
│   ├── content/
│   │   └── content_agent_prompt.md
│   ├── creative/
│   │   └── creative_agent_prompt.md
│   ├── keywords/
│   │   └── keyword_agent_prompt.md
│   ├── linkedin/
│   │   └── linkedin_agent_prompt.md
│   ├── orchestrator/
│   │   ├── planner_prompt.md
│   │   └── router_prompt.md
│   ├── research/
│   │   └── research_agent_prompt.md
│   └── system/
│       ├── amy_system.md
│       └── safety_rules.md
├── scripts/
│   ├── database/
│   │   ├── reset_database.py
│   │   └── seed_demo_data.py
│   ├── setup/
│   │   ├── setup_windows.bat
│   │   └── setup_windows.ps1
│   ├── start/
│   │   ├── start_amy.bat
│   │   ├── start_backend.bat
│   │   └── start_frontend.bat
│   ├── stop/
│   │   └── stop_amy.bat
│   └── utilities/
│       └── README.md
├── storage/
│   ├── generated/
│   │   ├── carousels/
│   │   │   └── .gitkeep
│   │   ├── exports/
│   │   │   └── .gitkeep
│   │   └── images/
│   │       └── .gitkeep
│   ├── logs/
│   │   └── .gitkeep
│   ├── temporary/
│   │   └── .gitkeep
│   └── uploads/
│       └── .gitkeep
├── tests/
│   ├── e2e/
│   │   └── .gitkeep
│   ├── fixtures/
│   │   └── .gitkeep
│   └── README.md
├── .env.example
├── .gitignore
├── LICENSE
├── PROJECT_STRUCTURE.md
├── README.md
└── docker-compose.yml
```
