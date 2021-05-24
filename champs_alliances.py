import networkx as nx
from tbapy import TBA
from tqdm import tqdm
from pprint import pprint

from GraphSaver import GraphSaver

tba = TBA("FfBdTrj0DX7qOqbIaLYYQ0i5HemtJYC2S6OlYl12ODrFdjdpMwG176m0zcL2Jtwn")

year = 2019

edges = set()


def team_str_num(s: str):
    s = s[3:]
    if s[-1].isnumeric():
        return int(s)
    else:
        return int(s[:-1])


c = 0


def get_alliance_edges(teams):
    l = []
    for t1 in teams:
        for t2 in teams:
            if t1 == t2:
                continue

            l.append((team_str_num(t1), team_str_num(t2)))

    return l


keys = [f"{y}cmp" for y in range(2002, 2017)]
keys.extend(["2017cmpmo", "2017cmptx"])
keys.extend(["2018cmpmi", "2018cmptx"])
keys.extend(["2019cmpmi", "2019cmptx"])

for k in tqdm(keys):
    for child_key in tba.event(k)["division_keys"]:
        try:
            alliances = tba.event_alliances(event=child_key)
            for alliance in alliances:
                edges.update(get_alliance_edges(alliance["picks"]))
        except:
            matches = tba.event_matches(event=child_key)
            for match in matches:
                if match["comp_level"] != "qm":
                    for c in ["red", "blue"]:
                        edges.update(
                            get_alliance_edges(match["alliances"][c]["team_keys"])
                        )

g = nx.Graph()
g.add_edges_from(edges)


GraphSaver(g, "champs_alliances", rough_figure_size=8000).save()
