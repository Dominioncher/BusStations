from pymongo import MongoClient


connection = MongoClient("mongodb+srv://BusStation:<password>@busstations-fcpis.mongodb.net/test?retryWrites=true&w=majority")
db = connection['BusStations']