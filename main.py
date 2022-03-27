from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pickle


# Create Flask instance
app = Flask(__name__)
# Add DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# Create a secret key
app.config["SECRET_KEY"] = "much_secret"


# Initialize DB
db = SQLAlchemy(app)
# Create DB model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create string
    def __repr__(self):
        return "<Name %r>" % self.name

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Insert valid email")])
    submit = SubmitField("submit")


#Create a Form Class for name html
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("submit")
#create form for iris
class IrisData(FlaskForm):
    sepal_length = StringField("Sepal length", validators=[DataRequired()])
    sepal_width = StringField("Sepal width", validators=[DataRequired()])
    petal_length = StringField("Petal length", validators=[DataRequired()])
    petal_width = StringField("Petal width", validators=[DataRequired()])
    submit = SubmitField("submit")


#Create route decorator for index
@app.route('/')
def index():
    info = "not the best but good"
    bold_tag = "this is <strong> Bold </strong> tag"
    return render_template("index.html", info=info, bold_tag=bold_tag)

@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        #checks if user with email already exists if not, proceeds
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User added successfully")

    all_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, all_users=all_users)


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

#Create name page
@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form submitted successfully")
    return render_template("name.html", name=name, form=form)

#Machine learning assignemnt
@app.route("/iris", methods=["GET"])
def iris():
    form = IrisData()
    return render_template("iris.html", form=form)


@app.route("/iris", methods=["POST"])
def iris_post():
    form = IrisData()


    sepal_length = form.sepal_length.data
    sepal_width = form.sepal_width.data
    petal_length = form.petal_length.data
    petal_width = form.petal_width.data

    prediction = iris_prediction([sepal_length, sepal_width, petal_length, petal_width])
    prediction = str(prediction[0])


    if prediction == "setosa":
        image = "https://en.wikipedia.org/wiki/Iris_setosa#/media/File:Irissetosa1.jpg"
    elif prediction == "virginica":
        image = "https://upload.wikimedia.org/wikipedia/commons/f/f8/Iris_virginica_2.jpg"
    else:
        image = "https://en.wikipedia.org/wiki/Iris_versicolor#/media/File:Blue_Flag,_Ottawa.jpg"

    if form.validate_on_submit():
        return render_template("iris_result.html", form=form, prediction=prediction, image=image)
    else:
        return render_template("iris.html", form=form)

def iris_prediction(iris_data : list):
    pickled_model = open('iris_predictor.pickle', 'rb')
    model = pickle.load(pickled_model)
    prediction = model.predict([iris_data])

    return prediction


if __name__ == '__main__':
    app.run(debug=True)