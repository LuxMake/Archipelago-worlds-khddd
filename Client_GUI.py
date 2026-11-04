from kivy.uix.scrollview import ScrollView

from kvui import GameManager

from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField

from BaseClasses import ItemClassification

from .Items import SPIRITLIST
from .Locations import get_location_id, location_name_groups

class KHDDDManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago")
    ]
    base_title = "Archipelago KHDDD Client"



    def build(self):
        layout = super().build()
        return layout


LINK_BOARD_MAP = "Link Boards"
BOARD_LOCATIONS = {spirit: [get_location_id(name) for name in location_name_groups[spirit+" Ability Link"]] for spirit in SPIRITLIST}

Builder.load_string("""
<KHDDDLinkBoardSearch>:
    size_hint: None, None
    size: (self.minimum_width, dp(40)) if self.shown else (0, 0)
    opacity: 1 if self.shown else 0
    disabled: not self.shown
    pos_hint: {"center_y": 0.5}
    spacing: dp(4)
    KHDDDSearchField:
        id: query
        mode: "outlined"
        size_hint: None, None
        -width: dp(150)
        -height: dp(32)
        pos_hint: {"center_y": 0.5}
        MDTextFieldHintText:
            text: "Spirit or item"
    MDCheckbox:
        id: progression
        size_hint: None, None
        size: dp(32), dp(32)
        pos_hint: {"center_y": 0.5}
    MDLabel:
        adaptive_size: True
        pos_hint: {"center_y": 0.5}
        text: "Progression"
""")

class KHDDDSearchField(MDTextField):
    """Override the static position of the hint text, surprised no one else has done this yet"""
    def set_pos_hint_text(self, y: float, x: float) -> None:
        super().set_pos_hint_text(y + (dp(56) - self.height) / 2, x)


class KHDDDLinkBoardSearch(BoxLayout):
    shown = BooleanProperty(False)


class LinkBoardSearch:
    """Search bar in UT's map header that hides Link Boards markers whose spirit and scouted items don't match."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.bar = None
        self.hidden_markers = {}

    def on_tracker_update(self, _in_logic: list[str]) -> bool:
        """Runs from UT's updateTracker, which follows every map switch once the new markers exist."""
        if self.bar is None and self.ctx.map_page is not None:
            self.bar = KHDDDLinkBoardSearch()
            self.bar.ids.query.bind(text=lambda *_: self.refresh())
            self.bar.ids.progression.bind(active=lambda *_: self.refresh())
            self.ctx.map_page.ids.map_list.parent.add_widget(self.bar)
        self.refresh()
        return True

    def refresh(self):
        if self.bar is None:
            return
        self.bar.shown = self.ctx.ui.current_map == LINK_BOARD_MAP
        query = self.bar.ids.query.text.strip().casefold() if self.bar.shown else ""
        progression_only = self.bar.shown and self.bar.ids.progression.active
        #load_map replaces every marker
        self.hidden_markers = {marker: size for marker, size in self.hidden_markers.items() if marker.parent}
        for spirit, locations in BOARD_LOCATIONS.items():
            show = self._matches(spirit, locations, query, progression_only)
            for location in locations:
                for marker in self.ctx.coord_dict.get(location, []):
                    self._show_marker(marker, show)

    def _matches(self, spirit: str, locations: list[int], query: str, progression_only: bool) -> bool:
        scouted = [self.ctx.locations_info[location] for location in locations if location in self.ctx.locations_info]
        if progression_only and not any(item.flags & ItemClassification.progression and item.location not in self.ctx.checked_locations
                                        for item in scouted):
            return False
        return query in spirit.casefold() or any(query in self.ctx.item_names.lookup_in_slot(item.item, item.player).casefold() for item in scouted)

    def _show_marker(self, marker, show: bool):
        if show and marker in self.hidden_markers:
            marker.size = self.hidden_markers.pop(marker)
            marker.opacity = 1
        elif not show and marker not in self.hidden_markers:
            self.hidden_markers[marker] = tuple(marker.size)
            marker.size = (0, 0) #A zero size also stops the hover tooltip
            marker.opacity = 0
