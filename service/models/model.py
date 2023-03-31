from service import db

# Setup init.py file
# A model is a class that represents a table or collection in our DB, and where every attribute of the class is a field of the table or collection.

class Relationships(db.Model):

    __tablename__ = 'relationships'

    id = db.Column(db.Integer,primary_key=True)
    input_one = db.Column(db.Text)
    input_two = db.Column(db.Text)
    correlation = db.Column(db.Integer)


    def __init__(self, input_one, input_two):

        self.input_one = input_one
        self.input_two = input_two

    def __repr__(self):

        text = f"The relationship between {self.input_one} and {self.input_two} is {self.correlation}."

        return text


db.create_all()
db.session.commit()
