import os
from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
from clm.models import db, Contact
from sqlalchemy import update

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '847rc0ruprguew09grywe8457398un9xfnhf7h302-3ru1430ntq=4r84230t723ct3'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)
db.create_all()
db.session.commit()

# admin = Contact(name='admin', email='admin@example.com', phone='111-111-1111')
# guest = Contact(name='guest', email='guest@example.com', phone='222-222-2222')

# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()

@app.route("/")
def welcome():
    '''
    Home page
    '''
    return render_template('web/index.html')

@app.route("/portfolio")
def portfolio():
    '''
    Guillermo's Portfolio
    '''
    return render_template('web/portfolio.html')

@app.route("/contact/add", methods=('GET','POST'))
def new_contact():
    '''
    Create new contact
    '''
    nameCheck = request.args.get('name')
    emailCheck = request.args.get('email')
    if request.method == 'POST':
        if nameCheck or emailCheck:
            existing_contact = Contact.query.filter(Contact.name == nameCheck or Contact.email == emailCheck).first()
            if existing_contact:
                return make_response(f'{name} ({email}) already created!')
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone'] # Create an instance of the Contact class
        new_contact = Contact(name=name, surname=surname, email=email, phone=phone)    
        db.session.add(new_contact) # Adds new Contact record to database
        db.session.commit() # Commits all changes

        return redirect('/contacts')
    else:
        
        return render_template('web/new_contact.html')


@app.route("/contact/delete/<int:id>", methods=('POST',))
def contact_delete(id):
    '''
    Delete contact
    '''
    to_delete = Contact.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()

    return redirect('/contacts')


@app.route("/contact/update/<int:id>", methods=['GET', 'POST'])
def update_contact(id):
    '''
    Edit contact
    '''
    to_edit = Contact.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.name = request.form['name']
        to_edit.surname = request.form['surname']
        to_edit.email = request.form['email']
        to_edit.phone = request.form['phone']
        db.session.commit()
        return redirect('/contacts')

    else:
        return render_template('web/edit_contact.html', data=to_edit)


@app.route("/contacts")
def display_contacts():
    '''
    Show alls contacts
    '''
    # session = db.session()
    # cursor = session.execute('SELECT * FROM contacts').cursor
    # data = cursor.fetchall()
    
    all_contacts = Contact.query.order_by(Contact.id).all()
    return render_template('web/contacts.html', output_data = all_contacts)


@app.route("/contacts/", methods=['GET'])
def contacts_search():
    '''
    Search
    '''
    if request.method=="GET":
        query = request.args.get("search")

        if Contact.query.filter(Contact.name == query).all() != None:
            results = Contact.query.filter(Contact.name == query).all()
            return render_template('web/result.html', results_data = results)     
        else:
            return redirect('/contact/add', results_data = query)
            
          
    
        



if __name__ == "__main__":
    app.run(port=3000)
