from flask import Flask, request
from werkzeug.utils import secure_filename
import os
from RubikMapper import face_mapper
from Reset import resetFaces
app = Flask(__name__)

# Set the absolute path for the upload folder
UPLOAD_FOLDER = 'D:/Python_VSCode/Arduino/RubikSolver/Rubik-Backend'
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
        return face_mapper(request.form['number'])
    else:
        return "No file found", 400
    
@app.route("/reset", methods=["DELETE"])
def reset():
    resetFaces()
    return "Success", 200

@app.route("/solve")
def solve():
    #solve()
    return "Success", 200

if __name__ == "__main__":
    app.run(host='192.168.50.200', debug=True, port=5001)
