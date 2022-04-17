from os import environ as env

MONGO_HOST=env.get("MONGO_HOST")
MONGO_DB=env.get("MONGO_DB")
MONGO_USER=env.get("MONGO_USER")
MONGO_PASS=env.get("MONGO_PASS")
MONGO_SSL=True

MONGO_FRAMES_COLLECTION=env.get("MONGO_FRAMES_COLLECTION")
MONGO_ESP_COLLECTION=env.get("MONGO_ESP_COLLECTION")
MONGO_OUTPUT_COLLECTION=env.get("MONGO_OUTPUT_COLLECTION")
MONGO_COMMAND_COLLECTION=env.get("MONGO_COMMAND_COLLECTION")

TRIANGULATION_ZERO=env.get("TRIANGULATION_ZERO")
TRIANGULATION_ENV_FACTOR=env.get("TRIANGULATION_ENV_FACTOR")
TRIANGULATION_ONE_METER_RSSI=env.get("TRIANGULATION_ONE_METER_RSSI")