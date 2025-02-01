from flask import Flask, request, render_template

app = Flask(__name__)
from upload import upload


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        file = request.files.get("file")

        file_content = file.read()

        if file_content:
            file_name = file.filename
            # Read file content as bytes

            print(f"File Name: {file_name}")

            download_link = upload(file_content, "Main.epub")
            return f"Received:  File Name={file_name},  <br> File Uploaded: <a href='{download_link}'>Download</a>"
        else:
            return "Uploaded Unsuccessful"

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
