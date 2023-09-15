from flask import Flask, request
from faker import Faker
import csv

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


@app.route("/mean/")
def mean():
    try:
        with open("hw.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            total_rows = 0
            sum_column1 = 0
            sum_column2 = 0

            for row in csv_reader:
                if len(row) >= 2:
                    try:
                        column1 = float(row[1])
                        column2 = float(row[2])
                        sum_column1 += column1
                        sum_column2 += column2
                        total_rows += 1
                    except ValueError:
                        continue  # Skip rows with non-numeric data in columns

            if total_rows == 0:
                return "No valid data found in the CSV file."

            average_column1 = round(sum_column1 / total_rows * 2.54, 2)
            average_column2 = round(sum_column2 / total_rows * 0.453592, 2)

            return f"Average of height: {average_column1} cm, Average of weight: {average_column2} kg"

    except FileNotFoundError:
        return "File not found."
