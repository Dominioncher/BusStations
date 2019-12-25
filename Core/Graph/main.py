import Core.Graph.Graph as Bus

graph = Bus.BusGraph()
graph.load_data()
x = 0
# nodes = list()
# graph.add_checkpoint("ИМИКН", 57.158820, 65.522632)
id1 = graph.add_checkpoint("10000", 57.15274, 65.54097)  # id 3827
id2 = graph.add_checkpoint("10001", 57.15170, 65.53907)
id3 = graph.add_checkpoint("10002", 57.15019, 65.53689)
id4 = graph.add_checkpoint("10003", 57.15091, 65.53548)
# graph.remove_checkpoint(3827)
to_delete = graph.get_optimised_route(graph.graph.nodes._nodes[321]['checkpoint'],
                                      graph.graph.nodes._nodes[187]['checkpoint'],
                                      [id1, id2, id3, id4, graph.graph.nodes._nodes[190]['checkpoint']])
graph.remove_checkpoints(to_delete)
# graph.graph.nodes._nodes[321]['checkpoint']  # Цветной бульвар ул. Ленина, 52/1
# graph.graph.nodes._nodes[190]['checkpoint']  # Центральный рынок напротив ул. Орджоникидзе, 63
# graph.graph.nodes._nodes[187]['checkpoint']  # Станкостроительный завод ул. Республики, 86
x = 0
