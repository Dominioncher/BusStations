import flask
from flask import request
from bson.json_util import dumps
import Core.Graph.Graph as Bus

app = flask.Flask(__name__)

graph = Bus.BusGraph()
graph.load_data()


@app.route('/checkpoints', methods=['GET'])
def get_checkpoints():
    checkpoints = []
    for node in graph.graph.nodes:
        checkpoints.append(graph.graph.nodes[node]['checkpoint'])
    return dumps(checkpoints)


@app.route('/', methods=['POST', 'GET'])
def get_map_html():
    return flask.render_template('map.html')


@app.route('/addCheckpoint', methods=['GET'])
def add_checkpoint():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    return graph.add_checkpoint('Новая остановка', lat, lon)
