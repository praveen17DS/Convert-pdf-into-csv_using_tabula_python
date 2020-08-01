from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import os
import tabula
from tabula import read_pdf
from flask import send_from_directory,Response
import urllib.request
import requests
import wget
import cx_Oracle
import csv
import pandas as pd
import numpy as np
import datetime
import functools



app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/356285/Desktop/bank/analyser/analyser/uploads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#listOfFiles = os.listdir('C:/Users/310362/Downloads')


DOWNLOAD_FOLDER='C:/Users/356285/Desktop/bank/analyser/analyser/downloads'
download_path = os.path.join(os.path.expanduser('~'), 'downloads') 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
              
@app.route('/sm', methods=['GET', 'POST'])
def upload_file():
   
    if request.method == 'POST':     
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        secure_password = request.form['password'] 
      
        # if user does not select file, browser also
        # submit an empty part without filename 
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #directory = "C:\\Users\\Tory\\Desktop\\Delete_Test"
            for F in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, F)
                os.remove(file_path)
            for F in os.listdir(DOWNLOAD_FOLDER):
                file_path = os.path.join(DOWNLOAD_FOLDER, F)
                os.remove(file_path)
            filename = secure_filename(file.filename)            
            f1=file.filename      
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            tabula.convert_into(UPLOAD_FOLDER+'/'+f1,os.path.splitext(download_path+'/'+f1)[0]+".csv", output_format="csv",pages='all',password=secure_password,lattice=True)
            
        
        return redirect(url_for('upload_file',filename=filename))
    
    
    return render_template('sm.html')
 
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['download_path'], filename, as_attachment=True)
    

if __name__ == "__main__":
    app.secret_key = 'super secret key'
     

    app.debug = True
    app.run()
           
  
 


  



      


    