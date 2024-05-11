from mongoengine import connect, StringField,BooleanField, Document

connect(
    db="goit_hw",
    host="mongodb+srv://mizhik:mizhik@cluster0.vnlh5xl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

class User(Document):
    fullname = StringField(required=True, unique=True) 
    email = StringField(max_length=100)
    completed = BooleanField(default=False)
