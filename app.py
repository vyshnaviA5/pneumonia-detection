from flask import Flask, render_template, redirect, url_for, request
import os
from werkzeug.utils import secure_filename
import warnings
from PIL import Image, ImageEnhance
warnings.filterwarnings('ignore')
import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
import numpy as np
from keras.preprocessing import image

from flask import Flask, render_template, request,redirect,url_for,flash
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='pd'
)

# if(mysql):
#     print("connection succeed")
# else:
#     print("not connected")


# Define the directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define allowed extensions for file upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():
    return render_template("1.html")

@app.route("/index1")
def index1():
    return render_template("1.html")

@app.route("/testing")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")



@app.route("/reg", methods=['POST'])
def insert():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

     # Check if the user is already registered
    query_check = "SELECT * FROM users WHERE email=%s"
    values_check = (email,)

    cur_check =connection.cursor()
    cur_check.execute(query_check, values_check)
    existing_user = cur_check.fetchone()
    if existing_user:
        return render_template("already_register.html")

    query = "INSERT INTO users(name, email, password) VALUES (%s, %s, %s)"
    values = ( name, email, password)

    cur = connection.cursor()
    cur.execute(query, values)
    connection.commit()
    
    return render_template("reg11.html")


@app.route('/submisson', methods=['POST'])
def sub():
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['password']

        query1 = "SELECT * FROM users WHERE email='%s' AND password='%s'" % (email, passwd)
        cur = connection.cursor()
        cur.execute(query1)
        fetchdata = cur.fetchone()

        if fetchdata:
            return render_template('main.html')
        else:
            conn = "fail"
            return render_template('log.html', conn=conn)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            model = load_model('chest_xray.h5') 
            img_file = image.load_img(path, target_size=(224,224))
            x = image.img_to_array(img_file)
            x = np.expand_dims(x, axis=0)
            img_data = preprocess_input(x)
            classes = model.predict(img_data)
            if classes[0][0] > 0.5:
                ans = "Result is Normal"
                return render_template('index.html', ans=ans)
            else:
                ans = "Affected By PNEUMONIA"
                return render_template('index.html', ans=ans)
            

if __name__ == "__main__":
    app.run(debug=True)
