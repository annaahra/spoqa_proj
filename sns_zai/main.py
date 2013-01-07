from __future__ import with_statement
# all the imports
import psycopg2
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_, or_
from Model import app, db, User1, Board, Friend
import md5

# configuration
DATABASE = 'SNS_Database'
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
#app = Flask(__name__)
app.config.from_object(__name__)
db.create_all()

def session_list_renewal():
    query = db.session.query(Friend.friend_email).filter(Friend.email == session['email'])
    user_list = db.session.query(User1.email).filter(not_(User1.email.in_(query)),User1.email != session['email'])
    friend_list = db.session.query(Friend.friend_email).filter(Friend.email == session['email'])
    post_list = db.session.query(Board).filter(or_(Board.email == session['email'],Board.email.in_(query)))
    session['user_list'] = user_list.all()
    session['friend_list'] = friend_list.all()
    session['post_list'] = post_list.all()
                
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not request.values['email'] or not request.values['password']:
            flash('Failed to login')
            return redirect(url_for('index'))
        else:
            email = request.values['email']
            password = md5.md5(request.values['password']).hexdigest()
            result = User1.query.filter_by(email = email, password = password).first()
            if result:
                session['logged_in'] = True
                session['email'] = email
                #friend_list = User1.query.filter(User1.email != session['email'])
                #flash('You were logged in id:' + session['id'])
                #session['friend_list'] = friend_list.all()
                session_list_renewal()
                
                return render_template('index.html')
            else:
                flash('ID or PASSWORD is wrong')
                return redirect(url_for('index'))
    elif request.method == 'GET':
        if session['logged_in']:
            friend_list = User1.query.filter(User1.email != session['email'])
            #flash('You were logged in id:' + session['id'])
            session['friend_list'] = friend_list.all()
            return render_template('index.html')
    return render_template('index.html', error=error)
#
#@app.route('/get_cft', methods=['POST'])
#def get_cft():
#    return
#
#@app.route('/get_sft', methods=['POST'])
#def get_sft():
#    friend_list = User1.query.filter(User1.email != session['id'])
#    return friend_list.all()
#
#@app.route('/get_post', methods=['POST'])
#def get_post():
#    return


@app.route('/logout')
def logout():
    session.pop('friend_list', None)
    session.pop('email', None)
    session.pop('logged_in', None)
    session.clear()
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/join', methods=['GET', 'POST'])
def join():
    if not request.values['name'] or not request.values['email'] or not request.values['password'] or not request.values['password1']:
        flash('Invalid')
        return redirect(url_for('index'))
    
    else:
        password = md5.md5(request.values['password']).hexdigest()
        password1 = md5.md5(request.values['password1']).hexdigest()
        
        if password != password1:
            flash('Password not matched')
            return redirect(url_for('join'))
        else:
            email = request.values['email']
            confirm_email = User1.query.filter_by(email = email).first()
        
            if confirm_email:
                flash('E-mail already exists')
                return redirect(url_for('join'))
            else:
                email = request.values['email']
                name = request.values['name']
                new_account = User1(email,name,password)
                db.session.add(new_account)
                db.session.commit()
  
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/addFriend', methods=['POST'])
def addFriend():
    friend_list = request.form.getlist('user')

    for friend in friend_list:
        friend_add = Friend(session['email'],friend)
        db.session.add(friend_add)
        db.session.commit()
    session_list_renewal()
#    return render_template('index.html')
    return redirect(url_for('index'))
    
@app.route('/post', methods=['POST'])
def post():
    if not session['email'] or not request.values['post']:
        flash('Invalid access')
        return redirect(url_for('index'))
    else:
        post = Board(session['email'],request.values['post'])
        db.session.add(post)
        db.session.commit()
        flash('post works')
    session_list_renewal()
#    return render_template('index.html')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
