from Core.DB.MongoController import db
from Core.DataLoaders.DataLoader import get_checkpoints


# Добавили остановки
checkpoints = get_checkpoints()
db.drop_collection('checkpoints')
db.create_collection('checkpoints')
db['checkpoints'].insert_many(checkpoints)
