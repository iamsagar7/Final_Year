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

app.config['UPLOAD_FOLDER'] = "/home/nexxus/Python/Final_Year/static/files"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imageclustering', methods=['GET', 'POST'])
def upload_files():
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
                        '/home/nexxus/Python/Final_Year/static/files/kmeans',
                        filename))
                CONFIG_kMEAN='/home/nexxus/Python/Final_Year/static/files/kmeans/'+filename
                from kmeans import main
                main(CONFIG_kMEAN)

            elif filename=="meanshift-config.config":
                file.save(
                    os.path.join(
                        '/home/nexxus/Python/Final_Year/static/files/meanshift',
                        filename))
                config_meanshift ='/home/nexxus/Python/Final_Year/static/files/meanshift/'+filename
                from Meanshift import main
                main(config_meanshift)
            else:
                file.save(
                    os.path.join(
                        '/home/nexxus/Python/Final_Year/static/csv',
                        filename))

            return redirect(request.url)
    return render_template('imageclustering.html')

@app.route('/numericclustering', methods=['GET', 'POST'])
def upload_numeric_cluster():
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
                        '/home/nexxus/Python/Final_Year/static/files/kmeans',
                        filename))
                CONFIG_kMEAN='/home/nexxus/Python/Final_Year/static/files/kmeans/'+filename
                from kmeans import main
                main(CONFIG_kMEAN)

            elif filename=="meanshift-config.config":
                file.save(
                    os.path.join(
                        '/home/nexxus/Python/Final_Year/static/files/meanshift',
                        filename))
                config_meanshift ='/home/nexxus/Python/Final_Year/static/files/meanshift/'+filename
                from Meanshift import main
                main(config_meanshift)
            else:
                file.save(
                    os.path.join(
                        '/home/nexxus/Python/Final_Year/static/csv',
                        filename))

            return redirect(request.url)
    return render_template('numericclustering.html')   


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         if filename == "kmean-config.config":
    #             file.save(
    #                 os.path.join(
    #                     '/home/nexxus/Python/Final_Year/static/files/kmeans',
    #                     filename))
    #             CONFIG_kMEAN='/home/nexxus/Python/Final_Year/static/files/kmeans/'+filename
    #             from kmeans import main
    #             main(CONFIG_kMEAN)

    #         elif filename=="meanshift-config.config":
    #             file.save(
    #                 os.path.join(
    #                     '/home/nexxus/Python/Final_Year/static/files/meanshift',
    #                     filename))
    #             config_meanshift ='/home/nexxus/Python/Final_Year/static/files/meanshift/'+filename
    #             from Meanshift import main
    #             main(config_meanshift)
    #         else:
    #             file.save(
    #                 os.path.join(
    #                     '/home/nexxus/Python/Final_Year/static/csv',
    #                     filename))

    #         return redirect(request.url)
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



@app.route('/abc/<abc>')
def abc(abc):
    return send_from_directory("images/meanshift", abc)

#meanshift
@app.route('/meanshift')
def meanshift():
    image_na = os.listdir('images/meanshift')
    image_na=natsort.natsorted(image_na)
    print(image_na)
    return render_template("meanshift.html", image_na=image_na)


@app.route('/kmeans', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        mydir = '/home/nexxus/Python/Final_Year/images/kmeans'
        for file in os.listdir(mydir):
            if file.endswith('.png'):
                os.remove(os.path.join(mydir, file))
                return redirect(request.url)
    return render_template('kmeans.html')


@app.route('/meanshift', methods=['POST', 'GET'])
def delete_shift():
    if request.method == 'POST':
        mydir = '/home/nexxus/Python/Final_Year/images/meanshift'
        for file in os.listdir(mydir):
            if file.endswith('.png'):
                os.remove(os.path.join(mydir, file))
                return redirect(request.url)
    return render_template('meanshift.html')


@app.route('/kimage/<kimage>')
def image(kimage):
    return send_from_directory("images/kmeanimg", kimage)

#kmean iamge
@app.route('/kmeanImage')
def kmeanImage():
    image_nam = os.listdir('images/kmeanimg')
    image_nam=natsort.natsorted(image_nam)
    print(image_nam)
    return render_template("KmeanImage.html", image_nam=image_nam)

@app.route('/KmeanImage', methods=['POST', 'GET'])
def delete_shif():
    if request.method == 'POST':
        mydir = '/home/nexxus/Python/Final_Year/images/kmeanimg'
        for file in os.listdir(mydir):
            if file.endswith('.jpg'):
                os.remove(os.path.join(mydir, file))
                return redirect(request.url)
    return render_template('KmeanImage.html')

@app.route('/shiftimage/<shiftimage>')
def meanshiftimage(shiftimage):
    return send_from_directory("images/meanshiftimg", shiftimage)

#meanshift image
@app.route('/Meanshiftimg')
def MeanshiftImage():
    image_nama = os.listdir('images/meanshiftimg')
    image_nama=natsort.natsorted(image_nama)
    print(image_nama)
    return render_template("Meanshiftimg.html", image_nama=image_nama)

@app.route('/Meanshiftimg', methods=['POST', 'GET'])
def delete_shifs():
    if request.method == 'POST':
        mydir = '/home/nexxus/Python/Final_Year/images/meanshiftimage'
        for file in os.listdir(mydir):
            if file.endswith('.jpg'):
                os.remove(os.path.join(mydir, file))
                return redirect(request.url)
    return render_template('Meanshiftimg.html')
if __name__ == '__main__':
    app.run(debug=True)
