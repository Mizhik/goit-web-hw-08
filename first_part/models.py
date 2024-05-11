from mongoengine import connect, Document, StringField, ListField, ReferenceField, CASCADE

connect(
    db="goit_hw",
    host="mongodb+srv://mizhik:mizhik@cluster0.vnlh5xl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}

class Quote(Document):
    tags = ListField(StringField(max_length=20))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"collection": "quotes"}
