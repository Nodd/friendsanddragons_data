import json
from pprint import pprint


class Hero:
    def __init__(self, data):
        self._data = data
        self.known = False

    def __getattr__(self, name):
        return self._data[name]

    @property
    def all_traits(self):
        traits = list(self._data["basic_traits"])
        traits.extend(
            (
                self._data["asc_traits"],
                self._data["asc2_traits"],
                self._data["asc3_traits"],
            )
        )
        return traits

    @property
    def all_gear(self):
        gear = []
        for asc in ["basic_gear", "asc_gear", "asc2_gear", "asc3_gear"]:
            gear.extend(self._data[asc].values())
        return gear


class Gear:
    GEAR_RANK = ["Magic", "Epic", "Mythic", "Legendary", "Exalted", "Divine"]
    AMULET_RANK = ["Radiant", "Brilliant", "Coruscating", "Incandescent"]
    GEAR_KIND = ["amulet", "weapon", "ring", "head", "off_hand", "body"]

    def __init__(self, name, kind):
        rank, name = name.split(" ", 1)
        self.rank = rank
        self.name = name
        self.kind = kind

    @property
    def rank_num(self):
        if self.kind == "amulet":
            return self.AMULET_RANK.index(self.rank)
        else:
            return self.GEAR_RANK.index(self.rank)

    @property
    def next_ranks(self):
        if self.kind == "amulet":
            ranks = self.AMULET_RANK[self.rank_num + 1 :]
        else:
            ranks = self.GEAR_RANK[self.rank_num + 1 :]
        return [f"{rank} {self.name}" for rank in ranks]

    @property
    def previous_ranks(self):
        if self.kind == "amulet":
            ranks = self.AMULET_RANK[: self.rank_num]
        else:
            ranks = self.GEAR_RANK[: self.rank_num]
        return [f"{rank} {self.name}" for rank in ranks]


class HeroesDB:
    def __init__(self, heroes):
        self._heroes = {data["name"]: Hero(data) for data in heroes}

    @property
    def heroes(self):
        yield from self._heroes.values()

    @property
    def all_traits(self):
        traits = set()
        for hero in self.heroes:
            traits.update(hero.all_traits)
        return traits

    @property
    def all_gear(self):
        all_gear = set()
        for hero in self.heroes:
            all_gear.update(hero.all_gear)
        return all_gear

    def by_stars(self, *stars: int):
        return [hero for hero in self.heroes if hero.stars in stars]

    def by_names(self, names: str | list[str]):
        if isinstance(names, str):
            names = self._heroes[names]
        else:
            return [hero for hero in self._heroes if hero.name in names]


with open("heroes.json") as f:
    heroes = json.load(f)
db = HeroesDB(heroes)

pprint(db.all_traits)
pprint(db.all_gear)
