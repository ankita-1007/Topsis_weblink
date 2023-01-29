from flask import Flask,request,render_template
from func import main
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
import csv
import os
from email.message import EmailMessage
import ssl
import smtplib

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='static/files'

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def getValue():
  # data=request.form
  
  
  weights=request.form['weights']
  impacts=request.form['impacts']
  email=request.form['mail']
  weights=weights.split(',')
  impacts=impacts.split(',')
  f=request.files['filename']
  f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

  file = "static/files/"+f.filename
  # print(file)
  # print(weights)
  # print(impacts)
  # print(email)
  # print(data)
  try:
     result=main(file,weights,impacts)
  except:
     return render_template('error.html')
     
  result.to_csv("static/files/result.csv",index=False)
  email_sender = 'your e-mail'
  
  email_password = 'your password'
  
  
  em = EmailMessage()
  em['From'] = email_sender
  em['Subject'] = 'Your Topsis Result'
  em.set_content("Here is your Topsis result")
  with open("static/files/result.csv","rb") as fp:
    file_data=fp.read()


  em.add_attachment(file_data,maintype='text',subtype='csv',filename="result.csv")

  context = ssl.create_default_context()
  email_receiver =email
  em['To'] =email_receiver
  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver,em.as_string())




  return render_template('pass.html')
# @app.route('/dataset',methods=['GET','POST'])
# def dataset():
#   file=request.form['file']
#   data=[]
#   with open(file) as f:
#     csvfile=csv.reader(f)
#     for row in csvfile:
#       data.append(row)

#   print(data)

#   return render_template('dataset.html',dataset=data)
 
  

   

  

if __name__ == '__main__':
  app.run(debug=True)

