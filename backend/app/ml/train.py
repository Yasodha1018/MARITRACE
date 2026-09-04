import tensorflow as tf
from tensorflow.keras import layers, models
from data_loader import OilSpillDataLoader
import os

def build_unet(input_size=(256, 256, 2)):
    """Build a U-Net model for oil spill segmentation"""
    inputs = layers.Input(input_size)
    
    # Encoder
    c1 = layers.Conv2D(64, 3, activation='relu', padding='same')(inputs)
    c1 = layers.Conv2D(64, 3, activation='relu', padding='same')(c1)
    p1 = layers.MaxPooling2D(2)(c1)
    
    c2 = layers.Conv2D(128, 3, activation='relu', padding='same')(p1)
    c2 = layers.Conv2D(128, 3, activation='relu', padding='same')(c2)
    p2 = layers.MaxPooling2D(2)(c2)
    
    c3 = layers.Conv2D(256, 3, activation='relu', padding='same')(p2)
    c3 = layers.Conv2D(256, 3, activation='relu', padding='same')(c3)
    p3 = layers.MaxPooling2D(2)(c3)
    
    c4 = layers.Conv2D(512, 3, activation='relu', padding='same')(p3)
    c4 = layers.Conv2D(512, 3, activation='relu', padding='same')(c4)
    p4 = layers.MaxPooling2D(2)(c4)
    
    # Bottleneck
    c5 = layers.Conv2D(1024, 3, activation='relu', padding='same')(p4)
    c5 = layers.Conv2D(1024, 3, activation='relu', padding='same')(c5)
    
    # Decoder
    u6 = layers.Conv2DTranspose(512, 2, strides=2, padding='same')(c5)
    u6 = layers.concatenate([u6, c4])
    c6 = layers.Conv2D(512, 3, activation='relu', padding='same')(u6)
    c6 = layers.Conv2D(512, 3, activation='relu', padding='same')(c6)
    
    u7 = layers.Conv2DTranspose(256, 2, strides=2, padding='same')(c6)
    u7 = layers.concatenate([u7, c3])
    c7 = layers.Conv2D(256, 3, activation='relu', padding='same')(u7)
    c7 = layers.Conv2D(256, 3, activation='relu', padding='same')(c7)
    
    u8 = layers.Conv2DTranspose(128, 2, strides=2, padding='same')(c7)
    u8 = layers.concatenate([u8, c2])
    c8 = layers.Conv2D(128, 3, activation='relu', padding='same')(u8)
    c8 = layers.Conv2D(128, 3, activation='relu', padding='same')(c8)
    
    u9 = layers.Conv2DTranspose(64, 2, strides=2, padding='same')(c8)
    u9 = layers.concatenate([u9, c1])
    c9 = layers.Conv2D(64, 3, activation='relu', padding='same')(u9)
    c9 = layers.Conv2D(64, 3, activation='relu', padding='same')(c9)
    
    outputs = layers.Conv2D(1, 1, activation='sigmoid')(c9)
    
    model = models.Model(inputs, outputs)
    return model

def train_model():
    """Train the U-Net model on the Zenodo dataset"""
    # Paths to your extracted data
    IMAGE_DIR = "./data/satellite/train_images/"
    MASK_DIR = "./data/satellite/train_masks/"
    
    # Create data loaders
    train_loader = OilSpillDataLoader(IMAGE_DIR, MASK_DIR, batch_size=4, img_size=(256, 256))
    
    # Build model
    model = build_unet()
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    # Train
    history = model.fit(
        train_loader,
        epochs=50,
        steps_per_epoch=len(train_loader)
    )
    
    # Save the model
    os.makedirs("./models", exist_ok=True)
    model.save("./models/unet_oil_spill.h5")
    print("Model saved to ./models/unet_oil_spill.h5")
    
    return model

if __name__ == "__main__":
    train_model()