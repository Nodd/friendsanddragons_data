from db import db

for hero in db.by_stars(1, 2, 3):
    hero.known = True
