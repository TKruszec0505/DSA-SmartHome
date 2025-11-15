import os
import shutil
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from PIL import Image
import numpy as np

INBOX_FILE = r"C:\Users\Tomasz\Desktop\nowe_zrzuty"

MATH_FILE = r"C:\Users\Tomasz\Desktop\screeny\matematykascreeny"
ELECTRO_FILE = r"C:\Users\Tomasz\Desktop\screeny\elektronikascreeny"
GAME_FILE = r"C:\Users\Tomasz\Desktop\screeny\gryscreeny"
RANDOM_FILE = r"C:\Users\Tomasz\Desktop\screeny\pozostałescreeny"

CLASS_NAMES = ["matematyka", "elektronika", "gry", "inne"]
TARGET_DIRS = [MATH_FILE, ELECTRO_FILE, GAME_FILE, RANDOM_FILE]

# Model konwolucyjny akceptujący dowolny rozmiar obrazu (dx, dy)
def build_flexible_cnn(num_classes):
    model = models.Sequential([
        layers.Input(shape=(None, None, 3)),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(),

        layers.GlobalAveragePooling2D(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

# Funkcja wczytująca obraz jako tablicę NumPy
def load_image(path):
    img = Image.open(path).convert('RGB')
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)  # dodaj batch dimension

# Funkcja do klasyfikacji jednego screena i przeniesienia go do odpowiedniego folderu
def classify_and_move_image(model, img_path):
    img_array = load_image(img_path)
    preds = model.predict(img_array)
    class_idx = np.argmax(preds)
    target_dir = TARGET_DIRS[class_idx]
    print(f"Plik '{img_path}' rozpoznany jako: {CLASS_NAMES[class_idx]}")
    shutil.move(img_path, os.path.join(target_dir, os.path.basename(img_path)))

# Funkcja do wczytywania danych treningowych z folderu
# Zakłada strukturę: dataset/matematyka/, dataset/elektronika/, dataset/gry/, dataset/inne/
def load_training_data(dataset_path, image_size=(256, 256), batch_size=16):
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    train_data = datagen.flow_from_directory(
        dataset_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )
    val_data = datagen.flow_from_directory(
        dataset_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    return train_data, val_data

if __name__ == "__main__":
    num_classes = len(CLASS_NAMES)
    model = build_flexible_cnn(num_classes)

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    # Trening modelu na folderze screenów
    # dataset_path = r"C:\Users\Tomasz\Desktop\screeny\train_dataset"
    # train_data, val_data = load_training_data(dataset_path)
    # model.fit(train_data, validation_data=val_data, epochs=10)

    # Klasyfikacja i sortowanie screenów
    for file_name in os.listdir(INBOX_FILE):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            classify_and_move_image(model, os.path.join(INBOX_FILE, file_name))

