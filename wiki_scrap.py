import contextlib
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pprint import pprint
from requests_html import AsyncHTMLSession
import asyncio
import re

BASE_URL = "https://friends-and-dragons.fandom.com"


def get_heroes():
    url_heroes = f"{BASE_URL}/wiki/Category:Heroes"
    page_heroes = urlopen(url_heroes)
    html_heroes = page_heroes.read().decode("utf-8")
    soup_heroes = BeautifulSoup(html_heroes, "html.parser")

    links_heroes = soup_heroes.find_all(class_="category-page__member-link")

    return {
        link["title"]: link["href"] for link in links_heroes if link["title"].isalpha()
    }


NUMBER_PTN = re.compile(r"\d+")


async def parse_hero(session, name, wiki_link):
    url = BASE_URL + wiki_link

    # page = urlopen(url)
    # html = page.read().decode("utf-8")
    response = await session.get(url)
    html = response.html.raw_html

    soup = BeautifulSoup(html, "html.parser")

    info = soup.find(name="div", class_="mw-parser-output")

    elements = info.find_all(lambda tag: tag.get("data-source"))
    data_source_tags = [e.get("data-source") for e in elements]

    # pprint(data_source_values)
    # 'name',
    # 'image',
    # 'class',
    # 'color',
    # 'species',
    # 'stars',
    # 'ai',
    # 'aispd',
    # 'basic_traits',
    # 'asc_traits',
    # 'asc2_traits',
    # 'asc3_traits',
    # 'basic_gear',
    # 'asc_gear',
    # 'asc2_gear',
    # 'asc3_gear',
    # 'basic_attack',
    # 'basic_health',
    # 'asc_attack',
    # 'asc_health',
    # 'asc2_attack',
    # 'asc2_health',
    # 'asc3_attack',
    # 'asc3_health'

    data = {}
    for tag in data_source_tags:
        if tag_data := get_data_source(info, tag):
            if len(tag_data) == 1:
                tag_data = tag_data[0]
                with contextlib.suppress(ValueError):
                    tag_data = int(tag_data)
            data[tag] = tag_data
    data["name"] = name

    ASC = ["basic", "asc", "asc2", "asc3"]
    for asc_attr in ["attack", "health"]:
        total = []
        base = []
        gear = []
        for asc in ASC:
            tag = f"{asc}_{asc_attr}"
            value = data[tag]
            total.append(int(value[0]))
            matches = NUMBER_PTN.findall(value[1])
            assert len(matches) == 2
            base.append(int(matches[0]))
            gear.append(int(matches[1]))
            del data[tag]

        data[f"{asc_attr}_total"] = total
        data[f"{asc_attr}_base"] = base
        data[f"{asc_attr}_gear"] = gear

    data["stars"] = data["stars"].count("⭐")

    for tag in ["basic_gear", "asc_gear", "asc2_gear", "asc3_gear"]:
        data[tag] = gear_list_to_dict(data[tag])

    pprint(data)

    return data


def gear_list_to_dict(gear_list):
    """Convert a list of gear to a dict with standard keys."""
    keys = ["amulet", "weapon", "ring", "head", "off_hand", "body"]
    return dict(zip(keys, gear_list))


def get_data_source(info, value):
    data_source = info.find(lambda tag: tag.get("data-source") == value)
    if data := data_source.find(class_="pi-data-value"):
        return data.get_text(separator="<br/>").split("<br/>")
    else:
        return


async def get_data():
    heroes = get_heroes()
    print(len(heroes), "heroes found")

    # Take only 2 heroes for testing
    heroes = dict(list(heroes.items())[:2])

    session = AsyncHTMLSession()
    tasks = [parse_hero(session, name, wiki_link) for name, wiki_link in heroes.items()]
    return await asyncio.gather(*tasks)


def main():
    data = asyncio.run(get_data())
    pprint(data)
    return data


if __name__ == "__main__":
    main()
