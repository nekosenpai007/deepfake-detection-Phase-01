from flask import Flask, request, jsonify, render_template_string
import cv2
import numpy as np
from detector import DeepfakeAnalyzer

app = Flask(__name__)
analyzer = DeepfakeAnalyzer()

HTML = """
<h2>Deepfake Detection – Classical Forensics</h2>

<h3>Compare Two Images</h3>
<form action="/api/compare" method="POST" enctype="multipart/form-data">
Original Image: <input type="file" name="original"><br><br>
Suspected Image: <input type="file" name="fake"><br><br>
<button type="submit">Analyze</button>
</form>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/compare", methods=["POST"])
def compare():
    img1 = cv2.imdecode(
        np.frombuffer(request.files["original"].read(), np.uint8),
        cv2.IMREAD_COLOR
    )
    img2 = cv2.imdecode(
        np.frombuffer(request.files["fake"].read(), np.uint8),
        cv2.IMREAD_COLOR
    )

    return jsonify(analyzer.compare_images(img1, img2))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
