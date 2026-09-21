# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
[markdownlint](https://dlaa.me/markdownlint/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.3] - 2026-09-21

The first release of the Senzing Bootcamp ChatGPT plugin, built from
[Senzing Bootcamp Claude plugin 0.5.3][template 0.5.3] for the Codex host. Seventeen skills,
eight lifecycle hooks and nineteen helper scripts.

### Added

- **The guided bootcamp, in Codex.** The `senzing-bootcamp` plugin ships seventeen skills
  covering bootcamp preparation, an entity-resolution primer, the business problem, SDK
  setup, system verification, Truth Set visualization, data collection, data quality and
  mapping, data processing, query/visualize/discover, and graduation. Install the
  marketplace, then say "Start the Senzing Bootcamp". You finish with working Senzing code
  and data in your project, a recap PDF you can keep and share, and a `production/` starter.
- **A Codex interaction contract that keeps the Socratic rhythm.** Codex separates
  intermediate commentary from the final response, and commentary is a progress update, not
  a turn boundary. `docs/codex-interaction-contract.md` states the rule and the turn-close
  audit that enforces it: a turn ends on exactly one 👉 question copied from the active
  shipped skill, with nothing after it, and a status-only final response is a violation.
- **Lifecycle hooks, discovered from `hooks/hooks.json`.** `UserPromptSubmit` rehydrates the
  active module on every answer and `Stop` keeps a status-only response from ending the turn
  — together they restore the persistent controller a Socratic workflow needs. The rest
  provide resume, recap checkpointing, write safety, feedback capture, compaction and
  session-end behavior. Every hook no-ops unless `config/bootcamp_progress.json` exists in
  the working directory, so the plugin never alters an unrelated Codex session. Codex asks
  you to review and trust non-managed plugin hooks before they run; decline and the skill
  instructions remain a best-effort fallback, with the progress file as the source of truth.
- **Take a note, at any point in the bootcamp.** A `bootcamp-note` skill captures an idea, a
  question, a reminder or a to-do to `docs/bootcamp_notes.md`. Say "take a Senzing bootcamp
  note". Written into your project and sent nowhere.
- **Package the bootcamp into one file.** A `package-bootcamp` skill collects the bootcamp
  into a single transferable zip under `backups/packages/`, so a bootcamp can move between
  machines or be handed to a colleague. Two profiles: `share` carries the results — recap
  PDF, keepsake documents, visualizations and `production/` — with no database, no source
  data and no credentials; `transfer` adds the revisit bundle, config and mappings so the
  bootcamp can be resumed elsewhere. The dry run comes first, so the one 👉 question quotes a
  measured size rather than an estimate. The plugin writes the archive and stops: it never
  uploads, emails or attaches it. The archive carries an `OPEN_ME_FIRST.md` and a
  `PACKAGE_MANIFEST.json` naming every included path with its SHA-256 and every path
  skipped, so a recipient can tell what is missing without guessing.
- **A database backup you can come back to.** Graduation writes a revisit bundle of the
  resolved repository, so the entity-resolution results outlive the bootcamp session. One
  shared procedure (`skills/graduation/database-backup.md`) serves both graduation and the
  packaging flow, handles SQLite and PostgreSQL, and refuses to guess when the database type
  is indeterminate rather than aiming `pg_dump` at a SQLite file.
- **One definition of what counts as a secret.** `scripts/secret_patterns.py` — a PEM private
  key, an AWS access-key ID, a Senzing license payload. The write gate blocks a *write* that
  matches; the packager excludes a *member* that matches, so a pattern added for one is
  available to the other. The gate keeps its own inline copy on purpose: an `ImportError` in
  a `PreToolUse` control must not degrade to "no secret scan".
- Nineteen bundled Python helper scripts, a vendored D3 build for the offline visualization,
  the Senzing brand assets the visual deliverables carry, and an example recap PDF with its
  thirteen rendered visualizations under `docs/examples/`.
- `.mcp.json` declaring the [Senzing MCP server]. The bootcamp cannot proceed without network
  access to it: it generates SDK code, looks up Senzing facts, and supplies working examples.
- `docs/model-selection.md` and `docs/codex-port.md`. Model names and controls are
  host-specific and change over time, so the plugin recommends a capable Codex model and
  medium-or-higher reasoning effort for long modules, and never claims to have changed the
  bootcamper's model or reasoning setting itself.
- Repository infrastructure: GitHub Actions workflows, Dependabot, linter and spellcheck
  configuration, and `CODEOWNERS`, matching `senzing-bootcamp-kiro-power` (which tracks the
  `senzing-garage/template-python` workflow set).
- Community health files from `senzing-garage/template-python`, adapted to the `Senzing`
  organization: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and the contributor license
  agreements.

[Senzing MCP server]: https://mcp.senzing.com/mcp
[template 0.5.3]: https://github.com/Senzing/senzing-bootcamp-claude-plugin/releases/tag/0.5.3
