import tensorflow as tf
import numpy as np
from PIL import Image
import io
import cv2
import os

class OilSpillDetector:
    def __init__(self, model_path="./models/unet_oil_spill.h5"):
        """Load the trained U-Net model"""
        if os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
            print(f"Model loaded from {model_path}")
        else:
            print(f"Model not found at {model_path}. Please train the model first.")
            self.model = None
        self.input_size = (256, 256)
    
    def preprocess(self, image_bytes):
        """Preprocess SAR image for model input"""
        img = Image.open(io.BytesIO(image_bytes))
        # Convert to array
        img_array = np.array(img)
        # Handle different channel configurations
        if len(img_array.shape) == 2:
            # Single channel - duplicate for VV + VH
            img_array = np.stack([img_array, img_array], axis=-1)
        elif img_array.shape[2] > 2:
            # Take first 2 channels
            img_array = img_array[:, :, :2]
        # Resize
        img_array = tf.image.resize(img_array, self.input_size).numpy()
        img_array = img_array / 255.0
        return np.expand_dims(img_array, axis=0)
    
    def predict_mask(self, image_bytes):
        """Generate oil spill segmentation mask"""
        if self.model is None:
            # Fallback to dummy detection
            return self._dummy_detection(image_bytes)
        
        input_arr = self.preprocess(image_bytes)
        pred = self.model.predict(input_arr)[0, :, :, 0]
        mask = (pred > 0.5).astype(np.uint8) * 255
        return mask, pred
    
    def _dummy_detection(self, image_bytes):
        """Fallback dummy detection when model is not available"""
        img = Image.open(io.BytesIO(image_bytes))
        img = img.resize(self.input_size)
        arr = np.array(img)
        if len(arr.shape) == 3:
            arr = np.mean(arr, axis=2)
        # Create a random mask (for demo only)
        mask = (arr > np.percentile(arr, 80)).astype(np.uint8) * 255
        pred = mask / 255.0
        return mask, pred
    
    def extract_polygon(self, mask, original_shape, min_area=100):
        """Convert mask to polygon coordinates"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        
        contours = [c for c in contours if cv2.contourArea(c) > min_area]
        if not contours:
            return None
        
        cnt = max(contours, key=cv2.contourArea)
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        scale_x = original_shape[1] / self.input_size[1]
        scale_y = original_shape[0] / self.input_size[0]
        poly = approx.squeeze().tolist()
        if poly and len(poly) > 0:
            poly = [[int(p[0]*scale_x), int(p[1]*scale_y)] for p in poly]
        return poly
    
    def estimate_area(self, mask, pixel_resolution_km=0.01):
        """Estimate spill area in km²"""
        pixel_count = np.sum(mask > 0)
        return pixel_count * (pixel_resolution_km ** 2)
    
    def classify_severity(self, area_km2, confidence):
        """Classify spill severity"""
        if area_km2 > 10:
            return "HIGH", "Major spill requiring immediate response"
        elif area_km2 > 2:
            return "MEDIUM", "Significant spill requiring coordinated response"
        else:
            return "LOW", "Minor spill requiring monitoring"