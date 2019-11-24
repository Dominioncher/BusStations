import json

import flask
import Core.DataLoaders.DataLoader as DL

PORT = 5000

app = flask.Flask(__name__)


@app.route('/checkpoints', methods=['GET'])
def get_checkpoints():
    checkpoints = DL.get_checkpoints()[:20]
    response_json = json.dumps(checkpoints)

    resp = flask.Response(status=200)
    resp.data = response_json
    resp.content_type = "application/json"

    return resp


app.run(port=PORT)
