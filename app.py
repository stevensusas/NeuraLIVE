from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import flask
import os
from werkzeug.utils import secure_filename
import zipfile
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from cell_count import count_cells

app = Flask(__name)

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXTENSIONS = {'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'zip_file' not in request.files:
        return redirect(request.url)

    file = request.files['zip_file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        zip_filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(zip_filename)

        # Extract images from the uploaded ZIP file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(app.config['UPLOAD_FOLDER'])

        # Process the images
        results = []
        image_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.tif'))

        for image_file in image_files:
            image = cv2.imread(image_file, cv2.IMREAD_COLOR)
            num_cells = count_cells(image)
            results.append(num_cells)

        # Create a scatter plot
        plt.scatter(range(1, len(image_files) + 1), results, marker='o', s=30, c='b', label='Data Points')
        plt.xlabel('Image Order')
        plt.ylabel('Number of Cells')
        plt.title('Cell Count')
        plt.grid(True)
        plt.legend()

        # Save the plot as an image
        graph_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'cell_count.png')
        plt.savefig(graph_filename)
        plt.close()

        return render_template('results.html', graph='/' + graph_filename)

if __name__ == '__main':
    app.run(debug=True)
