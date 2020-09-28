import os
from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self):
        return "<Contact(id'%s' name='%s', surname='%s', email='%s', phone='%s')>" % (self.id, self.name, self.surname, self.email, self.phone)

        
class ContactSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        include_relationships = True
        load_instance = True
        
contact_schema = ContactSchema()
contact_schema = ContactSchema(many=True)









        

    