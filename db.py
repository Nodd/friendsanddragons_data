import json
from pprint import pprint


class Hero:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        return self._data[name]

    @property
    def traits(self):
        traits = list(self._data["basic_traits"])
        traits.extend(
            (
                self._data["asc_traits"],
                self._data["asc2_traits"],
                self._data["asc3_traits"],
            )
        )
        return traits


class HeroesDB:
    def __init__(self, heroes):
        self._heroes = [Hero(data) for data in heroes]

    @property
    def traits(self):
        traits = set()
        for hero in self._heroes:
            for trait in hero.traits:
                traits.add(trait)
        return traits


heroes = json.load(open("heroes.json"))
db = HeroesDB(heroes)


print(len(db.traits))
pprint(db.traits)
