from numpy.random import default_rng
import tensorflow as tf
import numpy as np

'''
Function that gathers test/train data amd trains the model


FILEPATH MUST BE CHANGED
'''

FILEPATH = "C:\\Users\\alyss\\Documents\\EDGAR\\"




def main():
    trainModel()


def trainModel():
    x_dim = 40
    y_dim = 1067
    z_dim = 3
    channel_dim = 1
    batch_size = 128
    img_shape = (x_dim, y_dim, z_dim)

    # ********** Generating testing and training data **********
    # Separating 1000 random images for testing
    train_data = []
    test_data = []
    train_labels = []
    test_labels = []
    labels = np.load(FILEPATH + "label_list_stretched_no_xxx.npy",
                     allow_pickle=False)

    # This method of generation allows with/without replacement
    rng = default_rng(11)

    test_index = rng.choice(7532, size=1000, replace=False)
    for i in range(0, 7532):
        spectrogram = np.load(FILEPATH + "metrics_stretched_no_xxx\\metrics_stretched_no_xxx\\{}.npy".format(i),

                              allow_pickle=False)
        if i in test_index:
            test_data.append(spectrogram)
            test_labels.append(labels[i])
        else:
            train_data.append(spectrogram)
            train_labels.append(labels[i])
    train_data = np.array(train_data)
    test_data = np.array(test_data)

    # turning labels into integers
    label_dict = {'ang': 0, 'dis': 1, 'exc': 2, 'fea': 3, 'fru': 4,
                  'hap': 5, 'neu': 6, 'oth': 7, 'sad': 8, 'sur': 9} #, 'xxx': 10
    new_train_labels = []
    new_test_labels = []
    for label in train_labels:
        new_train_labels.append(label_dict[label])
    for label in test_labels:
        new_test_labels.append(label_dict[label])
    new_train_labels = np.array(new_train_labels)
    new_test_labels = np.array(new_test_labels)

    # ********** Convolutional Layer **********
    traditionalCNN_model = tf.keras.layers.Conv2D(
        40, 3, input_shape=img_shape, data_format="channels_last"
    )

    # ********** Leaky Relu **********
    leakyRelu_1 = tf.keras.layers.LeakyReLU()

    # Argument is dimensionality of output, one for each class
    dense_layer = tf.keras.layers.Dense(10) #11

    full_model = tf.keras.Sequential([
        traditionalCNN_model,
        leakyRelu_1,
        tf.keras.layers.Flatten(),  # This is required for the training to work
        dense_layer
    ])

    print(full_model.summary())
    full_model.compile(optimizer='adam',
                       loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                       metrics=['accuracy'])

    full_model.fit(train_data, new_train_labels, epochs=5)

    test_loss, test_acc = full_model.evaluate(
        test_data,  new_test_labels, verbose=2)

    print('\nTest loss:', test_loss)
    print('\nTest accuracy:', test_acc)
    full_model.save('model\\my_model')






if __name__ == "__main__":
    main()
