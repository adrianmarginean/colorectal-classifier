from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os
import logging

# Initialize the app
app = FastAPI()

# Mount the frontend
app.mount("/", StaticFiles(directory="app/frontend", html=True), name="frontend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
MODEL_PATH = "app/be/efficientnet_model.h5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model = load_model(MODEL_PATH, compile=False)

# Compile the model with a dummy optimizer and loss function to suppress the warning
model.compile(optimizer='adam', loss='categorical_crossentropy')



# Image preprocessing function
def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.resize((150, 150))  # Resize image
    image = img_to_array(image) / 255.0  # Normalize
    return np.expand_dims(image, axis=0)

image = Image.open("300px-Colorectal_adenocarcinoma_-_alt_--_intermed_mag.jpg") 
processed_image = preprocess_image(image)
predictions = model.predict(processed_image)  # Make predictions
print(f"Predictions: {predictions}")
class_index = int(np.argmax(predictions[0]))  # Get class index
confidence = float(predictions[0][class_index])  # Get confidence
print(f"Class index: {class_index}, Confidence: {confidence}")

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Prediction endpoint
@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    try:
        logging.info(f"Predictions:")
        image = Image.open(file.file)  # Open uploaded image
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)  # Make predictions
        logging.info(f"Predictions: {predictions}")
        class_index = int(np.argmax(predictions[0]))  # Get class index
        confidence = float(predictions[0][class_index])  # Get confidence
        logging.info(f"Class index: {class_index}, Confidence: {confidence}")
        return {"class_index": class_index, "confidence": confidence}
    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return {"error": str(e)}