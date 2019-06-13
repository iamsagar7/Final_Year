import flask
from flask import Flask, render_template, request, request, redirect, jsonify, make_response, url_for, render_template, send_from_directory, flash
import natsort
import os, sys
from werkzeug.utils import secure_filename
app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'config','csv'])

app.config[
    'SECRET_KEY'] = '7\x9e\xcb5\xa4f!\r\xb5F\x8d\xb4\x02\xc5\xc1\x8a2<,\xda-\xdc\x1a\x854|\xc5\xa6\tZ\xc0\x81'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['UPLOAD_FOLDER'] = "/home/sagar/Desktop/Clustering-on-iris-data/static/files"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename == "kmean-config.config":
                file.save(
                    os.path.join(
                        '/home/sagar/Desktop/Clustering-on-iris-data/static/files/kmeans',
                        filename))
                CONFIG_kMEAN='/home/sagar/Desktop/Clustering-on-iris-data/static/files/kmeans/'+filename
                from kmeans import main
                main(CONFIG_kMEAN)

            elif filename=="meanshift-config.config":
                file.save(
                    os.path.join(
                        '/home/sagar/Desktop/Clustering-on-iris-data/static/files/meanshift',
                        filename))
                config_meanshift ='/home/sagar/Desktop/Clustering-on-iris-data/static/files/meanshift/'+filename
                from Meanshift import main
                main(config_meanshift)
            else:
                file.save(
                    os.path.join(
                        '/home/sagar/Desktop/Clustering-on-iris-data/static/csv',
                        filename))

            return redirect(request.url)
    return render_template('index.html')


def upload_meanshift():
    if request.method == 'POST':
        # check if the post request has the file part

        meanshift = request.files['meanshift']
        # if user does not select file, browser also
        # submit an empty part without filename
        if meanshift.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if meanshift and allowed_file(meanshift.filename):
            filename = secure_filename(meanshift.filename)
            meanshift.save(
                os.path.join(
                    '/home/sagar/Python/test/Final_Year/images/meanshift',
                    filename))

            return redirect(request.url)
    return render_template('index.html')


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images/kmeans", filename)

#kmean
@app.route('/kmeans')
def kmeans():
    image_names = os.listdir('./images/kmeans')
    image_names=natsort.natsorted(image_names)
    print(image_names)
    return render_template("kmeans.html", image_names=image_names)


@app.route('/upload/<filename>')
def send_image2(filename):
    return send_from_directory("images/meanshift", filename)

#meanshift
@app.route('/meanshift')
def meanshift():

    imag_names = os.listdir('images/meanshift')
    imag_names=natsort.natsorted(imag_names)
    print(imag_names)
    return render_template("meanshift.html", image_names=imag_names)


@app.route('/kmeans', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        mydir = '//home/sagar/Desktop/Clustering-on-iris-data/images/kmeans'
        for file in os.listdir(mydir):
            if file.endswith('.png'):
                os.remove(os.path.join(mydir, file))
                return redirect(request.url)
    return render_template('kmeans.html')


@app.route('/meanshift', methods=['POST', 'GET'])
def delete_shift():
    if request.method == 'POST':
        mydir = '/home/sagar/Desktop/Clustering-on-iris-data/images/meanshift'
        for file in os.listdir(mydir):
            if file.endswith('.png'):
                os.remove(os.path.join(mydir, file))
                return redirect(request.url)
    return render_template('meanshift.html')


if __name__ == '__main__':
    app.run(debug=True)
