from time import sleep

import tensorflow as tf
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from numpy import around


class romanNumberDedection:
    totalOne = 0
    totalTwo = 0
    totalThree = 0
    totalFour = 0
    totalFive = 0
    totalPrediction = 0

    resultList = []
    lastNumber = None
    romanNumber = None

    def __init__(self, image_height, image_width, i2cHandler):
        self._i2c = i2cHandler
        self._romanNumberModel = self.loadRomanNumberModel(image_height, image_width)

    def loadRomanNumberModel(self, image_height, image_width):
        model = Sequential()
        model.add(Conv2D(16, (7, 7), activation='relu', padding='same', name='block1_conv1',
                         input_shape=(image_height, image_width, 3)))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block1_pool'))

        model.add(Conv2D(16, (5, 5), activation='relu', padding='same', name='block4_conv1'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block4_pool'))

        model.add(Conv2D(32, (5, 5), activation='relu', padding='same', name='block2_conv1'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block2_pool'))

        model.add(Conv2D(32, (3, 3), activation='relu', padding='same', name='block3_conv1'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block3_pool'))

        model.add(Conv2D(64, (3, 3), activation='relu', padding='same', name='block5_conv1'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='block5_pool'))

        model.add(Flatten())
        model.add(Dense(128, activation='relu', name="fc-1-1"))
        model.add(Dropout(0.5))
        model.add(Dense(128, activation='relu', name="fc-2-1"))
        model.add(Dense(6, activation='softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])

        model.load_weights('/home/pi/haley/haleyKeras/ciffer.h5')

        # Save graph to prevent problems with multithreading
        # https://github.com/fchollet/keras/issues/2397
        self.graph = tf.get_default_graph()

        return model

    def dedectNumber(self, img):
        # Image preprocessing
        # Process array for CNN prediction
        tmpImg = img.array
        # tmpImg = dot(tmpImg[..., :3], [.3, .6, .1])

        # Set batchsize to 1 for single prediction
        tmpImg = tmpImg.reshape((1,) + tmpImg.shape)

        # Set color channel to 1 for grayscale image
        # tmpImg = tmpImg.reshape(tmpImg.shape + (1,))
        imgProcessed = tmpImg * (1. / 255)

        # Load graph to prevent problems with multithreading
        # https://github.com/fchollet/keras/issues/2397
        with self.graph.as_default():
            prediction = around(self._romanNumberModel.predict(imgProcessed), 2)[0]

        self.checkPrediction(prediction)
        sleep(0.01)

    def checkPrediction(self, prediction):
        result = 0
        self.totalPrediction += 1

        threshold = 0.96
        #print(prediction)

        if prediction[0] >= threshold:
            self.totalOne += 1
            result = 1

        if prediction[1] >= threshold:
            self.totalTwo += 1
            result = 2

        if prediction[2] >= threshold:
            self.totalThree += 1
            result = 3

        if prediction[3] >= threshold:
            self.totalFour += 1
            result = 4

        if prediction[4] >= threshold:
            self.totalFive += 1
            result = 5

        self.resultList.append(result)

        #if result is not None:
        #    print(result)

        #print(str(self.totalOne) + "x1  " +
        #      str(self.totalTwo) + "x2  " +
        #      str(self.totalThree) + "x3  " +
        #      str(self.totalFour) + "x4  " +
        #      str(self.totalFive) + "x5  Total: " +
        #      str(self.totalPrediction)
        #      )
