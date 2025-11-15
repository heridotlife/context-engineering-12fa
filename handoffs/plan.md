# Execution Plan

**Prepared By**: GPT-5 Codex
**Context Snapshot Timestamp**: 2025-11-10T00:00:00Z

## Persona Alignment
- Persona selected: context-manager
- Rationale: Keeps the planning focused on orchestrating multi-agent handoffs, tooling setup, and documentation while delegating hands-on coding to Claude.

## Plan Overview
1. Scaffold a new Astro project in `projects/astro-mdx-blog` with MDX support and TypeScript baseline (owner: Claude).
2. Implement content collections for blog posts and presentations, including tagging and routes (`/blog`, `/presentations`, `/tags/[tag]`) (owner: Claude).
3. Add speaker mode support for presentation MDX (likely via `@astrojs/mdx` with remark/rehype plugins or a custom layout) (owner: Claude).
4. Configure UI components/layouts for blog and slides, ensuring simple navigation and shared styling (owner: Claude).
5. Set up linting, type checking, Playwright tests, and CI scripts (`npm run lint`, `npm run check`, `npm run build`, `npm run test:e2e`) (owner: Claude).
6. Document Cloudflare Pages deployment steps and add project README + deployment config (owner: Claude).
7. Run validation commands locally (lint, typecheck, build, Playwright) and capture results (owner: Claude).

## Context Bundle Summary
- Key files to review/edit: `package.json`, `astro.config.mjs`, `src/content`, `src/pages`, `src/layouts`, `playwright.config.ts`, `package.json` scripts.
- Commands to run:
  - `npm create astro@latest projects/astro-mdx-blog -- --template default --no-install`
  - `npm install` with necessary deps (MDX, Cloudflare adapter, testing tools).
  - `npm run lint`
  - `npm run check`
  - `npm run build`
  - `npm run test:e2e`
- External references: Astro MDX docs, Cloudflare Pages deployment guide, Playwright setup instructions.

## Guardrails & Safety Checks
- Keep dependency list minimal; prefer official Astro integrations.
- Ensure Playwright tests do not rely on external network calls.
- Document any manual Cloudflare configuration required; no secrets committed.
- Maintain ASCII-only files unless dependencies require otherwise.

## Handoff Notes
- Outstanding questions for Claude: choose a lightweight speaker mode approach (e.g., `astro-presentation` layout) and confirm compatibility with MDX.
- Follow-up expectations for User: review the generated project, adjust design preferences, and initiate Cloudflare deployment using documented steps.
