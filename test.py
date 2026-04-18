from mongoDB import appointments_collection

appointments_collection.insert_one({
    "test": "working"
})

print("Inserted")