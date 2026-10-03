import { useMemo, useState } from "react";

type Agent = {
  id: string;
  name: string;
  role: string;
  icon: string;
  position: string;
};

type Activity = {
  id: number;
  agent: string;
  text: string;
  time: string;
};

type Message = {
  sender: "amy" | "user";
  text: string;
};

const agents: Agent[] = [
  {
    id: "research",
    name: "Research",
    role: "Trends & intelligence",
    icon: "⌕",
    position: "research",
  },
  {
    id: "competitor",
    name: "Competitor",
    role: "Competitor monitoring",
    icon: "◈",
    position: "competitor",
  },
  {
    id: "keyword",
    name: "Keywords",
    role: "Keywords & hashtags",
    icon: "#",
    position: "keyword",
  },
  {
    id: "content",
    name: "Content",
    role: "Post generation",
    icon: "✦",
    position: "content",
  },
  {
    id: "creative",
    name: "Creative",
    role: "Visual generation",
    icon: "◉",
    position: "creative",
  },
  {
    id: "linkedin",
    name: "LinkedIn",
    role: "Publishing & scheduling",
    icon: "↗",
    position: "linkedin",
  },
];

const agentKeywords: Record<string, string[]> = {
  research: [
    "research",
    "trend",
    "trends",
    "news",
    "topic",
    "find",
  ],
  competitor: [
    "competitor",
    "competitors",
    "competition",
    "competitive",
  ],
  keyword: [
    "keyword",
    "keywords",
    "hashtag",
    "hashtags",
    "seo",
    "search term",
  ],
  content: [
    "content",
    "post",
    "write",
    "caption",
    "linkedin post",
    "create content",
  ],
  creative: [
    "image",
    "creative",
    "design",
    "visual",
    "graphic",
  ],
  linkedin: [
    "linkedin",
    "publish",
    "schedule",
    "post it",
  ],
};

