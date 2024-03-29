# -*- coding: utf-8 -*-
"""C_vs_D_classifier.ipynb


Original file is located at
    https://colab.research.google.com/drive/1_2TpQ9fEw7oxfiEqN-pXJycNHDrJ5fwu

###Cat vs Dog Image Classifier using Convolutional Neural Networks (CNNs)
This project is a machine learning image classifier that uses convolutional neural networks (CNNs) to distinguish between images of cats and dogs. The model is trained on the 'cats_vs_dogs' tensorflow dataset of labeled cat and dog images, and uses CNNs to automatically learn features from the images that are useful for distinguishing between the two classes. The model is then able to make predictions on new images by analyzing the learned features and outputting a probability score for each class. This project has practical applications in areas such as animal recognition and pet monitoring, and can also serve as a learning exercise for those interested in computer vision and deep learning.
"""

import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

"""###Loading data"""

def resize_image(img, label):
  return tf.image.resize(img, [height, width]) / 255, label

height = 250
width = 250

split = ['train[:80%]', 'train[80%:]']

trainDataset, testDataset = tfds.load(name='cats_vs_dogs', split=split, as_supervised=True)

trainDataset = trainDataset.map(resize_image)
testDataset = testDataset.map(resize_image)

classes_names = ['Cat', 'Dog']

for image, label in trainDataset.take(3):
  plt.figure()
  plt.imshow(image)
  plt.xlabel(f'{classes_names[label]}')

"""###Creating a CNN model"""

trainDataset = trainDataset.batch(32)
testDataset = testDataset.batch(32)

model = keras.Sequential([
    keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(height, width, 3)),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(32, (3,3), activation='relu'),
    keras.layers.MaxPooling2D((2,2)),    
    keras.layers.Conv2D(64, (3,3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(trainDataset, epochs=10, validation_data=testDataset, verbose=1)

model.save('c_vs_d.h5')

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training', 'Validation'])
plt.grid()
plt.show()

(loss, accuracy) = model.evaluate(testDataset)
print(f'Loss: {loss}')
print(f'Accuracy: {accuracy}')

"""We get accuracy about 71%, which is rather poor. We'll make it higher, but first let's make several predictions."""

predictions = model.predict(testDataset.take(8))

i = 0
fig, ax = plt.subplots(1, 8, figsize=(25,10))
for image, label in testDataset.take(8):
  predictedLabel = int(predictions[i] >= 0.5)
  ax[i].axis('off')
  ax[i].set_title(f'Pred: {classes_names[predictedLabel]}, Real: {classes_names[label[0]]}')
  ax[i].imshow(image[0])
  i += 1

plt.subplots_adjust(wspace=0.5)
plt.show()

"""Now let's check its performance on other images, which I found on the internet. We also need to choose the proper resize method:"""

image_1 = tf.io.read_file('cat.jpg')
image_1 = tf.image.decode_jpeg(image_1)
image_1 = tf.image.resize(image_1, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
image_1 = tf.expand_dims(image_1, axis=0)

image_2 = tf.io.read_file('cat.jpg')
image_2 = tf.image.decode_jpeg(image_2)
image_2 = tf.image.resize(image_2, [height, width], method=tf.image.ResizeMethod.AREA)
image_2 = tf.expand_dims(image_2, axis=0)

image_3 = tf.io.read_file('cat.jpg')
image_3 = tf.image.decode_jpeg(image_3)
image_3 = tf.image.resize(image_3, [height, width], method=tf.image.ResizeMethod.BICUBIC)
image_3 = tf.expand_dims(image_3, axis=0)




fig, axes = plt.subplots(1,3, figsize=(10,5))
axes[0].imshow(tf.squeeze(image_1))
axes[0].set_xlabel(f'Real: Cat, Pred: {classes_names[int(model.predict(image_1)[0][0])]}')
axes[0].set_title('NEAREST_NEIGHBOR')
axes[1].imshow(tf.squeeze(image_2))
axes[1].set_xlabel(f'Real: Cat, Pred: {classes_names[int(model.predict(image_2)[0][0])]}')
axes[1].set_title('AREA')
axes[2].imshow(tf.squeeze(image_3))
axes[2].set_xlabel(f'Real: Cat, Pred: {classes_names[int(model.predict(image_3)[0][0])]}')
axes[2].set_title('BICUBIC')

"""Let's keep nearest_neighbours as the resize method and make predictions on a few other pictures:"""

image_1 = tf.io.read_file('cat.jpg')
image_1 = tf.image.decode_jpeg(image_1)
image_1 = tf.image.resize(image_1, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
image_1 = tf.expand_dims(image_1, axis=0)

image_2 = tf.io.read_file('dog.jpg')
image_2 = tf.image.decode_jpeg(image_2)
image_2 = tf.image.resize(image_2, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
image_2 = tf.expand_dims(image_2, axis=0)

image_3 = tf.io.read_file('dog_4.jpg') 
image_3 = tf.image.decode_jpeg(image_3)
image_3 = tf.image.resize(image_3, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
image_3 = tf.expand_dims(image_3, axis=0)




fig, axes = plt.subplots(1,3, figsize=(10,5))
axes[0].imshow(tf.squeeze(image_1))
axes[0].set_xlabel(f'Real: Cat, Pred: {classes_names[int(model.predict(image_1)[0][0])]}')
axes[1].imshow(tf.squeeze(image_2))
axes[1].set_xlabel(f'Real: Dog, Pred: {classes_names[int(model.predict(image_2)[0][0])]}')
axes[2].imshow(tf.squeeze(image_3))
axes[2].set_xlabel(f'Real: Dog, Pred: {classes_names[int(model.predict(image_3)[0][0])]}')

"""Let's also make a function for convinient prediction-making."""

def predict_for_the_picture(image):
  image = tf.io.read_file(image)
  image = tf.image.decode_jpeg(image)
  image = tf.image.resize(image, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
  image = tf.expand_dims(image, axis=0)
  plt.figure(figsize=(4,4))
  plt.imshow(tf.squeeze(image))
  plt.xlabel(f'{classes_names[int(model.predict(image)[0][0])]}')

predict_for_the_picture('cat_1.jpg')

"""###Creating a CNN model using a pretrained network
As we saw, the accuracy of our model is rather poor but we can significantly increase it by using a pretrained model. We are going to use MobileNetV2 for our case.
"""

IMG_SHAPE = (height, width, 3)
base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

base_model.summary()

"""We'll add to this pretrained model one pooling and one dense layers:"""

base_model.trainable = False

global_average_layer = keras.layers.GlobalAveragePooling2D()
prediction_layer = keras.layers.Dense(1)

model = keras.Sequential([
    base_model,
    global_average_layer,
    prediction_layer
])

base_learning_rate = 0.0001
model.compile(optimizer=keras.optimizers.RMSprop(learning_rate=base_learning_rate),
              loss=keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

initial_epochs = 3
validation_steps=20

loss0,accuracy0 = model.evaluate(testDataset, steps = validation_steps)

history = model.fit(trainDataset,
                    epochs = initial_epochs,
                    validation_data=testDataset)
acc = history.history['accuracy']
print(acc)

"""And here we obtain much higher accuracy: around 98%"""

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training', 'Validation'])
plt.grid()
plt.show()

(loss, accuracy) = model.evaluate(testDataset)
print(f'Loss: {loss}')
print(f'Accuracy: {accuracy}')

model.save('Cats_vs_Dogs.h5')

predict_for_the_picture('dog_5.jpg')
