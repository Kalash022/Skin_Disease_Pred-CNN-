import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import os

# Function to build and compile the model
def build_model():
    # Load MobileNetV2 pre-trained model without the top classification layer
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')

    # Freeze the base layers so they won't be retrained
    base_model.trainable = False

    # Add custom layers for your skin disease classification
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),  # Pooling layer to reduce the spatial dimensions
        layers.Dense(128, activation='relu'),  # Fully connected layer
        layers.Dense(1, activation='sigmoid')  # Output layer for binary classification
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Print the summary of the model
    model.summary()

    return model

if __name__ == "__main__":
    # Build the model
    model = build_model()

    # Create a directory to save the model if it doesn't exist
    if not os.path.exists('saved_model'):
        os.makedirs('saved_model')

    # Save the model to the saved_model directory
    model.save('saved_model/skin_disease_model.h5')

    print("Model saved successfully in 'saved_model/skin_disease_model.h5'")
