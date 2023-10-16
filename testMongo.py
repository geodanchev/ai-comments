from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://geodanchev:Adidas@goshtest.9fabnmm.mongodb.net/?retryWrites=true&w=majority&tlsCAFile=.\certificate\isrgrootx1.pem"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)