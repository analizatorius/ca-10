from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    info = "not the best but good"
    bold_tag = "this is <strong> Bold </strong> tag"
    return render_template("index.html", info=info, bold_tag=bold_tag)

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

#create custum ERROR pages

#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#internal server error
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)