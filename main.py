from flask import Flask, request
from faker import Faker

fake = Faker()

app = Flask(__name__)


@app.route("/")
def index():
    return "Index Page"


@app.route("/requrements/")
def requirements():
    file_name = "requirements.txt"

    try:
        with open(file_name, "r") as file:
            content = file.read()
            substrings = content.split()
            content = "<br>".join(substrings)
        return content

    except FileNotFoundError:
        return "File not found."


@app.route("/users/generate")
def user_generator():
    quantity = request.args.get("quantity")

    if quantity is None:
        total_quantity = 100
    else:
        try:
            total_quantity = int(quantity)
            if not (0 <= total_quantity <= 100):
                return "Parameter is out of range. It should be between 0 and 100.", 400
        except ValueError:
            return "Parameter is not an integer.", 400

    result = ""
    for i in range(total_quantity):
        result += str(i + 1) + ". " + fake.name() + " " + fake.email() + "<br>"
    return result
