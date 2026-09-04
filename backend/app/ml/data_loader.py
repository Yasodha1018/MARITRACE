import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import Sequence
from PIL import Image
import random

class OilSpillDataLoader(Sequence):
    """Data loader for Sentinel-1 SAR oil spill dataset"""
    
    def __init__(self, image_dir, mask_dir, batch_size=8, img_size=(256, 256), shuffle=True):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.batch_size = batch_size
        self.img_size = img_size
        self.shuffle = shuffle
        
        # Get all image files
        self.image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.tif') or f.endswith('.tiff')])
        self.mask_files = sorted([f for f in os.listdir(mask_dir) if f.endswith('.tif') or f.endswith('.tiff')])
        
        # Ensure matching pairs
        assert len(self.image_files) == len(self.mask_files), "Mismatch between images and masks"
        
        self.indexes = np.arange(len(self.image_files))
        if self.shuffle:
            np.random.shuffle(self.indexes)
    
    def __len__(self):
        return int(np.ceil(len(self.image_files) / self.batch_size))
    
    def __getitem__(self, idx):
        batch_indexes = self.indexes[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_images = []
        batch_masks = []
        
        for i in batch_indexes:
            img_path = os.path.join(self.image_dir, self.image_files[i])
            mask_path = os.path.join(self.mask_dir, self.mask_files[i])
            
            # Load image (2048x2048x2 for VV + VH polarizations)
            img = self._load_image(img_path)
            # Load mask (2048x2048 binary)
            mask = self._load_mask(mask_path)
            
            # Resize to model input size
            img = tf.image.resize(img, self.img_size).numpy()
            mask = tf.image.resize(mask[..., np.newaxis], self.img_size).numpy()
            mask = (mask > 0.5).astype(np.float32)
            
            batch_images.append(img)
            batch_masks.append(mask)
        
        return np.array(batch_images), np.array(batch_masks)
    
    def _load_image(self, path):
        """Load SAR image (VV + VH polarizations)"""
        # Using PIL to load TIFF (works for multi-channel)
        img = Image.open(path)
        img = np.array(img)
        # If image has 2 channels (VV, VH), keep both
        if len(img.shape) == 3 and img.shape[2] == 2:
            return img.astype(np.float32) / 255.0
        # If single channel, duplicate to simulate 2 channels
        elif len(img.shape) == 2:
            return np.stack([img, img], axis=-1).astype(np.float32) / 255.0
        else:
            return img.astype(np.float32) / 255.0
    
    def _load_mask(self, path):
        """Load binary mask"""
        mask = Image.open(path)
        mask = np.array(mask)
        # Binary: foreground = 1, background = 0
        return (mask > 0).astype(np.float32)
    
    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indexes)