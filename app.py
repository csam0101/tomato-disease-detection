from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os

app = Flask(__name__)

# Load the trained model
model = load_model('tomato_disease_model.h5')

# Define a function to preprocess the image
def preprocess_image(image, target_size):
    image = cv2.resize(image, target_size)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0  # Normalize the image
    return image

# Define the route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['image']
        if file:
            # Read and preprocess the image
            image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
            processed_image = preprocess_image(image, target_size=(256, 256))

            # Make a prediction
            prediction = model.predict(processed_image)
            predicted_class = np.argmax(prediction, axis=1)[0]
            confidence = np.max(prediction)

            # Define your class labels (replace with actual class names)
            disease_map = {
                0: 'Bacterial Spot',
                1: 'Early Blight',
                2: 'Late Blight',
                3: 'Leaf Mold', 
                4: 'Septroia Leaf Spot',
                5: 'Spider Mites',
                6: 'Target Spot',
                7: 'Yellow Leaf Curl Virus', 
                8: 'Mosiac Virus',
                9: 'Healthy',
                10: 'Powdery Mildew'
            }

            predicted_disease = disease_map[predicted_class]
            
            # Return the result as a JSON object
            return jsonify({
                'disease': predicted_disease,
                'confidence': f'{confidence * 100:.2f}%'
            })
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))