function getTime() {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function detectAgent(command: string): string {
  const normalized = command.toLowerCase();

  for (const agent of agents) {
    const keywords = agentKeywords[agent.id] || [];

    if (
      keywords.some((keyword) =>
        normalized.includes(keyword)
      )
    ) {
      return agent.id;
    }
  }

  return "content";
}

function App() {
  const [command, setCommand] = useState("");
  const [activeAgent, setActiveAgent] = useState<string | null>(null);
  const [systemState, setSystemState] = useState("READY");
  const [listening, setListening] = useState(false);

  const [activities, setActivities] = useState<Activity[]>([
    {
      id: 1,
      agent: "AMY",
      text: "System initialized and ready.",
      time: getTime(),
    },
    {
      id: 2,
      agent: "SYSTEM",
      text: "All agents waiting for instructions.",
      time: getTime(),
    },
  ]);

  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "amy",
      text:
        "Hello. I'm AMY. Tell me what you want to accomplish and I'll activate the required agent.",
    },
  ]);

  const activeAgentInfo = useMemo(
    () =>
      agents.find(
        (agent) => agent.id === activeAgent
      ),
    [activeAgent]
  );

  /*
   * Main AMY command pipeline
   *
   * Frontend
   *   ↓
   * POST /api/amy/command
   *   ↓
   * FastAPI AMY route
   *   ↓
   * CommandRouter
   *   ↓
   * TaskManager / TaskExecutor
   */
  const runCommand = async (value?: string) => {
    const text = (value ?? command).trim();

    if (!text) {
      return;
    }

    // Local visual estimate so the UI reacts immediately.
    const localAgentId = detectAgent(text);

    const localAgent = agents.find(
      (agent) => agent.id === localAgentId
    );

    // Show command in chat immediately.
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text,
      },
      {
        sender: "amy",
        text:
          `${localAgent?.name || "AMY"} is being activated...`,
      },
    ]);

    // Immediately show the likely agent as working.
    setActiveAgent(localAgentId);
    setSystemState("WORKING");

    setActivities((prev) => [
      {
        id: Date.now(),
        agent: "AMY",
        text: `Sending command to backend: ${text}`,
        time: getTime(),
      },
      ...prev,
    ]);

    setCommand("");

    try {
      const response = await fetch(
        "/api/amy/command",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: text,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result?.error?.message ||
            "Backend rejected the command."
        );
      }

      /*
       * Backend returns:
       *
       * data.intent
       * data.task_id
       * data.status
       */

      const backendIntent =
        result?.data?.intent || "GENERAL";

      const taskId =
        result?.data?.task_id || "unknown";

      /*
       * Convert backend intent into our
       * visual agent IDs.
       */
      const intentToAgent: Record<string, string> = {
        RESEARCH: "research",
        COMPETITOR_RESEARCH: "competitor",
        KEYWORD_RESEARCH: "keyword",
        CONTENT_GENERATION: "content",
        CREATIVE_GENERATION: "creative",
        LINKEDIN_PUBLISH: "linkedin",
        LINKEDIN_SCHEDULE: "linkedin",
      };

      const backendAgentId =
        intentToAgent[backendIntent] ||
        localAgentId;

      const backendAgent = agents.find(
        (agent) => agent.id === backendAgentId
      );

      setActiveAgent(backendAgentId);
      setSystemState("WORKING");

      setMessages((prev) => [
        ...prev,
        {
          sender: "amy",
          text:
            `${backendAgent?.name || "AMY"} Agent activated. ` +
            `Task ${taskId} is now running.`,
        },
      ]);

      setActivities((prev) => [
        {
          id: Date.now(),
          agent:
            backendAgent?.name || "AMY",
          text:
            `Backend accepted task ${taskId} ` +
            `(${backendIntent}).`,
          time: getTime(),
        },
        ...prev,
      ]);
    } catch (error) {
      console.error(
        "AMY backend error:",
        error
      );

      setSystemState("ERROR");
      setActiveAgent(null);

      setMessages((prev) => [
        ...prev,
        {
          sender: "amy",
          text:
            "I couldn't reach the AMY backend. " +
            "Please make sure the FastAPI server is running on port 8000.",
        },
      ]);

      setActivities((prev) => [
        {
          id: Date.now(),
          agent: "AMY",
          text: "Backend connection failed.",
          time: getTime(),
        },
        ...prev,
      ]);
    }
  };

  /*
   * Browser speech recognition
   *
   * Voice → text → runCommand()
   *
   * The backend receives the exact same command
   * as a typed command.
   */
  const startVoice = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Speech recognition is not supported in this browser."
      );
      return;
    }

    const recognition =
      new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => {
      setListening(true);

      setActivities((prev) => [
        {
          id: Date.now(),
          agent: "AMY",
          text: "Listening for your command...",
          time: getTime(),
        },
        ...prev,
      ]);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.onerror = (event: any) => {
      console.error(
        "Speech recognition error:",
        event
      );

      setListening(false);

      setMessages((prev) => [
        ...prev,
        {
          sender: "amy",
          text:
            "I couldn't understand the voice input. Please try again.",
        },
      ]);
    };

    recognition.onresult = (event: any) => {
      const spokenText =
        event.results?.[0]?.[0]?.transcript?.trim();

      if (!spokenText) {
        return;
      }

      setCommand(spokenText);

      // Important:
      // directly pass the speech result to runCommand
      // rather than waiting for React state to update.
      runCommand(spokenText);
    };

    recognition.start();
  };

  return (
    <main className="amy-shell">
      <div className="noise" />
      <div className="grid-background" />

      {/* =========================
          TOP BAR
      ========================= */}

      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">
            A
          </div>

          <div>
            <div className="brand-name">
              CTons AMY
            </div>

            <div className="brand-subtitle">
              Autonomous Intelligence Workspace
            </div>
          </div>
        </div>

        <div className="topbar-center">
          <div className="system-pill">
            <span className="status-dot" />
            SYSTEM ONLINE
          </div>
        </div>

        <div className="topbar-right">
          <div className="metric">
            <span>AGENTS</span>
            <strong>06</strong>
          </div>

          <div className="metric">
            <span>TASK</span>
            <strong>{systemState}</strong>
          </div>

          <button className="icon-button">
            ⚙
          </button>
        </div>
      </header>

      {/* =========================
          WORKSPACE
      ========================= */}

      <section className="workspace">

        {/* =========================
            LEFT SIDEBAR
        ========================= */}

        <aside className="sidebar panel">

          <div className="panel-heading">
            <span>AGENT NETWORK</span>
            <span className="mini-live">
              LIVE
            </span>
          </div>

          <div className="agent-list">
            {agents.map((agent) => {
              const active =
                activeAgent === agent.id;

              return (
                <button
                  key={agent.id}
                  className={`agent-list-item ${
                    active ? "selected" : ""
                  }`}
                  onClick={() =>
                    runCommand(
                      `Activate ${agent.name} agent`
                    )
                  }
                >
                  <div
                    className={`agent-icon ${
                      active ? "active" : ""
                    }`}
                  >
                    {agent.icon}
                  </div>

                  <div className="agent-list-copy">
                    <strong>
                      {agent.name}
                    </strong>

                    <span>
                      {active
                        ? "Working now..."
                        : agent.role}
                    </span>
                  </div>

                  <span
                    className={`agent-state ${
                      active ? "working" : ""
                    }`}
                  >
                    {active ? "●" : "○"}
                  </span>
                </button>
              );
            })}
          </div>

          <div className="sidebar-footer">
            <div className="footer-line">
              <span>
                Voice interface
              </span>

              <span className="on">
                ON
              </span>
            </div>

            <div className="footer-line">
              <span>
                Wake word
              </span>

              <span>
                READY
              </span>
            </div>
          </div>
        </aside>

        {/* =========================
            CENTER STAGE
        ========================= */}

        <section className="center-stage">

          <div className="stage-header">
            <div>
              <div className="eyebrow">
                COMMAND CENTER
              </div>

              <h1>
                Agent Workspace
              </h1>
            </div>

            <div className="stage-status">
              <span className="pulse-ring" />

              {activeAgentInfo
                ? `${activeAgentInfo.name.toUpperCase()} ACTIVE`
                : "AWAITING COMMAND"}
            </div>
          </div>

          {/* =========================
              AGENT WORLD
          ========================= */}

          <div className="agent-world">

            <div className="orbit orbit-1" />
            <div className="orbit orbit-2" />
            <div className="orbit orbit-3" />

            <div className="connection connection-1" />
            <div className="connection connection-2" />
            <div className="connection connection-3" />
            <div className="connection connection-4" />
            <div className="connection connection-5" />
            <div className="connection connection-6" />

            {/* AMY CORE */}

            <div
              className={`amy-core ${
                activeAgent
                  ? "core-working"
                  : ""
              }`}
            >
              <div className="core-glow" />

              <div className="core-inner">
                <span>
                  AMY
                </span>

                <small>
                  {systemState}
                </small>
              </div>
            </div>

            {/* AGENT NODES */}

            {agents.map((agent) => {
              const active =
                activeAgent === agent.id;

              return (
                <div
                  key={agent.id}
                  className={`agent-node node-${agent.position} ${
                    active
                      ? "node-active"
                      : ""
                  }`}
                  onClick={() =>
                    runCommand(
                      `Activate ${agent.name} agent`
                    )
                  }
                >
                  <div className="node-circle">
                    <span>
                      {agent.icon}
                    </span>
                  </div>

                  <div className="node-label">
                    <strong>
                      {agent.name}
                    </strong>

                    <span>
                      {active
                        ? "WORKING"
                        : "IDLE"}
                    </span>
                  </div>
                </div>
              );
            })}

            <div className="world-scan" />
          </div>

          {/* =========================
              LIVE ACTIVITY
          ========================= */}

          <div className="activity-panel panel">

            <div className="panel-heading">
              <span>
                LIVE ACTIVITY
              </span>

              <span>
                {activities.length} EVENTS
              </span>
            </div>

            <div className="activity-feed">
              {activities
                .slice(0, 6)
                .map((activity) => (
                  <div
                    className="activity-row"
                    key={activity.id}
                  >
                    <span className="activity-indicator" />

                    <div className="activity-copy">
                      <strong>
                        {activity.agent}
                      </strong>

                      <span>
                        {activity.text}
                      </span>
                    </div>

                    <time>
                      {activity.time}
                    </time>
                  </div>
                ))}
            </div>
          </div>
        </section>

        {/* =========================
            RIGHT AMY CHAT
        ========================= */}

        <aside className="chat-panel panel">

          <div className="chat-header">
            <div>
              <div className="eyebrow">
                ASSISTANT
              </div>

              <h2>
                AMY
              </h2>
            </div>

            <div className="chat-online">
              <span className="status-dot" />
              ONLINE
            </div>
          </div>

          <div className="chat-messages">
            {messages.map(
              (message, index) => (
                <div
                  key={index}
                  className={`message-row ${
                    message.sender === "user"
                      ? "user-row"
                      : ""
                  }`}
                >
                  <div
                    className={`message ${
                      message.sender === "user"
                        ? "user-message"
                        : ""
                    }`}
                  >
                    {message.text}
                  </div>
                </div>
              )
            )}
          </div>

          {/* QUICK COMMANDS */}

          <div className="suggestions">

            <button
              onClick={() =>
                runCommand(
                  "Research AI trends on LinkedIn"
                )
              }
            >
              Research trends
            </button>

            <button
              onClick={() =>
                runCommand(
                  "Find competitor posts"
                )
              }
            >
              Analyze competitors
            </button>

            <button
              onClick={() =>
                runCommand(
                  "Create a LinkedIn post"
                )
              }
            >
              Create content
            </button>

          </div>

          {/* COMMAND BOX */}

          <div className="command-box">

            <textarea
              value={command}
              onChange={(event) =>
                setCommand(event.target.value)
              }
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !event.shiftKey
                ) {
                  event.preventDefault();

                  runCommand();
                }
              }}
              placeholder="Tell AMY what to do..."
              rows={3}
            />

            <div className="command-actions">

              <button
                className={`mic-button ${
                  listening
                    ? "listening"
                    : ""
                }`}
                onClick={startVoice}
                title="Voice command"
              >
                {listening
                  ? "◉"
                  : "🎙"}
              </button>

              <button
                className="send-button"
                onClick={() =>
                  runCommand()
                }
              >
                SEND ↗
              </button>

            </div>
          </div>
        </aside>
      </section>

      {/* =========================
          BOTTOM BAR
      ========================= */}

      <footer className="bottom-bar">

        <div>
          <span className="status-dot" />
          AMY CORE
        </div>

        <div>
          {listening
            ? "LISTENING..."
            : "VOICE READY"}
        </div>

        <div>
          ACTIVE AGENT:{" "}
          <strong>
            {activeAgentInfo?.name ||
              "NONE"}
          </strong>
        </div>

      </footer>
    </main>
  );
}

export default App;