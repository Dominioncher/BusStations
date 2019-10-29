from pymongo import MongoClient


connection = MongoClient("mongodb+srv://BusStation:BusStation@flamber-mongodb-pjxiq.mongodb.net/test?retryWrites=true&w=majority")
db = connection['BusStation']