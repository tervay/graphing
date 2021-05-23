from tbapy import TBA
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm
from GraphSaver import GraphSaver

tba = TBA("FfBdTrj0DX7qOqbIaLYYQ0i5HemtJYC2S6OlYl12ODrFdjdpMwG176m0zcL2Jtwn")

# years = [2019]
# states = ["ME", "VT", "NH", "MA", "RI", "CT"]
states = ["VA", "MD"]

years = [2019]
# states = [""]

nodes = set()
edges = set()


def str_to_num(s: str):
    s = s[3:]
    if s[-1].isnumeric():
        return int(s)
    else:
        return int(s[:-1])


for year in tqdm(years):
    events = tba.events(year=year)
    for event in events:
        # https://github.com/the-blue-alliance/the-blue-alliance/blob/master/consts/event_type.py
        if event["event_type"] not in [0, 1, 2, 5]:
            continue

        alliances = set()
        if event["state_prov"] in states:
            for match in tba.event_matches(event=event["key"]):
                if match["comp_level"] != "qm":
                    alliances.add(
                        frozenset(sorted(match["alliances"]["blue"]["team_keys"]))
                    )
                    alliances.add(
                        frozenset(sorted(match["alliances"]["red"]["team_keys"]))
                    )

        for alliance in alliances:
            for team in alliance:
                nodes.add(team[3:])

            for t1 in alliance:
                for t2 in alliance:
                    if t1 == t2:
                        continue

                    edges.add((str_to_num(t1), str_to_num(t2)))

g = nx.Graph()
# g.add_nodes_from(nodes)
g.add_edges_from(edges)

name = "-".join(sorted(states))
years = "-".join([str(y) for y in years])
GraphSaver(g, f"{name}_{years}", rough_figure_size=7500).save()
