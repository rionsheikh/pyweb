from flask import Flask,render_template,request
from werkzeug.utils import secure_filename,redirect
import os 
import moviepy.editor

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'up'


@app.route('/')
def index():
        return """
        <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>flask web application file upload </title>
                </head>
                <body>

                    <h1> Upload a file </h1>
                    <form action = "http://localhost:8000/uploader" method = "POST" 
                    enctype = "multipart/form-data">
                    <input type = "file" name = "file" />
                    <input type = "submit"/>
                 </form>  
                </body>
                </html>
        """


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      if not os.path.exists(os.getcwd()+"/up"):
         os.mkdir(os.getcwd()+"/up")
      if not os.path.exists(os.getcwd()+"/static"):
         os.mkdir(os.getcwd()+"/static")
      f = request.files['file']
      filename=secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
  
      videfilesrc=os.path.join("up",filename)
      videof=moviepy.editor.VideoFileClip(videfilesrc)
      videof=videof.subclip(0,20)
      videof.resize(0.4)
      videof.write_videofile(os.path.join("static",filename))
      vlocation=os.path.join("static",filename)
      dfile="<a href='{}' download='{}'>Download Now </a> ".format(vlocation,filename)
      os.remove(videfilesrc)
      return dfile