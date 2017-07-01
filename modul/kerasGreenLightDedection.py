import tensorflow as tf
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from numpy import around


class kerasGreenLightDedection:
    def __init__(self, image_height, image_width):
        self._cossLightModel = self.loadCrosslightModel(image_height, image_width)

    def loadCrosslightModel(self, image_height, image_width):
        model = Sequential()
        model.add(Conv2D(8, (3, 3), activation='relu', padding='same', name='block1_conv1',
                         input_shape=(image_height, image_width, 3)))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block1_pool'))

        model.add(Conv2D(8, (3, 3), activation='relu', padding='same', name='block2_conv1'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block2_pool'))

        model.add(Conv2D(8, (3, 3), activation='relu', padding='same', name='block3_conv1'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block3_pool'))

        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(1))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        model.load_weights('/home/pi/haley/haleyKeras/crosslight.h5')

        # Save graph to prevent problems with multithreading
        # https://github.com/fchollet/keras/issues/2397
        self.graph = tf.get_default_graph()

        return model

    def greenLightDedected(self, img):
        # Image preprocessing
        imgProcessed = img.array
        imgProcessed = imgProcessed.reshape((1,) + imgProcessed.shape)
        imgProcessed = imgProcessed * (1. / 255)

        # Load graph to prevent problems with multithreading
        # https://github.com/fchollet/keras/issues/2397
        with self.graph.as_default():
            prediction = around(self._cossLightModel.predict(imgProcessed), 3)[0][0]

        print("Crosslight Prediction: " + str(prediction))
        if prediction < 0.1:
            print("Green light found")
            return True
        else:
            print("No green light found")
            return False
