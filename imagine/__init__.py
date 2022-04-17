from flask import Flask, abort, request
import os
from pymongo import MongoClient
from pymongo.collection import Collection
from imagine.utilities import Triangulator
import time
from _thread import *

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

mongo = MongoClient(
    host=f'{app.config["MONGO_HOST"]}/{app.config["MONGO_DB"]}',
    username=app.config["MONGO_USER"],
    password=app.config["MONGO_PASS"],
    tls=app.config["MONGO_SSL"],
)

frames: Collection = mongo[app.config["MONGO_DB"]][
    app.config["MONGO_FRAMES_COLLECTION"]
]
esps: Collection = mongo[app.config["MONGO_DB"]][
    app.config["MONGO_ESP_COLLECTION"]
]
output: Collection = mongo[app.config["MONGO_DB"]][
    app.config["MONGO_OUTPUT_COLLECTION"]
]
command: Collection = mongo[app.config["MONGO_DB"]][
    app.config["MONGO_COMMAND_COLLECTION"]
]

triangulator = Triangulator(
    app.config["TRIANGULATION_ENV_FACTOR"],
    app.config["TRIANGULATION_ONE_METER_RSSI"],
    [float(i) for i in app.config["TRIANGULATION_ZERO"].split(",")],
    mongo_client=mongo,
    mongo_database=app.config["MONGO_DB"],
    mongo_frames_collection=app.config["MONGO_FRAMES_COLLECTION"],
    mongo_esp_collection=app.config["MONGO_ESP_COLLECTION"],
    mongo_output_collection=app.config["MONGO_OUTPUT_COLLECTION"]
)

_ovr = os.environ.get("TRIANGULATION_TIMESTAMP_OVERRIDE", default="no")
TIME_OVERRIDE: float = float(_ovr) if _ovr != "no" else False

@app.route('/sugma', methods=['GET'])
def update():
    if triangulator.run_once(TIME_OVERRIDE if TIME_OVERRIDE else (time.time() - 2.5), bounds=2.5):
        return "OK", 200
    return "FUCK", 500

@app.route('/beacons/locations', methods=['GET'])
def locations():
    res = output.find()
    return {i["beacon_id"]: {k: v for k, v in i.items() if not k in ["_id", "testpos"]} for i in res}

@app.route("/config/zero", methods=['GET'])
def get_zero():
    return triangulator.zero_zero

@app.route("/esp", methods=['POST'])
def new_esp():
    args = request.args
    id = args.get("id")
    lat = args.get("lat")
    lon = args.get("lon")
    if not (id and lat and lon):
        abort(404)
    triangulator.add_esp([float(lat), float(lon)], id)
    return "OK", 200

@app.route("/remove/esp", methods=['POST'])
def remove_esp():
    args = request.args
    id = args.get("id")
    result = triangulator.remove_esp(id)
    if result:
        return "OK", 200
    return "Not Found", 404

def update_constant():
    while True:
        triangulator.run_once(TIME_OVERRIDE if TIME_OVERRIDE else (time.time() - 2.5), bounds=2.5)
        time.sleep(5)

start_new_thread(update_constant, ())