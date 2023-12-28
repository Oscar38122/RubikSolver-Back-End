import cv2
import numpy as np
import json
import mysql.connector
from flask import make_response


def classify_rubiks_color(bgr): # This method assumes the lighting does not affect the colors,
                                # for a more reliable method HSV instead of BGR should be used
    colors = {
        'w': np.array([240, 240, 240]),
        'r': np.array([30, 30, 220]),
        'o': np.array([0, 140, 255]),
        'b': np.array([200, 0, 0]),
        'g': np.array([0, 200, 0]),
        'y': np.array([0, 240, 240]),
    }

    bgr = np.array(bgr)

    closest_color = min(colors.keys(), key=lambda color: np.linalg.norm(colors[color] - bgr))

    return closest_color

def get_average_color(image, roi): #Crops each cube from a face and gets an average color

    x, y, width, height = roi
    crop_img = image[y:y+height, x:x+width]
    #cv2.imshow("Cropped Region", crop_img)

    average_color = np.mean(crop_img, axis=(0, 1))
    return average_color



def crop_and_read_image(image_path, output_size=(1828, 1828)): # The output size might vary on camera resolution,
                                                               # for this project it will be fixed instead of dynamic

    image = cv2.imread(image_path)

    height, width, _ = image.shape

    center_x, center_y = width // 2, height // 2

    x1 = max(center_x - output_size[0] // 2, 0)
    y1 = max(center_y - output_size[1] // 2, 0)
    x2 = min(center_x + output_size[0] // 2, width)
    y2 = min(center_y + output_size[1] // 2, height)

    cropped_image = image[y1:y2, x1:x2]

    if cropped_image.shape[0] != output_size[0] or cropped_image.shape[1] != output_size[1]:
        cropped_image = cv2.resize(cropped_image, output_size)

    return cropped_image

def face_mapper(index):
    image_path = 'RubikFaceTest.jpg'
    cropped_image = crop_and_read_image(image_path)

    # Areas of each cube on picture
    topL = (150, 150, 300, 300) # top left
    topM = (775, 150, 300, 300) # top middle
    topR = (1400, 150, 300, 300) # top right
    middleL = (150, 775, 300, 300) # middle left
    middle = (775, 775, 300, 300) # middle
    middleR = (1400, 775, 300, 300) # middle right
    bottomL = (150, 1400, 300, 300) # bottom left
    bottomM = (775, 1400, 300, 300) # bottom middle
    bottomR = (1400, 1400, 300, 300) # bottom right



    #cv2.imshow("Cropped Image", cropped_image)

    positions = [topL, topM, topR, middleL, middle, middleR, bottomL, bottomM, bottomR]
    face = ''

    for i in range(len(positions)):
        positions[i] = get_average_color(cropped_image, positions[i])
        print("Average Color (BGR):", positions[i])
        positions[i] = classify_rubiks_color(positions[i])
        print("is closest to", positions[i])
        face = face + positions[i]

    if (int(index) == 1 and positions[4] != 'y'):
        return make_response("Wrong Cube Orientation", 409)
    elif (int(index) == 3 and positions[4] != 'b'):
        return make_response("Wrong Cube Orientation", 409)
    db = mysql.connector.connect(
        host="localhost",
        port=3306,  
        user="root",
        password="root",
        database="rubiksolver"
    )
    cursor = db.cursor()

    data = [int(index), face]
    query = "INSERT INTO faces (id, face) VALUES (%s, %s)"

    try:
        cursor.execute(query, data)
        db.commit()
        cursor.close()
    except Exception as e:
        print(e)


    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return make_response("Success", 201)

