from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

DATABASE_URI = "mongodb+srv://history:history@cluster0.hdcm5eu.mongodb.net/?retryWrites=true&w=majority"

mongo = MongoClient(DATABASE_URI)
dbname = mongo.zerotwodb
