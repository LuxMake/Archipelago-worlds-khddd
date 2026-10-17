from typing import Callable, TYPE_CHECKING, Any, override

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, add_item_rule
from BaseClasses import ItemClassification

from .Locations import KHDDDLocation, location_data_table, location_name_groups
from .Items import get_items_by_category, SPIRITLIST

from rule_builder.rules import Rule, HasAny, Has, CanReachLocation, HasAllCounts, HasAll, AtLeast, HasGroupUnique, HasFromListUnique

if TYPE_CHECKING:
    from . import KHDDDWorld

SORA_WORLDS = ["Traverse Town [Sora]", "La Cite des Cloches [Sora]", "The Grid [Sora]", "Prankster's Paradise [Sora]", "Country of the Musketeers [Sora]", "Symphony of Sorcery [Sora]"]
RIKU_WORLDS = ["Traverse Town [Riku]", "La Cite des Cloches [Riku]", "The Grid [Riku]", "Prankster's Paradise [Riku]", "Country of the Musketeers [Riku]", "Symphony of Sorcery [Riku]"]

SORA_COMPLETION_LOCS = ["Traverse Town Skull Noise Reward [Sora]", "La Cite des Cloches Guardian Bell Reward [Sora]", "The Grid Dual Disc Reward [Sora]",
                        "Prankster's Paradise Ferris Gear Reward [Sora]", "Country of the Musketeers All For One Reward [Sora]", "Symphony of Sorcery Counterpoint Reward [Sora]",
                        "The World That Never Was Xemnas Bonus Slot 1 [Sora]"]
RIKU_COMPLETION_LOCS = ["Traverse Town Skull Noise Reward [Riku]", "La Cite des Cloches Guardian Bell Reward [Riku]", "The Grid Dual Disc Reward [Riku]",
                        "Prankster's Paradise Ocean's Rage Reward [Riku]", "Country of the Musketeers All For One Reward [Riku]", "Symphony of Sorcery Counterpoint Reward [Riku]",
                        "The World That Never Was Ansem II Defeated [Riku]"]


def has_x_sora_worlds(num_of_worlds: int) -> Rule[Any]:
    return HasFromListUnique(*SORA_WORLDS, count=num_of_worlds)

def has_x_riku_worlds(num_of_worlds: int) -> Rule[Any]:
    return HasFromListUnique(*RIKU_WORLDS, count=num_of_worlds)

def beat_x_sora_worlds(num_of_worlds: int) -> Rule[Any]:
    return AtLeast(num_of_worlds, CanReachLocation("Traverse Town Skull Noise Reward [Sora]"), CanReachLocation("La Cite des Cloches Guardian Bell Reward [Sora]"),
                   CanReachLocation("The Grid Dual Disc Reward [Sora]"), CanReachLocation("Prankster's Paradise Ferris Gear Reward [Sora]"), CanReachLocation("Country of the Musketeers All For One Reward [Sora]"),
                   CanReachLocation("Symphony of Sorcery Counterpoint Reward [Sora]"), CanReachLocation("The World That Never Was Xemnas Bonus Slot 1 [Sora]"))

def beat_x_riku_worlds(num_of_worlds: int) -> Rule[Any]:
    return AtLeast(num_of_worlds, CanReachLocation("Traverse Town Skull Noise Reward [Riku]"), CanReachLocation("La Cite des Cloches Guardian Bell Reward [Riku]"),
                   CanReachLocation("The Grid Dual Disc Reward [Riku]"), CanReachLocation("Prankster's Paradise Ocean's Rage Reward [Riku]"), CanReachLocation("Country of the Musketeers All For One Reward [Riku]"),
                   CanReachLocation("Symphony of Sorcery Counterpoint Reward [Riku]"), CanReachLocation("The World That Never Was Ansem II Defeated [Riku]"))

def tt2_access_sora() -> Rule[Any]:
    return HasAllCounts({"Traverse Town [Sora]" : 2})

def tt2_access_riku() -> Rule[Any]:
    return HasAllCounts({"Traverse Town [Riku]" : 2})

