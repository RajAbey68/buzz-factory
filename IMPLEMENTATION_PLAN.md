# Implementation Plan — "Buzz-style" Open Agentic Team Chat

> Inspired by Jack Dorsey / Block's **Buzz** (walkthrough: YouTube `_jGSgzBkzrY`).
> Goal: a self-hostable, open-source, **Nostr**-based team-chat where AI agents are
> first-class members, harness-swappable, Git-integrated, and compute-portable.
> Methodology: BMAD (Analyst → PM → Architect → PO → Scrum Master → Dev → QA).
> Owner stack default: React 19 + TS + Vite + Tailwind + shadcn/ui; Supabase where a
> central store helps; Nostr relay for the chat fabric; Ollama/Codex/Claude Code for harness.

---

## 0. Analyst Brief (why this exists)

Buzz demonstrates the "future of work" pattern: a chat surface where humans and agents
share one persistent **context engine**, and software gets built/deployed on the fly.
Key differentiators called out in the video:

| Capability | What it does | Why it matters |
|---|---|---|
| Agents as first-class citizens | Agents are team members, not add-ons | Context + tasks live in one place |
| Swappable harness | Swap Claude Code/Codex/Goose/OpenCode/Hermes; context carries over | No model lock-in; beat "model fatigue" |
| Git-native | Feature branches, parallel worktrees, deploy-to-live (Railway etc.) | Software built in-chat, shipped immediately |
| Open protocol (Nostr) | Relays store/route all events; portable | Escape Slack-style data lock-in |
| Shared compute | Download local LLMs, share across team | Cost control + local-model choice |
| Audio huddles | Voice chat with agents, full chat context | Live creative collaboration |
| Workflows/loops | Recurring agent tasks reading external APIs → channel | "Closing the context loop" |
| Lightning backdoor | Bitcoin/Lightning micropayments (not yet live) | Pay agents/people for work |

**Opportunity for us:** Buzz is alpha, Block-hosted, proprietary-relay-optional. Building
our own on the *same open protocol* gives us Buzz's model with **data sovereignty** and
direct fit into the existing Agent-First fleet (Hermes, devserver Ollama `gemma3:4b`,
n8n, Hetzner worker). This is "Agent First, owned infra" incarnate.

**Tier-one source note (P1):** Protocol specifics (Nostr NIPs, relay behavior) MUST be
verified against nostr.com NIP registry before Phase 1 coding. Video is a secondary
narrative source, not a spec.

---

## 1. Product Requirements (PM)

### Personas
- **Solopreneur / small-team founder** — wants to brainstorm, build, deploy fast.
- **Agent operator** — configures harnesses, pins models, authors system prompts.
- **Community member** — joins public channels, files bugs that become agent tasks.

### Functional Requirements
- FR1. Public & private channels; invite via Nostr pubkey.
- FR2. Agents appear in member roster with avatar/status; `@mention` triggers them.
- FR3. Harness adapter interface; ≥3 harnesses at launch (Ollama-local, Claude Code, Codex).
- FR4. Context preservation across harness/model swap (chat history replayed).
- FR5. Per-agent config: name, harness, model pin, system prompt, skills dir, role.
- FR6. "Chief Agent Officer" meta-agent routes a task to the best agent.
- FR7. Git integration: create project, feature branch, parallel worktree, commit, open PR.
- FR8. Deploy hook: push built app to a host (Railway/Vercel/own) + post preview+screenshot.
- FR9. Workflows: scheduled agent task that reads an external API → posts to channel.
- FR10. Shared compute: advertise a local Ollama endpoint to the team over the relay.
- FR11. (Future) Audio huddle: WebRTC + STT + agent TTS with full chat context.
- FR12. (Future) Lightning payments via Nostr Wallet Connect.

### Non-Functional Requirements
- NFR1. All chat events flow through a self-hosted Nostr relay (data sovereignty).
- NFR2. Private channel content encrypted (NIP-44) — relay cannot read it.
- NFR3. TDD: every adapter and service has failing test before impl (P4).
- NFR4. Four-eyes: no merge without independent non-Anthropic reviewer (P3).
- NFR5. RLS on any Supabase table; secrets in env/Edge config only (CLAUDE.md security).
- NFR6. Latency: agent turn < ~10s median for local harness; < ~30s for remote.

### Success Metrics
- A user can: create channel → `@agent` build a CRM → see it deployed live → `@agent` fix a bug, in one session.
- Context survives a harness swap with zero re-prompting.
- ≥3 team members sharing one local Ollama endpoint via shared compute.

---

## 2. Architecture (Architect)

```
┌─────────────────────────────────────────────────────────────┐
│  Client (React 19 + Vite + Tailwind + shadcn/ui)             │
│  Channels • Agent roster • Settings (harness/model/compute)   │
└───────────────┬───────────────────────────┬──────────────────┘
                │ nostr-tools (WS)          │ REST/WS
                ▼                            ▼
        ┌───────────────┐          ┌──────────────────────────┐
        │ Self-hosted   │          │ Agent Gateway (Node/TS)  │
        │ Nostr Relay   │◄─────────│ subscribes to @agent msgs│
        │ (strfry/rs)   │  events  │ routes → HarnessAdapter  │
        └───────────────┘          └───────────┬──────────────┘
                                               │ adapter interface
                ┌──────────────────────────────┼──────────────────────────┐
                ▼                              ▼                          ▼
        ┌──────────────┐            ┌──────────────────┐        ┌──────────────────┐
        │ Ollama       │            │ Claude Code /    │        │ Codex / Goose /  │
        │ (devserver)  │            │ Codex CLI        │        │ OpenCode / Hermes│
        │ shared compute│           │ (subprocess)     │        │ (subprocess)     │
        └──────────────┘            └──────────────────┘        └──────────────────┘
                │                                                   │
                └───────────────► Git worktrees / Gitea / GitHub ───┘
                                      │
                                      ▼
                              Deploy (Railway/Vercel/own) + screenshot → channel
```

