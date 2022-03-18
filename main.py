from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pickle


#Create Flask instance
app = Flask(__name__)
#create a secret key
app.config["SECRET_KEY"] = "much_secret"

#Create a Form Class
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