import tensorflow as tf
print("TF Version:", tf.__version__)
print("Keras Version:", tf.keras.__version__)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(10)
])
print("Model created successfully!")