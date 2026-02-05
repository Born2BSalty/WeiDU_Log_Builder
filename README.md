———

  # WeiDU Log Builder (WLB)

  A Windows‑first (cross‑platform) 5‑step desktop wizard for WeiDU modding. It scans a mods folder, shows components, helps
  build a valid install order, exports weidu.log, and runs installs through mod_installer with an interactive console.

  Quick Start

  1. Install Python 3.12+
  2. Install uv: pip install uv
  3. Set up deps: uv sync --dev
  4. Run: uv run wlb

  What It Does

  - Lets you select components and reorder them.
  - Exports weidu.log from your selected order.


  1. Setup
      - Pick game (BGEE/BG2EE/EET)
      - Mods folder
      - WeiDU.exe path
      - Mod_Installer.exe path
      - Game folder and WeiDU log folder/file paths
      - Scan mods folder
      - Rules and checks shown in details panel
  3. Reorder Components
      - Drag and drop to set install order
  4. Preview & Export
      - Save weidu.log
  5. Installation & Progress
      - Start install
      - Interactive console (type directly in the console)
  Compatibility Rules (optional)
  Edit config/compat_rules.yaml to grey out or flag components.
  Example:

  #   component: "Ice Island Level Two Restoration"
  #   tab: ["bgee"]            # or ["bg2ee"] or ["bgee","bg2ee"]
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
  For a more CMD‑like interactive console on Windows, bundle WinPTY:

  WLB/bin/winpty/winpty.dll
  If WinPTY is present, WLB uses it automatically.


  - Lint: uv run ruff check src
  - Format: uv run ruff format src
  - Type check: uv run mypy src/wlb/infra src/wlb/services
  Project Layout
  - src/wlb/ui/ UI (Qt)
  - src/wlb/services/ app logic
  - src/wlb/infra/ IO + external processes
  - src/wlb/domain/ pure models
  ———