from flask import Flask, render_template, request, send_from_directory
from reddit_analysis import fetch_and_analyze_data, generate_graph
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    context = {"result": None, "image": None}
    
    if request.method == "POST":
        product = request.form.get("product")
        year = request.form.get("year")
        option = request.form.get("option")

        try:
            result, image_path = fetch_and_analyze_data(product, year, option)
            context = {
                "result": result,
                "image": image_path,
                "product": product,
                "year": year,
                "selected_option": option
            }
        except Exception as e:
            context["result"] = f"Error: {str(e)}"

    return render_template("index.html", **context)

@app.route("/static/plots/<path:filename>")
def serve_image(filename):
    return send_from_directory("static/plots", filename)

if __name__ == "__main__":
    os.makedirs("static/plots", exist_ok=True)
    app.run(debug=True)
