import random
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'our secret'

celebrities_images = [
    'Paris_Hilton.jpg',
    'Clooney_George.jpg'
]

celebrities_features = [
    ['female', ],
    ['male', ]
]


@app.route("/i")
def interface(exclude=None):

    i = random.randint(0, len(celebrities_images)-1)
    if exclude is not None:
        safe_guard=0
        while exclude == i or safe_guard > 10:
            safe_guard += 1
            i = random.randint(0, len(celebrities_images)-1)

    return render_template('interface.html', image=celebrities_images[i], index=i)


@app.route("/select/<index>/<context>")
def select(index, context):
    # do something with index
    if "name" in session:
        logfile = open("log/"+session["name"], 'a')
        logfile.write(index+','+context)
        logfile.write("\n")

        return interface()


@app.route("/game", methods=['POST', 'GET'])
def game():
    if request.method == 'POST':
        session["name"] = request.form['name']

    if "name" in session:
        return render_template('layout.html', name=session["name"])
    else:
        return redirect(url_for('index'))


@app.route("/quit")
def quit():
    session.pop('name', None)
    return redirect(url_for('index'))


@app.route("/")
def index():
    return render_template('start.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
