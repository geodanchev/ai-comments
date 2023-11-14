#!/bin/python3
import json
import os
from helpers.xml_processing import xml_to_object
from helpers.azure_openai import get_feedback_temperament_and_category, summarize_transcript
from helpers.db import store_customer_feedback, retrieve_customer_feedbacks
from helpers.webvtt_processing import read_vtt_file_from_request_content
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = ["xml", "vtt", "str", "sbv"]
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")


@app.route("/")
def home():
    return render_template("home.html")


def get_file_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower()

# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route("/preview", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect("/")

    file = request.files["file"]

    if file.filename == "":
        redirect("/")
    if file:
        fex = get_file_extension(file.filename)
        if fex and fex in app.config["ALLOWED_EXTENSIONS"]:
            match fex:
                case "xml":
                    content = {
                        'text': file.read().decode('utf-8').replace('\\r\\n', '\n').replace("\\'", "'"),
                        'operation':'process'
                    }
                    return render_template('preview.html', content=content)
                case "vtt" | "str" | "sbv":
                    content = {
                        'text':read_vtt_file_from_request_content(file.read(), fex),
                        'operation':'process2'
                    }
                    return render_template('preview.html', content=content)

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

@app.route('/process2', methods=['POST'])
def process2():
    content = request.form.get('content')
    
    return render_template('resultprocess2.html', content=summarize_transcript(content))

@app.route("/draw", methods=["GET"])
def render_chart():
    feedback = retrieve_customer_feedbacks()
    return render_template('draw.html', context=json.loads(json.dumps(feedback, default=str)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
