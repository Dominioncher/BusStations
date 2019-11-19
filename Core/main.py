import Core.Graph.Graph as Bus

graph = Bus.BusGraph()
graph.load_data()
graph.modify_checkpoints([1])
graph.add_checkpoint("ИМИКН", 57.158820, 65.522632)
graph.remove_checkpoint(1)
graph.optimize()
