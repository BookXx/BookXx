"""
    BookXx
	Developers:

	To run this you need to execute the following shell commands
	% pip3 install flask
	% pip3 install flash_oauthlib
	% python3 mktypapp.py

	For windows just don't type the "3"s

    The authentication comes from an app by Bruno Rocha
    GitHub: https://github.com/rochacbruno
"""
from functools import wraps
from flask import Flask, redirect, url_for, session, request, jsonify, render_template, request
from flask_oauthlib.client import OAuth
from datetime import datetime

app = Flask(__name__)
#gracehopper.cs-i.brandeis.edu:5000
#app.config['GOOGLE_ID'] = '783502545148-f4a0ss6kdf839iekmreq1inl2lqnhaqt.apps.googleusercontent.com'
#app.config['GOOGLE_SECRET'] = '9WksdPKQfOG77hO3DDteRFYr'

#127.0.0.1:5000
app.config['GOOGLE_ID'] = '246096591118-ti33uv184e4m1bib9grgn8alm45btadb.apps.googleusercontent.com'
app.config['GOOGLE_SECRET'] = 'iqgLqu6pXgLuHsZFq6nvxDX3'

#gracehopper.cs-i.brandeis.edu:5200
#app.config['GOOGLE_ID'] = '246096591118-ti33uv184e4m1bib9grgn8alm45btadb.apps.googleusercontent.com'
#app.config['GOOGLE_SECRET'] = 'iqgLqu6pXgLuHsZFq6nvxDX3'

app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not('google_token' in session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/main')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        print("logged in")
        print(jsonify(me.data))
        return render_template("main.html")
        #return jsonify({"data": me.data})
    print('redirecting')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    #
    return redirect(url_for('main'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    print(session['google_token'])
    me = google.get('userinfo')
    session['userinfo'] = me.data
    print(me.data)
    return render_template("main.html")
    #return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')




@app.route('/')
def main():
	return render_template("main.html")

@app.route('/buy')
@require_login
def buy():
	return render_template('buy.html')

@app.route('/sell')
@require_login
def sell():
	return render_template('sell.html')

books=[]
bookCounter=0

@app.route('/processSell',methods=['GET','POST'])
@require_login
def processSell():
	global books
	global bookCounter
	if request.method == 'POST':
		userinfo = session['userinfo']
		who = userinfo['email']
		t = request.form['title']
		cou = request.form['course']
		l = request.form['link']
		con = request.form['condition']
		p = request.form['price']
		d = request.form['description']
		n = datetime.now()

		book = {
            'id':bookCounter,
            'title':t,
            'course':cou,
            'link':l,
            'condition':con,
            'price':p,
            'description':d,
			'when':n,
			'who':who
            }
		bookCounter = bookCounter + 1
		books.insert(0,book) # add msg to the front of the list

	return render_template("booksForSale.html",books=books)



@app.route('/booksForSale')
def booksForSale():
	global books
	print("in booksForSale")
	print(books)
	return render_template('booksForSale.html',books=books)


@app.route('/removeBook',methods=['GET','POST'])
def takeOrder():
	global books
	if request.method == 'POST':
		userinfo = session['userinfo']
		who = userinfo['email']
		seller = request.form['who']
		num = request.form['id']
		newBooks = [x for x in books if not(x['who']==who and int(x['id'])==int(num)) ]
		print("newBooks=")
		print(newBooks)
		books = newBooks
	return render_template("booksForSale.html",books=books)



@app.route('/pitch')
def pitch():
	return render_template('pitch.html')


@app.route('/formdemo')
def formdemo():
	return render_template('formdemo.html')


@app.route('/rent')
@require_login
def rent():
	return render_template('rent.html')




@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/bio')
def bio():
	return render_template('bio.html')

@app.route('/staci')
def staci():
	return render_template('staci.html')

@app.route('/brianna')
def brianna():
	return render_template('brianna.html')

@app.route('/Lijep7')
def Lijep7():
	return render_template('Lijep7.html')

@app.route('/Ryan')
def ryan():
	return render_template('ryan.html')





messages=[]
@app.route('/chat',methods=['GET','POST'])
def chat():
	if request.method == 'POST':
		msg = request.form['msg']
		who = request.form['who']
		now = datetime.now()
		x = {'msg':msg,'now':now,'who':who}
		messages.insert(0,x) # add msg to the front of the list
		return render_template("chat.html",messages=messages)
	else:
		return render_template("chat.html",messages=[])

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)  #use 5000 for development on localhost 127.0.0.1
	#app.run('0.0.0.0',port=5200)  # use 5200 for production gracehopper
