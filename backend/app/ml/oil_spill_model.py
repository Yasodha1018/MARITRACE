import tensorflow as tf
import numpy as np
from PIL import Image
import io
import cv2
import os

class OilSpillDetector:
    def __init__(self, model_path=None):
        self.model = None
        self.input_size = (256, 256)
        model_path = model_path or os.path.join(os.path.dirname(__file__), "trained_models", "oi1_spill_unet.keras")
        try:
            self.model = tf.keras.models.load_model(model_path)
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"⚠️ Model not loaded: {e}. Using dummy predictor.")
            self.model = None

    def _dummy_predict(self, image_bytes):
        # Return a fake mask (center blob)
        img = Image.open(io.BytesIO(image_bytes)).convert('L')
        img = img.resize(self.input_size)
        arr = np.array(img)
        mask = np.zeros((256, 256), dtype=np.uint8)
        # Create a fake circular spill
        for i in range(256):
            for j in range(256):
                if (i-128)**2 + (j-128)**2 < 30**2:
                    mask[i,j] = 255
        return mask, np.ones((256,256))*0.9

    def predict_mask(self, image_bytes):
        if self.model is None:
            return self._dummy_predict(image_bytes)
        # Real model logic (same as before)
        # ... (keep your existing code for real model)