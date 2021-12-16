from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/user')
def hello_user():
    return 'Hello, user!'

@app.route("/user/<name>")
def user(name):
    return f"<h>Hello {name}</h>"

if __name__ == '__main__':
    app.run(debug=True)