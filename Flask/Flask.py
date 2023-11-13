from flask import Flask, render_template, jsonify, request, send_file
from glob import glob
from io import BytesIO
from zipfile import ZipFile
import os, sys, config
import subprocess, shutil, config

# subprocess.run(["python", config.PATH_DETECT_SCRIPT, config.PATH_USABLE_MODELS+model, config.UPLOADED_FILES_PATH])

# subprocess.run([config.PYTHON, config.PATH_CROP_SCRIPT, config.PATH_USABLE_MODELS+model])
# subprocess.run([config.PYTHON, config.PATH_FEATURE_SCRIPT])
# subprocess.run([config.PYTHON, config.PATH_OUTLINE_SCRIPT, config.PATH_TO_RESULTS, threshold])

scriptDetect = open(config.PATH_DETECT_SCRIPT, mode="r", encoding="utf-8").read()
scriptCrop = open(config.PATH_CROP_SCRIPT, mode="r", encoding="utf-8").read()
scriptFeature = open(config.PATH_FEATURE_SCRIPT, mode="r", encoding="utf-8").read()
scriptOutline = open(config.PATH_OUTLINE_SCRIPT, mode="r", encoding="utf-8").read()
app = Flask("AppServices")

def cleanup_files():
    if os.path.exists(config.RESULT_FOLDER_PATH):
        shutil.rmtree(config.RESULT_FOLDER_PATH)

    # Clear contents of PATH_TO_SAVE_CROPPED_IMAGES except csv folder and .gitkeep file
    save_cropped_images_path = config.PATH_TO_SAVE_CROPPED_IMAGES
    for item in os.listdir(save_cropped_images_path):
        item_path = os.path.join(save_cropped_images_path, item)
        if os.path.isfile(item_path) and item != '.gitkeep':
            os.remove(item_path)
        elif os.path.isdir(item_path) and item != 'csv':
            shutil.rmtree(item_path)

    # Clear contents of PATH_TO_CSV_FILES
    csv_files_path = config.PATH_TO_CSV_FILES
    for csv_file in os.listdir(csv_files_path):
        csv_file_path = os.path.join(csv_files_path, csv_file)
        if os.path.isfile(csv_file_path):
            os.remove(csv_file_path)

    # Clear contents of PATH_TO_RESULTS
    results_path = config.PATH_TO_RESULTS
    for result_item in os.listdir(results_path):
        result_item_path = os.path.join(results_path, result_item)
        if os.path.isfile(result_item_path):
            os.remove(result_item_path)
        elif os.path.isdir(result_item_path):
            shutil.rmtree(result_item_path)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/detect", methods=['POST'])
def detect():
    print("flask detect")
    cleanup_files()
    model = request.form['model']
    uploaded_file = request.files['file']
    filename = uploaded_file.filename

    if filename != '':
        # Save the uploaded file to a temporary directory
        file_path = os.path.join(config.UPLOADED_FILES_PATH, filename)
        result_path = os.path.join(config.RESULT_FILE_PATH, filename)
        uploaded_file.save(file_path)

        # Call your Python script with the file path as an argument
        # subprocess.run(["python", config.PATH_DETECT_SCRIPT, config.PATH_USABLE_MODELS+model, file_path])
        exec(scriptDetect, {"model": config.PATH_USABLE_MODELS+model,"folder": file_path})

        # Send the result file as a downloadable response
        response = send_file(result_path, as_attachment=True)

        # Delete the uploaded and result files
        os.remove(file_path)

        return response

    return jsonify({"error": "No file uploaded"})

@app.route("/detectMulti", methods=['POST'])
def detectMulti():
    print("flask detect Multiple")
    cleanup_files()
    model = request.form['model']
    uploaded_files = request.files.getlist('files')
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.filename:
                file_path = os.path.join(config.UPLOADED_FILES_PATH, uploaded_file.filename)
                uploaded_file.save(file_path)
        
        # subprocess.run(["python", config.PATH_DETECT_SCRIPT, config.PATH_USABLE_MODELS+model, config.UPLOADED_FILES_PATH])
        exec(scriptDetect, {"model": config.PATH_USABLE_MODELS+model,"folder": config.UPLOADED_FILES_PATH})

        for uploaded_file in uploaded_files:
            if uploaded_file.filename:
                file_path = os.path.join(config.UPLOADED_FILES_PATH, uploaded_file.filename)
                os.remove(file_path)
        
        target = config.RESULT_FOLDER_PATH
        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for file in glob(os.path.join(target, '*.png')):
                zf.write(file, os.path.basename(file))
        stream.seek(0)

        return send_file(
            stream,
            as_attachment=True,
            download_name='archive.zip'
        )
    
    return jsonify({"error": "No file uploaded"}) 

