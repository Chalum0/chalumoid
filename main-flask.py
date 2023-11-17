from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/<name>/<second>", methods=["GET"])
def form(name, second):
    print(name, second)
    return render_template("index.html")


if __name__  == "__main__":
    app.run(debug=True)
