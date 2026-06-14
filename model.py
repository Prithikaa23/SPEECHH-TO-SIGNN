import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import TimeDistributed, Conv2D, MaxPooling2D, Flatten, LSTM, Dense

def build_cnn_rnn_model(num_classes=2000):
    # Input shape: (frames, height, width, channels)
    input_shape = (10, 64, 64, 3)  
    inputs = Input(shape=input_shape)

    # CNN applied frame by frame
    x = TimeDistributed(Conv2D(32, (3,3), activation="relu"))(inputs)
    x = TimeDistributed(MaxPooling2D((2,2)))(x)
    x = TimeDistributed(Flatten())(x)

    # RNN on sequence of features
    x = LSTM(128)(x)

    # Output classification
    outputs = Dense(num_classes, activation="softmax")(x)

    # Build Model
    model = Model(inputs, outputs)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model

# Initialize model
model = build_cnn_rnn_model()
