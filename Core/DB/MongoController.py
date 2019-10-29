from pymongo import MongoClient


connection = MongoClient("mongodb+srv://BusStation:BusStation@busstations-fcpis.mongodb.net/test?retryWrites=true&w=majority")
db = connection['BusStation']