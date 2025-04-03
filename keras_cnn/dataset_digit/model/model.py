import os
import preprocessing

# Configuració de les carpetes
train_dir = os.path.join(os.path.dirname(__file__), '..', 'train_images')
val_dir = os.path.join(os.path.dirname(__file__), '..', 'val_images')

image_size = (64, 64)
threshold = 80
erode_dilate = True
kernel_size = (3, 3)


X_train, y_train = preprocessing.load_data_from_directory(train_dir, threshold, erode_dilate, kernel_size, image_size)
X_val, y_val = preprocessing.load_data_from_directory(val_dir, threshold, erode_dilate, kernel_size, image_size)

# Comprovem la forma de les dades
print(f"Shape of X_train: {X_train.shape}")
print(f"Shape of y_train: {y_train.shape}")
print(f"Shape of X_val: {X_val.shape}")
print(f"Shape of y_val: {y_val.shape}")


import os
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator



# Paràmetres de les imatges
batch_size = 32

# Generador de dades
datagen = ImageDataGenerator(rescale=1.0/255.0)

# Generadors per a entrenament i validació
train_generator = datagen.flow(X_train, y_train, batch_size)
val_generator = datagen.flow(X_val, y_val, batch_size)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input

model = Sequential([
    Input(shape=(image_size[0], image_size[1], 1)),
    MaxPooling2D(pool_size=(2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(9, activation='softmax')  # 9 classes per als dígits 1-9
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(
    train_generator,
    epochs=20,
    validation_data=val_generator
)

model_path = os.path.join(os.path.dirname(__file__), 'digit_ocr_model.keras')
model.save(model_path)
