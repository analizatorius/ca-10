import flask as Flask


app = Flask(__name__)


@app.route('/')
def home(name):
    people = ["Jonas", "Ketras"]
    return render_template("index.html", people=people, page_title="INDEX")

@app.route("/<name>")
def home(name):
    return f"Cia tavo {name}, imk"

#@app.route()

if __name__ == '__main__':
    app.run(debug=True)
