from app.orchestrator.router import CommandRouter


def test_research_command():
    router = CommandRouter()

    result = router.classify(
        "Research AI agent trends"
    )

    assert result == "RESEARCH"


def test_competitor_command():
    router = CommandRouter()

    result = router.classify(
        "Find what our competitors are posting"
    )

    assert result == "COMPETITOR_RESEARCH"


def test_keyword_command():
    router = CommandRouter()

    result = router.classify(
        "Find keywords and hashtags for AI automation"
    )

    assert result == "KEYWORD_RESEARCH"


def test_general_command():
    router = CommandRouter()

    result = router.classify(
        "Show me my dashboard"
    )

    assert result == "GENERAL"