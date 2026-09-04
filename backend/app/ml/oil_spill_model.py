import tensorflow as tf
import numpy as np
from PIL import Image
import io
import cv2

class OilSpillDetector:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.input_size = (256, 256)

    def preprocess(self, image_bytes):
        img = Image.open(io.BytesIO(image_bytes)).convert('L')
        img = img.resize(self.input_size)
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=(0, -1))
        return arr

    def predict_mask(self, image_bytes):
        input_arr = self.preprocess(image_bytes)
        pred = self.model.predict(input_arr)[0, :, :, 0]
        mask = (pred > 0.5).astype(np.uint8) * 255
        return mask

    def extract_polygon(self, mask, original_shape):
        # Find contours and scale back to original image dimensions
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        cnt = max(contours, key=cv2.contourArea)
        # approximate polygon
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        # scale to original size (assuming square)
        scale_x = original_shape[1] / self.input_size[1]
        scale_y = original_shape[0] / self.input_size[0]
        poly = approx.squeeze().tolist()
        poly = [[int(p[0]*scale_x), int(p[1]*scale_y)] for p in poly]
        return poly