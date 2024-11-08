
import os
import json
import numpy as np
from skimage.io import imread
from skimage.transform import resize
import matplotlib.pyplot as plt

class ImageGenerator:
    def __init__(self, file_path, label_path, batch_size, image_size, rotation=False, mirroring=False, shuffle=False):
        self.file_path = file_path
        self.label_path = label_path
        self.batch_size = batch_size
        self.image_size = image_size
        self.rotation = rotation
        self.mirroring = mirroring
        self.shuffle = shuffle
        self.epoch_count = 0
        self.index = 0

        # Load the labels
        try:
            with open(self.label_path, 'r') as f:
                self.labels = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: File not found at {self.label_path}")
            raise

        # List all .npy files
        try:
            self.file_names = [file for file in os.listdir(self.file_path) if file.endswith('.npy')]
            print(f"Loaded {len(self.file_names)} image files")
            if self.shuffle:
                np.random.shuffle(self.file_names)  # Initial shuffle if required
        except FileNotFoundError:
            print(f"ERROR: Directory not found at {self.file_path}")
            raise

    def next(self):
        if self.index >= len(self.file_names):
            self.epoch_count += 1
            self.index = 0
            if self.shuffle:
                np.random.shuffle(self.file_names)

        end_index = min(self.index + self.batch_size, len(self.file_names))
        batch_files = self.file_names[self.index:end_index]
        self.index = end_index

        images = []
        labels = []

        for fname in batch_files:
            img = np.load(os.path.join(self.file_path, fname))
            if self.mirroring and np.random.rand() > 0.5:
                img = np.fliplr(img)
            if self.rotation:
                img = np.rot90(img, k=np.random.choice([1, 2, 3]))
            img = resize(img, self.image_size, anti_aliasing=True)
            images.append(img)
            labels.append(self.labels[fname.split('.')[0]])

        if len(batch_files) < self.batch_size:
            # Adjust for partially filled batches if not the end of the data
            more_files = self.file_names[:self.batch_size - len(batch_files)]
            self.index = len(more_files)  # Adjust the index for the next call to next
            for fname in more_files:
                img = np.load(os.path.join(self.file_path, fname))
                if self.mirroring and np.random.rand() > 0.5:
                    img = np.fliplr(img)
                if self.rotation:
                    img = np.rot90(img, k=np.random.choice([1, 2, 3]))
                img = resize(img, self.image_size, anti_aliasing=True)
                images.append(img)
                labels.append(self.labels[fname.split('.')[0]])

        return np.array(images), np.array(labels)

    def current_epoch(self):
        return self.epoch_count

    def class_name(self, x):
        return self.labels[str(x)]

    def show(self):
        images, labels = self.next()
        if images.size > 0:
            plt.figure(figsize=(10, 10))
            for i in range(min(len(images), 16)):  # Show up to 16 images
                plt.subplot(4, 4, i + 1)
                plt.imshow(images[i])
                plt.title(self.class_name(labels[i]))
                plt.axis('off')
            plt.show()
        else:
            print("No images to display.")

if __name__ == "__main__":
    # Corrected paths according to your file structure
    gen = ImageGenerator('./data/exercise_data', './data/Labels.json', 32, (64, 64, 3), True, True, True)
    gen.show()
    