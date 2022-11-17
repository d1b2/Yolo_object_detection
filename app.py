
import argparse
import io
import os
from PIL import Image

import torch
import shutil

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]

        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        path_upload="static/uploaded/"
        
        if os.path.exists(path_upload):shutil.rmtree(path_upload)
        os.makedirs(path_upload)
        img.save("static/uploaded/image0.jpg")
        #results.save(save_dir="static/uploaded/")
        results = model([img])

        results.render()  # updates results.imgs with boxes and labels
       # os.makedirs
        #results.save("predicted.jpg")

        #mypath = "detcted"
        #for root, dirs, files in os.walk(mypath):
           # for file in files:
               # os.remove(os.path.join(root, file))
        path_detect="static/detected/"
        
        if os.path.exists(path_detect):shutil.rmtree(path_detect)
        
        results.save(save_dir="static/detected/")
        return render_template('result.html')
        #return redirect("static/image0.jpg")

    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    
    path = 'best.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom',path)
    model.eval()
    app.run(host="0.0.0.0", port=args.port,debug=True)  # debug=True causes Restarting with stat