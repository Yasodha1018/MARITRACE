import tensorflow as tf
import numpy as np
from PIL import Image
import io
import cv2
import os
from datetime import datetime
import requests
import json

class OilSpillDetector:
    def __init__(self, model_path=None):
        """
        Initialize the oil spill detector with a pre-trained model.
        If no model path provided, downloads a pre-trained model.
        """
        self.model_path = model_path or self._download_model()
        self.model = tf.keras.models.load_model(self.model_path)
        self.input_size = (256, 256)
        
    def _download_model(self):
        """Download pre-trained model if not available locally"""
        model_dir = "./models"
        os.makedirs(model_dir, exist_ok=True)
        model_file = os.path.join(model_dir, "unet_oil_spill.h5")
        
        if not os.path.exists(model_file):
            print("Downloading pre-trained model...")
            # Download from Hugging Face or alternative source
            url = "https://huggingface.co/MeghanaK25/sar-oil-slick-detection/resolve/main/model.h5"
            response = requests.get(url, stream=True)
            with open(model_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Model downloaded successfully!")
        return model_file
    
    def preprocess(self, image_bytes):
        """Preprocess SAR image for model input"""
        img = Image.open(io.BytesIO(image_bytes)).convert('L')  # Grayscale for SAR
        img = img.resize(self.input_size)
        arr = np.array(img) / 255.0
        # Normalize and add channel dimension
        arr = np.expand_dims(arr, axis=(0, -1))
        return arr
    
    def predict_mask(self, image_bytes):
        """Generate oil spill segmentation mask"""
        input_arr = self.preprocess(image_bytes)
        pred = self.model.predict(input_arr)[0, :, :, 0]
        mask = (pred > 0.5).astype(np.uint8) * 255
        return mask, pred
    
    def extract_polygon(self, mask, original_shape, min_area=100):
        """Convert mask to polygon coordinates"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        
        # Filter by minimum area
        contours = [c for c in contours if cv2.contourArea(c) > min_area]
        if not contours:
            return None
            
        cnt = max(contours, key=cv2.contourArea)
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        # Scale to original image dimensions
        scale_x = original_shape[1] / self.input_size[1]
        scale_y = original_shape[0] / self.input_size[0]
        poly = approx.squeeze().tolist()
        if poly and len(poly) > 0:
            poly = [[int(p[0]*scale_x), int(p[1]*scale_y)] for p in poly]
        return poly
    
    def estimate_area(self, mask, pixel_resolution_km=0.01):
        """Estimate spill area in km²"""
        pixel_count = np.sum(mask > 0)
        area_km2 = pixel_count * (pixel_resolution_km ** 2)
        return area_km2
    
    def classify_severity(self, area_km2, confidence):
        """Classify spill severity"""
        if area_km2 > 10:
            return "HIGH", "Major spill requiring immediate response"
        elif area_km2 > 2:
            return "MEDIUM", "Significant spill requiring coordinated response"
        else:
            return "LOW", "Minor spill requiring monitoring"