from flask import Flask, render_template, request, jsonify
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = tf.keras.models.load_model('wound_classifier.h5')

# Define the categories
categories = ['Abrasions', 'Bruises', 'Burns', 'Cut', 'Ingrown Nails', 'Laceration', 'Stab Wound']

#@app.route('/', methods=['GET'])
#def index():
 #   return render_template('wounds.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('wounds.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/remedy', methods=['GET'])
def remedy():
    return render_template('remedy.html')

@app.route('/bmi', methods=['GET'])
def bmi():
    return render_template('bmi.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'})

        file = request.files['file']

        # Check if no file is selected
        if file.filename == '':
            return jsonify({'message': 'No selected file'})

        if file:
            # Load and preprocess the user input image
            img = load_img(BytesIO(file.read()), target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = preprocess_input(img_array)
            img_array = np.expand_dims(img_array, axis=0)

            # Make predictions
            predictions = model.predict(img_array)

            # Get the predicted class index
            predicted_class_index = np.argmax(predictions)

            # Get the predicted class label
            predicted_class_label = categories[predicted_class_index]

            return jsonify({'message': f'Injury Type: {predicted_class_label}'})

    return render_template('wounds.html')

if __name__ == '__main__':
    app.run(debug=True)
