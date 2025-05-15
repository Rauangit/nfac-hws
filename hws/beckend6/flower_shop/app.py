from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Flower, Purchase
from repositories import UsersRepository, FlowersRepository, PurchasesRepository
import os

app = Flask(__name__)
app.secret_key = 'secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
jwt = JWTManager(app)

@app.route("/")
def home():
    return "Welcome to the Flower Shop!"

@app.route("/signup")
def signup_form():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    full_name = request.form["full_name"]
    password = generate_password_hash(request.form["password"])
    photo = request.files["photo"]

    filename = photo.filename
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(photo_path)

    user = User(email, full_name, password, filename)
    UsersRepository.add(user)
    return redirect("/login")

@app.route("/login")
def login_form():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    user = UsersRepository.find_by_email(email)

    if not user or not check_password_hash(user.password_hash, password):
        return "Неверный логин или пароль", 401

    access_token = create_access_token(identity=user.id)
    response = make_response(redirect("/profile"))
    response.set_cookie("access_token", access_token)
    return response


@app.route("/profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = UsersRepository.get_by_id(user_id)
    return render_template("profile.html", user=user)


@app.route("/flowers")
def show_flowers():
    return render_template("flowers.html", flowers=FlowersRepository.all())


@app.route("/flowers", methods=["POST"])
def add_flower():
    name = request.form["name"]
    quantity = int(request.form["quantity"])
    price = float(request.form["price"])
    flower = Flower(name, quantity, price)
    FlowersRepository.add(flower)
    return redirect("/flowers")


@app.route("/cart/items", methods=["POST"])
def add_to_cart():
    flower_id = request.form["flower_id"]
    cart = request.cookies.get("cart", "")
    cart_items = cart.split(",") if cart else []
    cart_items.append(flower_id)
    response = redirect("/flowers")
    response.set_cookie("cart", ",".join(cart_items))
    return response


@app.route("/cart/items")
def show_cart():
    cart = request.cookies.get("cart", "")
    cart_items = cart.split(",") if cart else []
    flowers = [FlowersRepository.get(int(f)) for f in cart_items if FlowersRepository.get(int(f))]
    total = sum(f.price for f in flowers)
    return render_template("cart.html", flowers=flowers, total=total)


@app.route("/purchased", methods=["POST"])
@jwt_required()
def purchase_flowers():
    user_id = get_jwt_identity()
    cart = request.cookies.get("cart", "")
    flower_ids = cart.split(",") if cart else []
    for fid in flower_ids:
        flower = FlowersRepository.get(int(fid))
        if flower:
            PurchasesRepository.add(Purchase(user_id, flower.id))
    response = redirect("/purchased")
    response.set_cookie("cart", "", expires=0)
    return response


@app.route("/purchased")
@jwt_required()
def show_purchased():
    user_id = get_jwt_identity()
    purchases = PurchasesRepository.for_user(user_id)
    flowers = [FlowersRepository.get(p.flower_id) for p in purchases]
    return render_template("purchased.html", flowers=flowers)

