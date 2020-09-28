from flask import Flask, render_template, request, send_file,send_from_directory
from werkzeug.utils import secure_filename
import pandas
from geopy.geocoders import ArcGIS
from make_map import mapmake
import zipfile
import os

arc = ArcGIS()

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",hc="100%")

@app.route("/success",methods=['POST'])
def success():
    if request.method == 'POST':
        global file
        file = request.files["File"]
        filenames = file.filename
        # file.save(secure_filename("uploaded"+file.filename))

        if file.filename.lower().endswith(".csv") == False:
            return render_template("index.html", text="Please give us a csv file")

        df = pandas.read_csv(file)

        if "address" and "Address" not in df.columns:
            return render_template("index.html", text="Please make sure that you have a address column in your CSV file!!")

        try:
            df["Latitude"]=df["Address"].apply(arc.geocode).apply(lambda x: x.latitude if x != None else None)
            df["Longitude"]=df["Address"].apply(arc.geocode).apply(lambda x: x.longitude if x != None else None)
            df.to_csv("uploads/uploaded-%s.csv"%filenames, index=False)
            mapmake(filenames)
            return render_template("index.html", text=df.to_html(), btn="download.html", hc="fit-content")
        except Exception as e:
            return render_template("index.html", text=e)
        
@app.route("/download/")
def download():
    zipfolder = zipfile.ZipFile('uploads/%s.zip'%filenames,'w', compression = zipfile.ZIP_STORED)

    zipfolder.write("uploads/map-%s.html"%filenames)    
    zipfolder.write("uploads/uploaded-%s.csv"%filenames)
    zipfolder.close()

    return send_file("uploads/%s.zip"%filenames,attachment_filename="your_files.zip", mimetype='zip',as_attachment=True)

if __name__ == '__main__':
    app.debug=False
    app.run(threaded = True)
