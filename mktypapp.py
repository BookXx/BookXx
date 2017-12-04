from flask import Flask, render_template, request
app = Flask(__name__)
from datetime import datetime

@app.route('/')
def main():
	return render_template("main.html")

@app.route('/buy')
def buy():
	return render_template('buy.html')

@app.route('/sell')
def sell():
	return render_template('sell.html')

@app.route('/pitch')
def pitch():
	return render_template('pitch.html')


@app.route('/formdemo')
def formdemo():
	return render_template('formdemo.html')


@app.route('/rent')
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
    app.run('0.0.0.0',port=3000)
