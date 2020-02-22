'''
Initial try at Model Training structure. Uses CNN model found in 
"Speech Emotion Recognition From 3D Log-MelSpectrograms With Deep Learning Network"

Needs input, and "test/train" function syntax, but the model should have the correct functions
Model functions may have to have parameters changed based on desired outputs or data dimensionality
'''

import tensorflow as tf

# ********** Log Mel-spectrograms as input **********
# when turned into a function, this should probably have
# Input: log mel spctrograms
# Output: Accuracy, confusion matrix, etc.
# @TODO turn this whole thing into a function of some kind


# ********** Normalization **********
# Pre-defined global image size/shape.
# Scaling could be required based on length (might not happen here)
IMG_SIZE = 900
IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 9)


# ********** Traditional CNN **********
# Create the base model from the pre-trained model MobileNet V2
traditionalCNN_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                         include_top=False,
                                                         weights='imagenet')
print(traditionalCNN_model.summary())


# ********** Leaky Relu **********
leakyRelu_1 = tf.keras.layers.LeakyReLU()

# ********** Max Pooling **********
maxPool3D_layer = tf.keras.layers.MaxPool3D()

# ********** Skip Connection **********
# Skips the block of 3 UFLB
dilatedCNN_skip = tf.keras.layers.Conv3D(
    filters=3, kernel_size=3, strides=2, dilation_rate=2)
batchNormalization_skip = tf.keras.layers.BatchNormalization()
skip_connection = tf.keras.Sequential([
    dilatedCNN_skip,
    batchNormalization_skip,
])


# ********** 3-UFLB **********
dilatedCNN_UFLB_1 = tf.keras.layers.Conv3D(
    filters=3, kernel_size=3, strides=2, dilation_rate=2)
batchNormalization_UFLB_1 = tf.keras.layers.BatchNormalization()
leakyRelu_UFLB_1 = tf.keras.layers.LeakyReLU()
ulfb_model_1 = tf.keras.Sequential([
    dilatedCNN_UFLB_1,
    batchNormalization_UFLB_1,
    leakyRelu_UFLB_1
])


dilatedCNN_UFLB_2 = tf.keras.layers.Conv3D(
    filters=3, kernel_size=3, strides=2, dilation_rate=2)
batchNormalization_UFLB_2 = tf.keras.layers.BatchNormalization()
leakyRelu_UFLB_2 = tf.keras.layers.LeakyReLU()
ulfb_model_2 = tf.keras.Sequential([
    dilatedCNN_UFLB_2,
    batchNormalization_UFLB_2,
    leakyRelu_UFLB_2
])


dilatedCNN_UFLB_3 = tf.keras.layers.Conv3D(
    filters=3, kernel_size=3, strides=2, dilation_rate=2)
batchNormalization_UFLB_3 = tf.keras.layers.BatchNormalization()
leakyRelu_UFLB_3 = tf.keras.layers.LeakyReLU()
ulfb_model_3 = tf.keras.Sequential([
    dilatedCNN_UFLB_3,
    batchNormalization_UFLB_3,
    leakyRelu_UFLB_3
])

# ********** Linear Layer **********
# @TODO I don't know what the Linear Layer exactly is, the paper seems to gleam over it

# ********** Leaky Relu **********
leakyRelu_2 = tf.keras.layers.LeakyReLU()

# ********** BLSTM - Bidirectional Long Short Term Memory **********
# Argument is dimensionality of output
lstm_layer = tf.keras.layers.Bidirectional(
    tf.keras.layers.LSTM(128))

# ********** Attention Weights **********
attention_layer = tf.keras.layers.Attention()

# ********** Full Connected **********
# Argument is dimensionality of output
fullyConntected_layer = tf.keras.layers.Dense(
    32)

# ********** Leaky Relu **********
leakyRelu_3 = tf.keras.layers.LeakyReLU()

# ********** Dropout Layer **********
# Argument is fraction of input to drop
dropout_layer = tf.keras.layers.Dropout(0.1)

# ********** Softmax Loss **********
softmax_layer = tf.keras.layers.Softmax()

# ********** Center Loss **********
# @TODO Center loss is not implementable in tensorflow unless we use someones random open-source github code


# ********** Combining the full model into it's final parent **********
full_model = tf.keras.Sequential([
    traditionalCNN_model,
    leakyRelu_1,
    maxPool3D_layer,
    # @TODO May need something customizable, I haven't looked into how we can get the model to either send it to skip or UFLB)
    leakyRelu_2,
    lstm_layer,
    attention_layer,
    fullyConntected_layer,
    leakyRelu_3,
    dropout_layer,
    # @TODO Same as above, need to send to both layers? non-sequentially
])

# @TODO Actual training implementation (not hard I hope, just model.predict or something like that)
# @TODO Needs a way to save the model, so training can be done once
