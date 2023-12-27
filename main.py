from flask import Flask, request
from werkzeug.utils import secure_filename
import os
from RubikSolver import face_mapper
app = Flask(__name__)

# Set the absolute path for the upload folder
UPLOAD_FOLDER = '/Rubik-Backend'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/face", methods=["POST"])
def face():
    print("here")
    if 'photo' in request.files:
        file = request.files['photo']
        # Secure the filename
        filename = secure_filename(file.filename)
        # Save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(request.form['number'])
        face_mapper(request.form['number'])
        return "Success", 201
    else:
        return "No file found", 400

if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=5001)
