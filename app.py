import os
from flask import Flask, flash, render_template, request
from groq import Groq
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"txt"}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "capstone-flask-secret-2026")


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def summarize_text(text: str) -> str:
    api_key = os.environ.get(
        "GROQ_API_KEY",
        "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",
    )
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured. Please set it in your environment.")

    client = Groq(api_key=api_key)
    prompt = (
        "Summarize the following text clearly and concisely. "
        "Use short paragraphs and, when appropriate, bullet points.\n\n"
        f"{text}"
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes user-provided text.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=600,
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Groq returned an empty summary.")
    return content.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    original_text = ""
    summary = ""

    if request.method == "POST":
        if "text_file" not in request.files:
            flash("No file was sent. Please choose a .txt file.", "error")
            return render_template("index.html", original_text=original_text, summary=summary)

        file = request.files["text_file"]

        if not file or file.filename == "":
            flash("No file selected. Please upload a .txt file.", "error")
            return render_template("index.html", original_text=original_text, summary=summary)

        safe_name = secure_filename(file.filename)
        if not allowed_file(safe_name):
            flash("Invalid file type. Please upload a .txt file only.", "error")
            return render_template("index.html", original_text=original_text, summary=summary)

        try:
            original_text = file.read().decode("utf-8").strip()
        except UnicodeDecodeError:
            flash("The file must be UTF-8 encoded text.", "error")
            return render_template("index.html", original_text=original_text, summary=summary)

        if not original_text:
            flash("The uploaded file is empty. Please upload a file with text content.", "error")
            return render_template("index.html", original_text=original_text, summary=summary)

        try:
            summary = summarize_text(original_text)
            flash("Summary generated successfully.", "success")
        except Exception as exc:
            flash(f"Failed to generate summary: {exc}", "error")

    return render_template("index.html", original_text=original_text, summary=summary)


@app.errorhandler(413)
def request_entity_too_large(_error):
    flash("File is too large. Maximum allowed size is 2 MB.", "error")
    return render_template("index.html", original_text="", summary=""), 413


if __name__ == "__main__":
    app.run(debug=True)
