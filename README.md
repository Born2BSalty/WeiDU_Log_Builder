———

  # WeiDU Log Builder (WLB)

 A Windows‑first (cross‑platform) 5‑step desktop wizard for WeiDU modding. It scans a mods folder, shows
  components, helps
  build a valid install order, exports weidu.log, and runs installs through mod_installer with an interactive


  1. Install Python 3.12+
  3. In `D:\Modding\WLB\dev`:
  5. Run: `uv run wlb`

  Release (End Users)

  Use `D:\Modding\WLB\release\dist\WLB\WLB.exe`.
  What It Does

  - Step 1: Setup
  - Step 2: Scan & Select Components
  - Step 3: Reorder Components
  - Step 4: Preview & Export
  - Step 5: Installation & Progress
  Compatibility Rules (optional)

  Edit:
  `D:\Modding\WLB\dev\config\compat_rules.yaml`

  Example:

  # - mod: "bg1ub"
  #   component: "Ice Island Level Two Restoration"
  #   tab: ["bgee"]
  #   issue: "included"
  #   message: "Already included in BG:EE v2.5+."

  Rule fields:
  - mod (required): mod header name or TP2 name
  - component_id (optional): component number
  - tab (optional): which tab(s) to apply to
  - mode (optional): game selection filter (BGEE/BG2EE/EET)
  - min_tab_version (optional): only apply if game version >= value
  - issue / kind: included, not_needed, not_compatible, warning, conflict

  Windows Terminal (optional)

  If WinPTY exists here, WLB uses it automatically:
  `D:\Modding\WLB\dev\bin\winpty\`

  Checks

  - Lint: `uv run ruff check src`
  - Format: `uv run ruff format src`
  - Type check: `uv run mypy src/wlb/infra src/wlb/services`

  Project Layout

  - `dev/src/wlb/ui/` UI (Qt)
  - `dev/src/wlb/services/` app logic
  - `dev/src/wlb/infra/` IO + external processes
  - `dev/src/wlb/domain/` pure models
  - `release/dist/WLB/` packaged app
  ———