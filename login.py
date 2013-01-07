'''
Created on 2013. 1. 7.

@author: Anna
'''

from flask import Flask, session, redirect, url_for, escape, request, render_template
from CreateUserDB import db, SnsUser

app = Flask(__name__)
db.create_all()

@app.route('/')
def index():
    if 'email' in session:
        return 'Logged in as %s' % escape(session['email'])
    return 'You are not logged in'

@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    mail = request.form['email']
    pwd = request.form['password']
    session['email'] = mail
    for email in db.session.query(SnsUser.email).filter(SnsUser.email==mail):
        if db.session.query(SnsUser.password).filter(SnsUser.password==pwd):
            return redirect(url_for('index'))    
        else:
            return redirect(url_for('logout'))    
                                 
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)