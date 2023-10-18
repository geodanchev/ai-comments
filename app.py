#!/bin/python3
import json
import os
from helpers.xml_processing import xml_to_object
from helpers.azure_openai import get_feedback_temperament_and_category
from helpers.db import store_customer_feedback, retrieve_customer_feedbacks
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = ["xml"]
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")


@app.route("/")
def home():
    return render_template("home.html")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route("/preview", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect("/")

    file = request.files["file"]

    if file.filename == "":
        redirect("/")

    if file and allowed_file(file.filename):
        file_content = file.read()
        xml_string = file_content.decode('utf-8')
        xml_string = xml_string.replace('\\r\\n', '\n').replace("\\'", "'")

        return render_template('preview.html', content=xml_string)
    else:
        return "Error"


@app.route('/process', methods=['POST'])
def process():
    content = request.form.get('content')
    feedbacks = xml_to_object(content)
    print(content, feedbacks)

    for feedback in feedbacks:
        comment = feedback["comment"]
        additional_properties = json.loads(
            get_feedback_temperament_and_category(comment))
        feedback.update(additional_properties)
        store_customer_feedback(feedback)

    return redirect("draw")


@app.route("/draw", methods=["GET"])
def render_chart():
    feedback = retrieve_customer_feedbacks()
    return render_template('draw.html', context=json.loads(json.dumps(feedback, default=str)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
