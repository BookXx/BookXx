from flask import Flask, render_template, request
app = Flask(__name__)


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


if __name__ == '__main__':
    app.run('0.0.0.0',port=3000)