### Core interfaces
```ts
// Harness adapter — the swappable core
interface HarnessAdapter {
  id: 'ollama' | 'claude-code' | 'codex' | 'goose' | 'opencode' | 'hermes';
  run(req: AgentRequest): AsyncIterable<AgentEvent>; // streamed
}
interface AgentRequest {
  agent: AgentConfig;            // name, model pin, systemPrompt, skills
  messages: ChatMessage[];       // full history → context carry-over
  tools?: ToolSpec[];            // git, deploy, web, etc.
}
interface AgentConfig {
  name: string; harness: HarnessId; model?: string;
  systemPrompt: string; skillsDir?: string; role?: string;
}
```

### Data / protocol
- Nostr events for: channel create (NIP-29 group / custom), message, agent status, deploy result.
- Encrypted content via NIP-44 for private channels.
- Agent registry: versioned YAML/JSON in repo (git-backed, portable) — satisfies "local, git-backed state".
- Optional Supabase: agent memory/embeddings (pgvector) for long-term context recall.

### Reuse of existing fleet
- **devserver** (Hostinger): Nostr relay + Ollama `gemma3:4b` (already running) as shared compute.
- **hermes-dev** (Hetzner): Agent Gateway service + cron for workflows.
- **n8n** (devserver): workflow orchestration where it fits.
- **Hermes** itself: a harness adapter (it's already an agent runtime).

---

## 3. Epics & Stories (PO)

**E1 — Foundations**
- E1.1 Stand up self-hosted Nostr relay on devserver (Docker, strfry).
- E1.2 Nostr client wrapper (connect, publish, subscribe, encrypt).
- E1.3 Repo scaffold (Vite React app + Node gateway), CI, Linear project.

**E2 — Chat Core**
- E2.1 Channel list + public/private channels (NIP-29 + NIP-44).
- E2.2 Message composer, live timeline, mentions.
- E2.3 Agent presence: agents rendered as members with status.

**E3 — Harness Abstraction**
- E3.1 Define `HarnessAdapter` interface + streaming protocol.
- E3.2 Ollama adapter (devserver endpoint).
- E3.3 Claude Code adapter (subprocess, streamed).
- E3.4 Context carry-over: replay `messages` on harness swap; verify no re-prompt needed.

**E4 — Agent Registry & Routing**
- E4.1 Agent config schema + UI editor (name, harness, model pin, system prompt, skills).
- E4.2 Skills dir wiring (global skills accessible to agents).
- E4.3 Chief Agent Officer meta-agent (route task → best agent).

**E5 — Git & Projects**
- E5.1 Agent creates project + feature branch + parallel worktree.
- E5.2 Commit + open PR (GitHub or self-hosted Gitea relay-hosted git).
- E5.3 Deploy hook → host + screenshot → post to channel.
- E5.4 Projects view (toggle in settings/experiments).

**E6 — Workflows & Shared Compute**
- E6.1 Scheduled workflow: external API → agent → channel post.
- E6.2 Shared compute: advertise Ollama endpoint; team agents route local tasks there.

**E7 — Future / Optional**
- E7.1 Audio huddles (WebRTC + STT + TTS).
- E7.2 Lightning payments (Nostr Wallet Connect).

---

## 4. Roadmap (Sprints)

| Sprint | Epic | Exit criteria |
|---|---|---|
| S0 | E1 | Relay up; client connects; repo + Linear live |
| S1 | E2 | Two humans + one agent chat in a private channel |
| S2 | E3 | `@agent` works on Ollama + Claude Code; harness swap keeps context |
| S3 | E4 | Configure 3 agents; CAO routes a task correctly |
| S4 | E5 | `@agent build CRM → deploy → screenshot in channel` |
| S5 | E6 | Daily workflow posts; 2 members share Ollama |

---

## 5. Tech Decisions & Risks

- **Protocol = Nostr** (confirmed open in video). *Risk:* relay QoS/scale — mitigate with strfry + vertical scaling on devserver.
- **Relay hosting = devserver** (2CPU/3.7GB). *Risk:* relay + Ollama contention — cap Ollama, monitor disk (existing 15-min disk cron).
- **Local-first harness = Ollama `gemma3:4b`** already live; Claude Code/Codex for heavy lifts.
- **Secrets:** relay keys, API keys in env/Edge config; never in code (CLAUDE.md).
- **Budget (P1):** synthesizer = Anthropic; checkers/reviewers = DeepSeek/GLM/Gemini (free models). No Anthropic for review loops.
- **Verification (P4/P3):** TDD red-green; four-eyes via independent non-Anthropic LLM review before merge.

---

## 6. Verification Plan (QA)

- Unit: each adapter parses `AgentRequest` → emits valid `AgentEvent` stream (failing test first).
- Integration: spin a test relay; simulate `@agent` mention → assert agent reply event published.
- Context test: swap harness mid-conversation; assert downstream agent received full `messages`.
- E2E: scripted "build + deploy + fix" flow posts screenshot to channel.
- Four-eyes gate: every PR gets an independent non-Anthropic model review before merge.

---

## 7. Open Questions (resolve before S0 ends)
1. Confirm scope: open clone (this plan) vs. adopt Buzz vs. Hermes-only integration.
2. Relay choice: strfry vs nostr-rs-relay (perf/ops trade-off).
3. GitHub vs self-hosted Gitea for "relay-hosted git" (video implies Block hosts git on relay).
4. Supabase needed at all, or pure Nostr + local state sufficient for v1?
