import flask
from Core.DB.MongoController import db
from bson.json_util import dumps

PORT =  int(os.environ.get("PORT", 5000))

app = flask.Flask(__name__)


@app.route('/checkpoints', methods=['GET'])
def get_checkpoints():
    checkpoints = list(db['checkpoints'].find())

    resp = flask.Response(status=200)
    resp.data = dumps(checkpoints)
    resp.content_type = "application/json"
    return resp


@app.route('/', methods=['POST', 'GET'])
def get_map_html():
    return flask.render_template('map.html')


app.run(port=PORT)
