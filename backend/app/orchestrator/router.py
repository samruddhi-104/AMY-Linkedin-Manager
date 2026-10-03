import re


class CommandRouter:
    """
    Converts natural-language commands into AMY intents.
    """

    RESEARCH_PATTERNS = [
        r"\bresearch\b",
        r"\bresearching\b",
        r"\btrend(s)?\b",
        r"\bwhat is happening\b",
        r"\bfind information\b",
        r"\bwhat'?s new\b",
        r"\bwhat'?s trending\b",
        r"\bnews\b",
    ]

    COMPETITOR_PATTERNS = [
        r"\bcompetitor(s)?\b",
        r"\bcompetition\b",
        r"\bother companies\b",
        r"\bcompetitive\b",
        r"\bwhat .* competitors\b",
    ]

    KEYWORD_PATTERNS = [
        r"\bkeyword(s)?\b",
        r"\bhashtag(s)?\b",
        r"\bsearch term(s)?\b",
    ]

    CONTENT_PATTERNS = [
        r"\bcreate .*post\b",
        r"\bwrite .*post\b",
        r"\bgenerate .*post\b",
        r"\bcreate .*linkedin\b",
        r"\bwrite .*linkedin\b",
        r"\bcontent\b",
        r"\bpost idea\b",
        r"\blinkedin post\b",
    ]

    CREATIVE_PATTERNS = [
        r"\bcreate .*image\b",
        r"\bgenerate .*image\b",
        r"\bmake .*image\b",
        r"\bcreate .*visual\b",
        r"\bmake .*visual\b",
        r"\bcreate .*graphic\b",
        r"\bgenerate .*creative\b",
    ]

    LINKEDIN_PATTERNS = [
        r"\bpublish\b",
        r"\bpost on linkedin\b",
        r"\blinkedin publish\b",
        r"\bpublish on linkedin\b",
    ]

    SCHEDULE_PATTERNS = [
        r"\bschedule\b",
        r"\bscheduled\b",
        r"\bschedule .*post\b",
        r"\bschedule .*linkedin\b",
    ]

    def classify(
        self,
        command: str,
    ) -> str:
        """
        Classify a command into an AMY intent.
        """

        normalized = (
            command
            .lower()
            .strip()
        )

        if not normalized:
            return "GENERAL"

        # -----------------------------------------------------
        # Scheduling
        # -----------------------------------------------------

        if any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in self.SCHEDULE_PATTERNS
        ):
            return "LINKEDIN_SCHEDULE"

        # -----------------------------------------------------
        # LinkedIn publishing
        # -----------------------------------------------------

        if any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in self.LINKEDIN_PATTERNS
        ):
            return "LINKEDIN_PUBLISH"

        # -----------------------------------------------------
        # Creative / image generation
        # -----------------------------------------------------

        if any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in self.CREATIVE_PATTERNS
        ):
            return "CREATIVE_GENERATION"

        # -----------------------------------------------------
        # Content generation
        # -----------------------------------------------------

        if any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in self.CONTENT_PATTERNS
        ):
            return "CONTENT_GENERATION"

        # -----------------------------------------------------
        # Competitor research
        # -----------------------------------------------------

        if any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in self.COMPETITOR_PATTERNS
        ):
            return "COMPETITOR_RESEARCH"

        # -----------------------------------------------------
        # Keyword / hashtag research
        # -----------------------------------------------------

        if any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in self.KEYWORD_PATTERNS
        ):
            return "KEYWORD_RESEARCH"

        # -----------------------------------------------------
        # General research
        # -----------------------------------------------------

        if any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in self.RESEARCH_PATTERNS
        ):
            return "RESEARCH"

        return "GENERAL"