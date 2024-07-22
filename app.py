from flask import Flask, render_template, redirect, url_for, session, request
from datetime import datetime
import csv
from forms import LoginForm, QuestionnaireForm  # Make sure to import your LoginForm
import random
import copy
import pandas as pd


ROUND_ROBIN_CSV_FILE_PATH = "round_robin__melted_50p_2s_120f_30r_Shuffled_Exploded.csv"


## initialising the app
app = Flask(__name__)

# We need a secret key for the session...
app.config["SECRET_KEY"] = ("a3c2c89e8d2be872c1362d323970a90d5e15f9ecafec2f789ca256394660186b")

@app.route("/")
def hello(): # we go to login-directly
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():


    form = LoginForm() # creating an object

    if form.validate_on_submit():
        session["participant_id"] = form.unique_id.data
        session["s_id"] = "sess-" + form.session_id.data

        # Check if session ID is "sess-1" and skip to rating
        if session.get("s_id") == "sess-1":
            return redirect(url_for("start_rating"))

        # session can be 0 or 1. If it's 1, we don't need to train the individual again (already done once),
        # so we directly skip to the training


        # if session is sess-0 then explain how the process will work and also do the training sesison.
        return redirect(url_for("process_explanation"))

    # if the loginform is invalid, rended the loginform once again.
    return render_template("login.html", form=form)


@app.route("/process_explanation")
def process_explanation():
    return render_template("process_explanation.html")


@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    form = QuestionnaireForm()

    if form.validate_on_submit():
        responses = {
            "age": form.age.data,
            "Gender": form.gender.data,
            "Vision": f"{form.vision.data}",
            "Color": f"{form.colorblind.data}",
            "AI Exposure": f"{form.aiexposure.data}",
        }

        filename = f"{session['participant_id']}_questionnaire_responses.txt"

        with open(filename, "w") as file:
            for question, response in responses.items():
                file.write(f"{question}: {response}\n")

        # start the training of the individual once the responses are recorded in a text file
        return redirect(url_for("start_training"))

    # re-render the same HTML if its a incorrectly validated form
    return render_template("questionnaire.html", form=form)


@app.route("/start_training")
def start_training():
    return render_template("start_training.html")


@app.route("/training", methods=["GET", "POST"])
def training():
    train_images = [
        {"filename": "Bad.png", "description": "Bad image"},
        {"filename": "Poor.jpeg", "description": "Poor image"},
        {"filename": "Fair.jpeg", "description": "Fair image"},
        {"filename": "Good.png", "description": "Good image"},
        {"filename": "Excellent.png", "description": "Excellent image"},
    ]

    if "current_image_index" not in session:
        session["current_image_index"] = 0
    else:
        if request.method == "POST":
            session["current_image_index"] += 1

    if session["current_image_index"] >= len(train_images):
        session.pop("current_image_index", None)
        return redirect(url_for("end_training"))

    next_image = train_images[session["current_image_index"]]

    return render_template("training2.html", image_info=next_image)


@app.route("/end_training")
def end_training():
    return render_template("end_training.html")


@app.route("/start_rating")
def start_rating():
    return render_template("start_rating.html")




# Load the CSV file with the image data

# To rate the images, using the following CSV file
df = pd.read_csv(f"./{ROUND_ROBIN_CSV_FILE_PATH}")


@app.route("/rate_image", methods=["GET", "POST"])
def rate_image():

    if "images_rated" not in session:
        session["images_rated"] = []
        session["current_image_index"] = 0

    p_id = session["participant_id"]
    sess = session["s_id"]

    images = df[(df["p-id"] == p_id) & (df["sess"] == sess)].reset_index()

    if request.method == "POST":
        # Process the rating for the current image
        rating = request.form["rating"]
        time_spent = request.form["time_spent"]
        current_image_index = session.get("current_image_index", 0)

        if current_image_index < len(images):
            img = images.iloc[current_image_index]["img"]
            # Write the rating to CSV
            with open("ratings.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        p_id,
                        sess,
                        img,
                        rating,
                        time_spent,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ]
                )

            session["images_rated"].append(img)

            # Increment the index here before fetching the next image
            session["current_image_index"] = current_image_index + 1

    # Fetch the next image to display after the index has been incremented
    current_image_index = session.get("current_image_index", 0)
    if current_image_index >= len(images):
        # All images have been rated
        return redirect(url_for("complete"))

    # Fetch and display the next image
    next_img = images.iloc[current_image_index]["img"]

    return render_template("rate_image.html", image_file=next_img)


@app.route("/complete")
def complete():
    rated_images = session.get("images_rated", [])

    count = len(rated_images)

    return render_template(
        "complete2.html",
    )


@app.route("/end_session")
def end_session():
    session.clear()
    return "bye"


if __name__ == "__main__":
    app.run(debug=True)
