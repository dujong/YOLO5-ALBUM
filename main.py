import torch


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
img = 'https://ultralytics.com/images/zidane.jpg'
results = model(img)

import json

with open('tags_ko.json') as f:
    tags_ko = json.load(f)
    
from glob import glob

img_list = glob('static/photos/*.jpg')

db = {}

for img_path in img_list:
    results = model(img_path)
    
    tags = set()

    for pred in results.pred[0]:
        tag = results.names[int(pred[-1])] # English
#         tag = tags_ko[int(pred[-1])] # Korean
        tag = tag.replace(' ', '')
        tags.add(tag)
        
    db[img_path] = list(tags)


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('templates/index.html', photos=db)

if __name__ == '__main__':
    app.run()