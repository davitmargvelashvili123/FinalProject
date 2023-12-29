from flask import render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from forms import AddProductForm, RegisterForm, LoginForm, AddAnswerForm
from models import Product, User, Answer
from ext import app


library = "Flask 2,0"

role = "mod"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gods")
def gods():
    return render_template("gods.html")


@app.route("/heroes")
def heroes():
    return render_template("heroes.html")


@app.route("/creatures")
def creatures():
    return render_template("creatures.html")


@app.route("/zeus")
def zeus():
    return render_template("zeus.html")


@app.route("/poseidon")
def poseidon():
    return render_template("poseidon.html")


@app.route("/hades")
def hades():
    return render_template("hades.html")


@app.route("/perseus")
def perseus():
    return render_template("perseus.html")


@app.route("/theseus")
def theseus():
    return render_template("theseus.html")


@app.route("/medusa")
def medusa():
    return render_template("medusa.html")


@app.route("/hydra")
def hydra():
    return render_template("hydra.html")


@app.route("/heracles")
def heracles():
    return render_template("heracles.html")


@app.route("/pegasus")
def pegasus():
    return render_template("pegasus.html")


@app.route("/questions")
def questions():
    products = Product.query.all()
    return render_template("questions.html", products=products, role=role)


@app.route("/answers")
def answerer():
    answers = Answer.query.all()
    return render_template("answers.html", answers=answers, role=role)


@app.route("/product/<int:product_id>")
def view_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")
    return render_template("product.html", product=chosen_product, role=role)


@app.route("/answer/<int:answer_id>")
def view_answer(answer_id):
    chosen_answer = Answer.query.get(answer_id)
    if not chosen_answer:
        return render_template("404.html")
    return render_template("answer.html", answer=chosen_answer, role=role)


@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
@login_required
def edit_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")

    if current_user.username != "admin" and current_user.username != chosen_product.name:
        return redirect("/")

    form = AddProductForm(question=chosen_product.question, img=chosen_product.img)
    if form.validate_on_submit():
        chosen_product.question = form.question.data
        chosen_product.img = form.img.data.filename

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)

        chosen_product.save()
        return redirect("/questions")

    return render_template("add_product.html", form=form)


@app.route("/edit_answer/<int:answer_id>", methods=["POST", "GET"])
@login_required
def edit_answer(answer_id):
    chosen_answer = Answer.query.get(answer_id)
    if not chosen_answer:
        return render_template("404.html")

    if current_user.username != "admin" and current_user.username != chosen_answer.name:
        return redirect("/")

    form = AddAnswerForm(whoanswer=chosen_answer.whoanswer, answer=chosen_answer.answer)
    if form.validate_on_submit():
        chosen_answer.whoanswer = form.whoanswer.data
        chosen_answer.answer = form.answer.data

        chosen_answer.save()
        return redirect("/answers")

    return render_template("add_answer.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")

    if current_user.username != "admin" and current_user.username != chosen_product.name:
        return redirect("/")

    chosen_product.delete()
    return redirect("/questions")


@app.route("/delete_answer/<int:answer_id>")
@login_required
def delete_answer(answer_id):
    chosen_answer = Answer.query.get(answer_id)
    if not chosen_answer:
        return render_template("404.html")

    if current_user.username != "admin" and current_user.username != chosen_answer.name:
        return redirect("/")

    chosen_answer.delete()
    return redirect("/answers")


@app.route("/add_product", methods=["POST", "GET"])
@login_required
def add_product():

    form = AddProductForm()
    if form.validate_on_submit():
        new_product = Product(name=current_user.username, question=form.question.data, img=form.img.data.filename)
        new_product.create()

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)
        return redirect("/questions")
    return render_template("add_product.html", form=form)


@app.route("/add_answer", methods=["POST", "GET"])
@login_required
def add_answer():

    form = AddAnswerForm()
    if form.validate_on_submit():
        new_answer = Answer(name=current_user.username, whoanswer=form.whoanswer.data, answer=form.answer.data)
        new_answer.create()

        return redirect("/answers")
    return render_template("add_answer.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(User.username == form.username.data).first()
        if existing_user:
            flash("მომხმარებელი უკვე არსებობს")
        else:
            new_user = User(username=form.username.data, password=form.password.data, role="normal")
            new_user.create()
            return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")