def can_access_sora_portals() -> Rule[Any]:
    return AtLeast(6, CanReachLocation("Traverse Town Secret Portal [Sora]"), CanReachLocation("La Cite des Cloches Secret Portal [Sora]"), CanReachLocation("The Grid Secret Portal [Sora]"),
                          CanReachLocation("Country of the Musketeers Secret Portal [Sora]"), CanReachLocation("Prankster's Paradise Secret Portal [Sora]"), CanReachLocation("Symphony of Sorcery Secret Portal [Sora]"))

def can_access_riku_portals() -> Rule[Any]:
    return AtLeast(5, CanReachLocation("Traverse Town Secret Portal [Riku]"), CanReachLocation("La Cite des Cloches Secret Portal [Riku]"),
                   CanReachLocation("The Grid Secret Portal [Riku]"), CanReachLocation("Country of the Musketeers Secret Portal [Riku]"), CanReachLocation("Prankster's Paradise Secret Portal [Riku]"))

def has_required_recipes(num_of_recipes: int) -> Rule[Any]:
    return HasGroupUnique("Recipes", num_of_recipes)

def has_macguffins(num_of_recipes) -> Rule[Any]:
    return HasAll("Meow Wow Recipe", "Komory Bat Recipe", "Recusant Sigil") & has_required_recipes(num_of_recipes)

def can_infinite_jump() -> Rule[Any]:
    return HasAll("Wall Kick", "Super Jump") | Has("Flowmotion")

def can_glide() -> Rule[Any]:
    return HasAny("Glide", "Superglide") | Has("Flowmotion")

def can_pole_jump() -> Rule[Any]:
    return HasAll("Pole Swing", "Super Jump", "Air Slide") | HasAll("Flowmotion", "Air Slide")

#Region-specific helpers
def post_office_access() -> Rule[Any]:
    return HasAny("Wall Kick", "Glide", "Rail Slide") | Has("Flowmotion")

