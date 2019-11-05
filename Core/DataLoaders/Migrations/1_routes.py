from Core.DB.MongoController import db
from Core.DataLoaders.DataLoader import get_routes

# Добавили маршруты
routes = get_routes()
db.drop_collection('routes')
db.create_collection('routes')
db['routes'].insert_many(routes)
