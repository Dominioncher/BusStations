from pymongo import MongoClient
import pandas as pd

connection = MongoClient(
    "mongodb+srv://BusStation:BusStation@busstations-fcpis.mongodb.net/test?retryWrites=true&w=majority")
db = connection['BusStation']
db_routes = db["routes"]
db_checkpoints = db["checkpoints"]
db_checkpoints_distances = db["checkpoints_distances"]