def set_rules(khdddworld):
    multiworld = khdddworld.multiworld
    player = khdddworld.player
    options = khdddworld.options

    #Make all Link Board nodes require base recipe
    for name, data in location_name_groups.items():
        spirit_name = name[:-13] #Trim " Ability Link"

        if SPIRITLIST[spirit_name] in khdddworld.ids_for_gates: #Only add rule for recipes in the pool
            for nodes in data:
                khdddworld.set_rule(khdddworld.get_location(nodes), Has(spirit_name+" Recipe"))


    #Ensure the player is not expected to level grind much for checks

    #Sora Level Rules
    if (options.character == 0 or options.character == 1) and options.stats_on_levels < 3:
        for num in range(2, 5):
            khdddworld.set_rule(khdddworld.get_location("Sora Level " + f"{num:02d}"), HasFromListUnique(*SORA_WORLDS, count=1))
        for num in range(6, 10):
            khdddworld.set_rule(khdddworld.get_location("Sora Level " + f"{num:02d}"), AtLeast(2, *[Has(world) for world in SORA_WORLDS]))
        for num in range(11, 15):
            khdddworld.set_rule(khdddworld.get_location("Sora Level " + f"{num:02d}"), HasFromListUnique(*SORA_WORLDS, count=3))
        for num in range(16, 20):
            khdddworld.set_rule(khdddworld.get_location("Sora Level " + str(num)), HasFromListUnique(*SORA_WORLDS, count=4))
        for num in range(21, 25):
            khdddworld.set_rule(khdddworld.get_location("Sora Level " + str(num)), HasFromListUnique(*SORA_WORLDS, count=5))
        for num in range(26, 99):
            khdddworld.set_rule(khdddworld.get_location("Sora Level "+ str(num)), HasFromListUnique(*SORA_WORLDS, count=6))


    # Riku Level Rules
    if (options.character == 0 or options.character == 2) and options.stats_on_levels < 3:
        for num in range(2, 5):
            khdddworld.set_rule(khdddworld.get_location("Riku Level " + f"{num:02d}"), has_x_riku_worlds(1))
        for num in range(6, 10):
            khdddworld.set_rule(khdddworld.get_location("Riku Level " + f"{num:02d}"), has_x_riku_worlds(2))
        for num in range(11, 15):
            khdddworld.set_rule(khdddworld.get_location("Riku Level " + f"{num:02d}"), has_x_riku_worlds(3))
        for num in range(16, 20):
            khdddworld.set_rule(khdddworld.get_location("Riku Level " + f"{num:02d}"), has_x_riku_worlds(4))
        for num in range(21, 25):
            khdddworld.set_rule(khdddworld.get_location("Riku Level " + f"{num:02d}"), has_x_riku_worlds(5))
        for num in range(26, 99):
            khdddworld.set_rule(khdddworld.get_location("Riku Level "+f"{num:02d}"), has_x_riku_worlds(6))

    ###############################
    #########SORA RULES############
    ###############################

    if options.character == 0 or options.character == 1:
        ###################################
        ############Superbosses############
        ###################################
        if options.superbosses or options.goal == 1:
            khdddworld.set_rule(khdddworld.get_location("Traverse Town Secret Portal [Sora]"),
                    has_x_sora_worlds(6) & (Has("High Jump") | can_infinite_jump()))
            khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Secret Portal [Sora]"),
                    has_x_sora_worlds(6))
            khdddworld.set_rule(khdddworld.get_location("The Grid Secret Portal [Sora]"),
                    has_x_sora_worlds(6))
            khdddworld.set_rule(khdddworld.get_location("Prankster's Paradise Secret Portal [Sora]"),
                    has_x_sora_worlds(6))
            khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Secret Portal [Sora]"),
                    has_x_sora_worlds(6))
            khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Secret Portal [Sora]"),
                    has_x_sora_worlds(6) & (Has("High Jump") | can_infinite_jump()))
            khdddworld.set_rule(khdddworld.get_location("Traverse Town 2 Ultima Weapon Reward [Sora]"),
                    can_access_sora_portals() & (
                         has_required_recipes(options.recipe_reqs.value)))
            khdddworld.set_rule(khdddworld.get_location("Unbound Keyblade Reward [Sora]"),
                    can_access_sora_portals())
            if options.goal == 1: #All Superbosses defeated needs a rule here too
                khdddworld.set_rule(khdddworld.get_location("All Superbosses Defeated [Sora] [Riku]"),
                         can_access_sora_portals() & tt2_access_sora() & has_required_recipes(options.recipe_reqs.value))


        ###################################
        ###########Traverse Town###########
        ###################################

        #####Third District Balcony#####
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Third District Vibrant Fantasy [Sora]"),
                 Has("High Jump") | can_infinite_jump())

        #####Second District Rooftops#####
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Second District Confetti Candy [Sora]"),
                 Has("High Jump") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Second District Balloon [Sora]"),
                 Has("High Jump") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Second District Hi-Potion [Sora]"),
                 Has("High Jump") | can_infinite_jump())

        #Everything in and beyond Sora's Post Office room should require this movement for the player's own sanity

        #####Post Office#####
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Post Office Rampant Fantasy [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Post Office Vibrant Fantasy [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Post Office Troubling Fantasy [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Post Office Spark [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Post Office Paint Gun: Red [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Post Office Potion [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Post Office Ice Dream Cone [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())

        #####Fountain Plaza#####
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fountain Plaza Balloon [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fountain Plaza Intrepid Figment [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fountain Plaza Ice Dream Cone [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fountain Plaza Rampant Fantasy [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") & (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fountain Plaza Strike Raid [Sora]"),
                 HasAny("Glide", "Superglide", "Flowmotion") | (can_infinite_jump()))

        #####Fourth District#####
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fourth District Shield Cookie [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fourth District Water Barrel [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fourth District Hi-Potion [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fourth District Ice Dream Cone [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fourth District Potion [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fourth District Block-It Chocolate [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fourth District 2nd Potion [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fourth District Balloon (Command) [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))

        #####Fifth District#####
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fifth District Shield Cookie [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fifth District Potion [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fifth District Block-It Chocolate [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))

        #####Garden#####
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Garden Royal Cake [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Garden Confetti Candy [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Garden Rampant Figment [Sora]"), #On the upper ledge
                 HasAny("Rail Slide", "Flowmotion") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Garden Drop-Me-Not [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | (can_infinite_jump()))


        #####Story#####
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Hockomonkey Bonus Slot 1 [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Hockomonkey Bonus Slot 2 [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Skull Noise Reward [Sora]"),
                 HasAny("Glide", "Rail Slide", "Superglide", "Flowmotion") | can_infinite_jump())

        ###################################
        ########La Cite des Cloches########
        ###################################
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Bell Tower Dulcet Figment [Sora]"),
                 HasAny("Flowmotion", "High Jump") | (can_pole_jump()) | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Bell Tower Drop-Me-Not [Sora]"),
                 HasAny("Flowmotion", "High Jump") | (can_pole_jump()) | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Catacombs Water Barrel [Sora]"),
                            HasAny("Flowmotion", "High Jump", "Air Slide", "Wall Kick", "Glide", "Superglide"))

        ###################################
        ##############The Grid#############
        ###################################
        for name, data in location_data_table.items(): #Sora can only reach the first location without tools
            if data.region == "The Grid [Sora]" and name != "The Grid City Potion [Sora]":

                if name == "The Grid Secret Portal [Sora]":
                    if not options.superbosses and options.goal == 0:
                        continue

                khdddworld.set_rule(khdddworld.get_location(name),
                         (HasAny("Glide", "Superglide", "Rail Slide", "Flowmotion")
                         | can_infinite_jump()))

        khdddworld.set_rule(khdddworld.get_location("The Grid Throughput Dulcet Figment [Sora]"),
                (HasAny("High Jump", "Rail Slide", "Flowmotion")
                | (can_infinite_jump()) | (can_pole_jump())))
        khdddworld.set_rule(khdddworld.get_location("The Grid City Troubling Fancy [Sora]"),
                    (Has("Flowmotion")
                    | (can_infinite_jump()) | (HasAny("Glide", "Superglide"))))

        ###################################
        ########Prankster's Paradise#######
        ###################################
        khdddworld.set_rule(khdddworld.get_location("Prankster's Paradise Windup Way Aerial Slam [Sora]"),
                 can_infinite_jump() | (Has("High Jump") & can_pole_jump()))
        khdddworld.set_rule(khdddworld.get_location("Prankster's Paradise Windup Way Royal Cake [Sora]"),
                 can_infinite_jump() | (Has("High Jump") & can_pole_jump()))
        khdddworld.set_rule(khdddworld.get_location("Prankster's Paradise Circus Rampant Fancy [Sora]"),
                 can_infinite_jump() | (Has("High Jump") & can_pole_jump()))

        ###################################
        #####Country of the Musketeers#####
        ###################################
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Mont Saint-Michel Sparkga [Sora]"),
                 (can_infinite_jump() | (HasAny("High Jump", "Flowmotion"))))

        ###################################
        ########Symphony of Sorcery########
        ###################################
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Cloudwalk Candy Goggles [Sora]"),
                 (HasAny("Wall Kick", "Superglide", "Glide", "Flowmotion")))
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Glen Royal Cake [Sora]"),
                 (HasAny("Wall Kick", "Superglide", "Glide", "Flowmotion")))
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Glen Intrepid Fantasy [Sora]"),
                 (HasAny("Wall Kick", "Superglide", "Glide", "Flowmotion")))
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Fields Electricorn Recipe [Sora]"),
                 (HasAny("Superglide", "Glide", "Flowmotion") | (can_infinite_jump())))

        ###################################
        #####The World That Never Was######
        ###################################
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Xemnas Bonus Slot 1 [Sora]"),
                 (can_infinite_jump() | (Has("High Jump")
                        & (HasAny("Air Slide", "Glide"))) | (Has("Flowmotion"))))

        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Glossary: Recusant's Sigil Reward [Sora]"),
                 (can_infinite_jump() | (Has("High Jump")
                        & (HasAny("Air Slide", "Glide"))) | (Has("Flowmotion"))))

        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Glossary: Hearts Tied to Sora Reward [Sora]"),
                 (can_infinite_jump() | (Has("High Jump")
                        & (HasAny("Air Slide", "Glide"))) | (Has("Flowmotion"))))

        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Contorted City Ice Dream Cone 3 [Sora]"),
                 (can_infinite_jump() | (Has("Flowmotion"))
                        | (Has("High Jump") & (HasAny("Air Slide", "Glide")))))

        #####Add Macguffin Rules#####
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Xemnas Bonus Slot 1 [Sora]"),
                 has_macguffins(options.recipe_reqs.value) & (HasAllCounts({"Lucky Emblem": options.emblem_reqs.value})))
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Glossary: Recusant's Sigil Reward [Sora]"),
                 has_macguffins(options.recipe_reqs.value) & (HasAllCounts({"Lucky Emblem": options.emblem_reqs.value})))
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Glossary: Hearts Tied to Sora Reward [Sora]"),
                 has_macguffins(options.recipe_reqs.value) & (HasAllCounts({"Lucky Emblem": options.emblem_reqs.value})))

    ###############################
    #########RIKU RULES############
    ###############################

    if options.character == 0 or options.character == 2:
        ###################################
        ############Superbosses############
        ###################################
        if options.superbosses or options.goal == 1:
            khdddworld.set_rule(khdddworld.get_location("Traverse Town Secret Portal [Riku]"), has_x_riku_worlds(6) & (HasAny("Rail Slide", "Double Flight", "Flowmotion") | can_infinite_jump()))
            khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Secret Portal [Riku]"), has_x_riku_worlds(6) & Has("Air Slide"))
            khdddworld.set_rule(khdddworld.get_location("The Grid Secret Portal [Riku]"), has_x_riku_worlds(6))
            khdddworld.set_rule(khdddworld.get_location("Prankster's Paradise Secret Portal [Riku]"), has_x_riku_worlds(6))
            khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Secret Portal [Riku]"), has_x_riku_worlds(6))
            khdddworld.set_rule(khdddworld.get_location("Traverse Town 2 Ultima Weapon Reward [Riku]"), can_access_riku_portals() & (has_required_recipes(options.recipe_reqs.value)))
            khdddworld.set_rule(khdddworld.get_location("Unbound Keyblade Reward [Riku]"), can_access_riku_portals())
            if options.goal == 1:
                khdddworld.set_rule(khdddworld.get_location("All Superbosses Defeated [Sora] [Riku]"),
                         can_access_riku_portals() & tt2_access_riku() & HasAllCounts({"Lucky Emblem": options.emblem_reqs.value}) & has_required_recipes(options.recipe_reqs.value))

        ###################################
        ###########Traverse Town###########
        ###################################
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Second District Block-It Chocolate [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Second District Balloon [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Traverse Town Second District Yoggy Ram Recipe [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump())

        khdddworld.set_rule(khdddworld.get_location("Traverse Town Third District Ice Dream Cone [Riku]"),
                 HasAny("Double Flight", "Flowmotion", "High Jump") | (can_infinite_jump()))

        khdddworld.set_rule(khdddworld.get_location("Traverse Town Back Streets Troubling Fantasy [Riku]"),
                 HasAll("Double Flight", "Air Slide") | (
                     can_infinite_jump()) | (Has("Flowmotion")))

        khdddworld.set_rule(khdddworld.get_location("Traverse Town Back Streets Intrepid Figment [Riku]"),
                 HasAll("Double Flight", "Air Slide") | (
                     can_infinite_jump()) | Has("Flowmotion"))

        khdddworld.set_rule(khdddworld.get_location("Traverse Town Fountain Plaza Blizzard Edge [Riku]"),
                 HasAny("Double Flight", "High Jump", "Flowmotion") | can_infinite_jump())

        khdddworld.set_rule(khdddworld.get_location("Traverse Town Garden Royal Cake [Riku]"),
                 HasAny("Rail Slide, Flowmotion") | can_infinite_jump())

        ###################################
        ########La Cite des Cloches########
        ###################################
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Bell Tower Royal Cake [Riku]"),
                 HasAny("Flowmotion", "High Jump", "Double Flight") | (
                     can_pole_jump()) | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Bell Tower Dulcet Figment [Riku]"),
                 HasAny("Flowmotion", "High Jump", "Double Flight") | (can_pole_jump()) | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Wargoyle Bonus Slot 1 [Riku]"), #Require Air Slide for these checks for convenience
                 Has("Air Slide"))
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Wargoyle Bonus Slot 2 [Riku]"),
                 Has("Air Slide"))
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Chronicle: Kingdom Hearts Reward [Riku]"),
                 Has("Air Slide"))
        khdddworld.set_rule(khdddworld.get_location("La Cite des Cloches Guardian Bell Reward [Riku]"),
                 Has("Air Slide"))

        ###################################
        ##############The Grid#############
        ###################################
        khdddworld.set_rule(khdddworld.get_location("The Grid City Fleeting Figment [Riku]"),
                 (HasAny("Flowmotion", "Rail Slide")
                        | (can_infinite_jump())))
        khdddworld.set_rule(khdddworld.get_location("The Grid City Drop-Me-Not [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") | (can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("The Grid City Thundara [Riku]"),
                 (Has("Flowmotion") | (can_infinite_jump())))
        khdddworld.set_rule(khdddworld.get_location("The Grid Throughput Noble Fantasy [Riku]"),
                 (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion")
                         | (can_infinite_jump()) | (can_pole_jump())))

        ###################################
        ########Prankster's Paradise#######
        ###################################
        #Both of these are technically possible without flowmotion
        khdddworld.set_rule(khdddworld.get_location("Prankster's Paradise Monstro: Gullet Charming Fantasy [Riku]"),
                 Has("Flowmotion") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("Prankster's Paradise Monstro: Gullet Sir Kyroo Recipe [Riku]"),
                 (HasAny("Rail Slide", "Flowmotion") | can_infinite_jump()))

        ###################################
        #####Country of the Musketeers#####
        ###################################

        #####Grand Lobby#####
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Grand Lobby Shadowbreaker [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight") | can_infinite_jump()))

        #####Green Room#####
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Green Room Candy Goggles [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Green Room Prickly Fantasy [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Green Room Fleeting Fantasy [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Green Room Shield Cookie 3 [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Green Room Hi-Potion [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Green Room Stop [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Green Room Drop-Me-Not [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Green Room Confetti Candy 3 [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))

        #####Machine Room#####
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Machine Room Blizzaga [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Machine Room Ducky Goose Recipe [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Machine Room Ice Dream Cone 2 [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Machine Room Drop-Me-Not [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Machine Room Hi-Potion [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Machine Room Mega-Potion [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))

        #####Backstage#####
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Backstage Royal Cake [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Backstage Fleeting Fantasy [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Backstage Dream Candy [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Backstage Staggerceps Recipe [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Backstage Drop-Me-Not [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Backstage Mega-Potion [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))

        #####Story#####
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Flashback: Bon Journey Reward [Riku]"),
                 HasAny("Pole Spin", "Flowmotion")
                        & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Stage Gadget Reward [Riku]"),
                            HasAny("Pole Spin", "Flowmotion")
                            & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Holey Moley Bonus Slot 1 [Riku]"),
                            HasAny("Pole Spin", "Flowmotion")
                            & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Shadow Strike Reward [Riku]"),
                            HasAny("Pole Spin", "Flowmotion")
                            & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers Shadow Slide Reward [Riku]"),
                            HasAny("Pole Spin", "Flowmotion")
                            & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))
        khdddworld.set_rule(khdddworld.get_location("Country of the Musketeers All For One Reward [Riku]"),
                            HasAny("Pole Spin", "Flowmotion")
                            & (HasAny("High Jump", "Double Flight", "Rail Slide", "Flowmotion") | can_infinite_jump()))

        ###################################
        ########Symphony of Sorcery########
        ###################################

        #####Moonlight Wood#####
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Zero Graviza [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Paint Gun: Green [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Intrepid Fancy [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())

        if options.lord_kyroo:
            khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Lord Kyroo Fight [Riku]"),
                     HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())

        #####Golden Wood#####
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Elixir [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Intrepid Fantasy [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Mega-Potion [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                               & (HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump()))
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Paint Gun: Red [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Ryu Dragon Recipe [Riku]"),
                 HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())

        #####Snowgleam Wood#####
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Ice Barrage [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                               & HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Candy Goggles [Riku]"),
                            HasAny("Flowmotion", "Rail Slide")
                            & HasAny("High Jump", "Double Flight",
                                     "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Block-It Chocolate [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                 & HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Ice Dream Cone 3 [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                 & HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Dulcet Fancy [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                 & HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Confetti Candy 3 [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                 & HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())

        #####Story#####
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Chernobog Bonus Slot 1 [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                 & HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Chernobog Bonus Slot 2 [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                 & HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("Symphony of Sorcery Counterpoint Reward [Riku]"),
                 HasAny("Flowmotion", "Rail Slide")
                 & HasAny("High Jump", "Double Flight", "Flowmotion") | can_infinite_jump() | can_pole_jump())

        ###################################
        #####The World That Never Was######
        ###################################

        #Delusive Beginning

        #On ledge behind pole
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Delusive Beginning Third Elixir [Riku]"),
                 HasAny("Flowmotion", "Rail Slide", "High Jump") | can_infinite_jump() | can_pole_jump())
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Delusive Beginning Keeba Tiger Recipe [Riku]"),
                 HasAny("Flowmotion", "Rail Slide", "High Jump") | can_infinite_jump() | can_pole_jump())
        #Parkour chests
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Delusive Beginning Second Elixir [Riku]"),
                            HasAny("Flowmotion", "High Jump", "Doubleflight") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Delusive Beginning Dulcet Fantasy [Riku]"),
                            HasAny("Flowmotion", "High Jump", "Doubleflight") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Delusive Beginning Dark Splicer [Riku]"),
                            HasAny("Flowmotion", "High Jump", "Doubleflight") | can_infinite_jump())

        #Fact Within Fiction

        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Fact Within Fiction Spark Raid [Riku]"),
                            HasAll("Rail Slide", "Super Jump") | can_infinite_jump() | Has("Flowmotion"))

        #Verge of Chaos
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Candy Goggles [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Second Elixir [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Shield Cookie 3 [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Skelterwild Recipe [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") | can_infinite_jump())
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Wondrous Fantasy [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") | can_infinite_jump())

        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Ansem II Defeated [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") & Has("Air Slide"))
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Ansem I Defeated [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") & Has("Air Slide"))
        khdddworld.set_rule(khdddworld.get_location("The World That Never Was Anti Black Coat Nightmare Defeated [Riku]"),
                 HasAny("Flowmotion", "Rail Slide") & Has("Air Slide"))

        if options.goal == 0: #YX/AVN can only be played with Final Boss goal
            if options.character == 0:
                khdddworld.set_rule(khdddworld.get_location("The World That Never Was Young Xehanort Defeated [Riku]"),
                    (CanReachLocation(khdddworld.get_location("The World That Never Was Xemnas Bonus Slot 1 [Sora]"))))
            elif options.character == 2:
                 khdddworld.set_rule(khdddworld.get_location("The World That Never Was Young Xehanort Defeated [Riku]"),
             (HasAll("Meow Wow Recipe", "Komory Bat Recipe", "Recusant Sigil") & (HasAllCounts({"Lucky Emblem":options.emblem_reqs.value})) & (has_required_recipes(options.recipe_reqs.value))))

            if options.armored_ventus_nightmare:
                khdddworld.set_rule(khdddworld.get_location("Armored Ventus Nightmare Defeated [Riku]"),
                    (CanReachLocation(khdddworld.get_location("The World That Never Was Young Xehanort Defeated [Riku]"))))

            #Require Rail Slide to reach the end since it is needed to start ABC
            khdddworld.set_rule(khdddworld.get_location("The World That Never Was Young Xehanort Defeated [Riku]"),
                    HasAny("Rail Slide", "Flowmotion"))
            if options.armored_ventus_nightmare:
                khdddworld.set_rule(khdddworld.get_location("Armored Ventus Nightmare Defeated [Riku]"),
                    HasAny("Rail Slide", "Flowmotion"))


    #Lord Kyroo Completion Access
    #if options.lord_kyroo:
    #    if options.character == 0 or options.character == 1:
    #        khdddworld.set_rule(khdddworld.get_location("Lord Kyroo Defeated [Sora] [Riku]"),
    #                 CanReachLocation(khdddworld.get_location("Prankster's Paradise Promontory Lord Kyroo Fight [Sora]")))
    #    elif options.character == 0 or options.character == 2:
    #        khdddworld.set_rule(khdddworld.get_location("Lord Kyroo Defeated [Sora] [Riku]"),
    #                 CanReachLocation(khdddworld.get_location("La Cite des Cloches Nave Lord Kyroo Fight [Riku]")))
    #        khdddworld.set_rule(khdddworld.get_location("Lord Kyroo Defeated [Sora] [Riku]"),
    #                 CanReachLocation(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Lord Kyroo Fight [Riku]")))

    #Region rules
    #if options.character == 0:
    #    khdddworld.set_rule(khdddworld.get_entrance("Levels"),
    #             has_x_sora_worlds(1) | (has_x_riku_worlds(1)))
    #elif options.character == 1:
    #    khdddworld.set_rule(khdddworld.get_entrance("Levels"),
    #             has_x_sora_worlds(1))
    #elif options.character == 2:
    #    khdddworld.set_rule(khdddworld.get_entrance("Levels"),
    #             has_x_riku_worlds(1))

    khdddworld.set_rule(khdddworld.get_entrance("Traverse Town [Sora]"),
             Has("Traverse Town [Sora]"))
    khdddworld.set_rule(khdddworld.get_entrance("The Grid [Sora]"),
             Has("The Grid [Sora]"))
    khdddworld.set_rule(khdddworld.get_entrance("La Cite des Cloches [Sora]"),
             Has("La Cite des Cloches [Sora]"))
    khdddworld.set_rule(khdddworld.get_entrance("Prankster's Paradise [Sora]"),
             Has("Prankster's Paradise [Sora]"))
    khdddworld.set_rule(khdddworld.get_entrance("Country of the Musketeers [Sora]"),
             Has("Country of the Musketeers [Sora]"))
    khdddworld.set_rule(khdddworld.get_entrance("The World That Never Was [Sora]"),
             Has("The World That Never Was [Sora]") & has_x_sora_worlds(4))
    khdddworld.set_rule(khdddworld.get_entrance("Symphony of Sorcery [Sora]"),
             Has("Symphony of Sorcery [Sora]"))
    khdddworld.set_rule(khdddworld.get_entrance("Traverse Town 2 [Sora]"),
             HasAny("Wall Kick", "Glide", "Superglide", "Rail Slide", "Flowmotion") & (HasAllCounts({"Traverse Town [Sora]":2})))

    khdddworld.set_rule(khdddworld.get_entrance("Traverse Town [Riku]"),
             Has("Traverse Town [Riku]"))
    khdddworld.set_rule(khdddworld.get_entrance("The Grid [Riku]"),
             Has("The Grid [Riku]"))
    khdddworld.set_rule(khdddworld.get_entrance("La Cite des Cloches [Riku]"),
             Has("La Cite des Cloches [Riku]"))
    khdddworld.set_rule(khdddworld.get_entrance("Prankster's Paradise [Riku]"),
             Has("Prankster's Paradise [Riku]"))
    khdddworld.set_rule(khdddworld.get_entrance("Country of the Musketeers [Riku]"),
             Has("Country of the Musketeers [Riku]"))
    khdddworld.set_rule(khdddworld.get_entrance("The World That Never Was [Riku]"),
             Has("The World That Never Was [Riku]") & has_x_riku_worlds(4))
    khdddworld.set_rule(khdddworld.get_entrance("Symphony of Sorcery [Riku]"),
             Has("Symphony of Sorcery [Riku]"))
    khdddworld.set_rule(khdddworld.get_entrance("Traverse Town 2 [Riku]"),
             HasAllCounts({"Traverse Town [Riku]":2}))

    if options.emblem_reqs.value > 0:
        khdddworld.set_rule(khdddworld.get_location("All Lucky Emblems Found [Sora] [Riku]"),
             HasAllCounts({"Lucky Emblem":options.emblem_reqs.value}))



    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)