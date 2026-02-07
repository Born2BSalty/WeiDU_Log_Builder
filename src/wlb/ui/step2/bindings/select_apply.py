from __future__ import annotations

from wlb.domain.models import ModInfo
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.bindings.mods_apply_models import build_game_models
from wlb.ui.step2.bindings.select_binding import wire_model
from wlb.ui.step2.compat.select_missing import MissingFilesReporter
from wlb.ui.step2.models.display_names import display_mod_name
from wlb.ui.step2.models.selection_store import SelectionOrderStore
from wlb.ui.step2.views.select_layout import SelectionUi


def apply_mods(
    ui: SelectionUi,
    mods: list[ModInfo],
    store: SelectionOrderStore,
    settings: SettingsService,
    reporter: MissingFilesReporter | None = None,
) -> None:
    mods = sorted(mods, key=lambda mod: display_mod_name(mod.name).lower())
    bgee_model, bg2ee_model = build_game_models(mods, settings)
    wire_model(
        ui.bgee_view,
        bgee_model,
        ui.details_desc,
        ui.details_mod_id,
        ui.details_component,
        ui.details_version,
        ui.details_path,
        ui.details_author,
        ui.details_readme,
        ui.details_name,
        store,
        "BGEE",
        reporter.for_item if reporter is not None else None,
    )
    wire_model(
        ui.bg2ee_view,
        bg2ee_model,
        ui.details_desc,
        ui.details_mod_id,
        ui.details_component,
        ui.details_version,
        ui.details_path,
        ui.details_author,
        ui.details_readme,
        ui.details_name,
        store,
        "BG2EE",
        reporter.for_item if reporter is not None else None,
    )
