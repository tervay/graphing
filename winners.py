import networkx as nx
from tbapy import TBA
from tqdm import tqdm

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


for event in tqdm(tba.events(year=year)):
    if event["event_type"] not in [0, 1, 2, 3, 4, 5]:
        continue

    try:
        alliances = tba.event_alliances(event=event["key"])
    except:
        continue

    for alliance in alliances:
        if (
            "status" not in alliance
            or alliance["status"] == "unknown"
            or alliance["status"] is None
        ):
            continue

        if alliance["status"]["status"] == "won":
            for p1 in alliance["picks"]:
                for p2 in alliance["picks"]:
                    if p1 == p2:
                        continue

                    edges.add((team_str_num(p1), team_str_num(p2)))

            if "backup" in alliance and alliance["backup"] is not None:
                for p in alliance["picks"]:
                    edges.add((team_str_num(p), team_str_num(alliance["backup"]["in"])))


g = nx.Graph()
# g.add_nodes_from(nodes)
g.add_edges_from(edges)


GraphSaver(g, f"winners_{year}", rough_figure_size=7500).save()
