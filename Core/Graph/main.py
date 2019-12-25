import Core.Graph.Graph as Bus

graph = Bus.BusGraph()
graph.load_data()
x = 0
nodes = list()
nodes.append(dict(lat=57.15274, lon=65.54097, name=1, id=10001))
nodes.append(dict(lat=57.15170, lon=65.53907, name=2, id=10002))
nodes.append(dict(lat=57.15019, lon=65.53689, name=3, id=10003))
nodes.append(dict(lat=57.15091, lon=65.53548, name=4, id=10004))
graph.get_optimised_route(graph.graph.nodes._nodes[321]['checkpoint'], graph.graph.nodes._nodes[190]['checkpoint'],
                          nodes)
# graph.modify_checkpoints([1])
# graph.add_checkpoint("ИМИКН", 57.158820, 65.522632)
# graph.remove_checkpoint(1)
# graph.optimize()
# graph.graph.nodes._nodes[321]
# graph.graph.nodes._nodes[190]
#