@app.route("/detectFaceOutliners", methods=['POST'])
def detectFaceOutliners():
    print("flask detect multiple, cropp and outline")
    cleanup_files()
    model = request.form['model']
    threshold = request.form['threshold']
    # print(threshold)
    uploaded_files = request.files.getlist('files')
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.filename:
                file_path = os.path.join(config.UPLOADED_FILES_PATH, uploaded_file.filename)
                uploaded_file.save(file_path)
        
        # subprocess.run([config.PYTHON, config.PATH_CROP_SCRIPT, config.PATH_USABLE_MODELS+model])
        # subprocess.run([config.PYTHON, config.PATH_FEATURE_SCRIPT])
        # subprocess.run([config.PYTHON, config.PATH_OUTLINE_SCRIPT, config.PATH_TO_RESULTS, threshold])

        exec(scriptCrop, {"model": config.PATH_USABLE_MODELS+model})
        exec(scriptFeature)
        exec(scriptOutline, {"folder_name": config.PATH_TO_RESULTS, "score_threshold": threshold})

        #clear upload
        for uploaded_file in uploaded_files:
            if uploaded_file.filename:
                file_path = os.path.join(config.UPLOADED_FILES_PATH, uploaded_file.filename)
                os.remove(file_path)
        
        target = config.PATH_TO_RESULTS
        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for file in glob(os.path.join(target, '*.png')):
                zf.write(file, os.path.basename(file))
            for file in glob(os.path.join(target, '*.txt')):
                zf.write(file, os.path.basename(file))
        stream.seek(0)

        return send_file(
            stream,
            as_attachment=True,
            download_name='archive.zip'
        )
    
    return jsonify({"error": "No file uploaded"})

app.config.from_object(__name__)
app.run(debug = True, port = 8000)

# @app.route("/login")
# def login():
#     if 'user' in session:
#         return redirect("/")
    
#     return render_template('Login.html')

# @app.route("/login", methods=['POST'])
# def loginPost():
#     resposne_form = request.form
#     if not resposne_form['login'] and not resposne_form['password']:
#         return "Brak danych <br/><a href='/'><button>Powrót</button></a>"
    
#     con = sqlite3.connect(DATABASE)
#     cur = con.cursor()
#     cur.execute("select * from users where login='"+resposne_form['login']+"' and password='"+resposne_form['password']+"';")
#     user = cur.fetchall()
#     con.close()

#     if user:
#         session['user']=user

#     return redirect("/login")
        

# @app.route("/register")
# def register():
#     return render_template('Register.html')

# @app.route("/register", methods=['POST'])
# def registerPost():
#     login = request.form['login']
#     password = request.form['password']
#     con = sqlite3.connect(DATABASE)
#     cur = con.cursor()
#     cur.execute("INSERT INTO users (login,password,admin) VALUES (?,?,?)",(login,password,"no") )
#     con.commit()
#     con.close()
#     return redirect("/")

# @app.route("/users")
# def users():
#     return render_template('Users.html')

# @app.route("/logout")
# def logout():
#     if 'user' in session:
#         session.pop('user')
#     else:
#         # Przekierowanie klienta do strony początkowej
#         redirect(url_for('index'))
#     return render_template('Logout.html')

# @app.route("/addBook", methods=['POST'])
# def addBook():
#     login = request.form['autor']
#     password = request.form['title']
#     con = sqlite3.connect(DATABASE)
#     cur = con.cursor()
#     cur.execute("INSERT INTO books (autor,title) VALUES (?,?)",(login,password) )
#     con.commit()
#     con.close()
#     return redirect("/")

# @app.route("/createdb")
# def createdb():
#     global isDataBaseCreated
#     conn = sqlite3.connect(DATABASE)
#     cur = conn.cursor() 
#     try:
#         cur.execute("SELECT * FROM users")
#         items = cur.fetchall() 
#         for item in items:
#             print(item[0] + item[1])
#     except sqlite3.OperationalError:
#         conn.execute('CREATE TABLE users (login TEXT, password TEXT, admin TEXT)')
#         conn.execute('CREATE TABLE books (autor TEXT, title TEXT)')

#     conn.close()
#     isDataBaseCreated=True
#     return redirect("/")

