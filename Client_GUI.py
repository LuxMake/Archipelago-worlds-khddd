from kivy.uix.scrollview import ScrollView

from kvui import GameManager

class KHDDDManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago")
    ]
    base_title = "Archipelago KHDDD Client"

    def build(self):
        layout = super().build()
        return layout
