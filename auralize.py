import tensorflow as tf

if __name__ == "__main__":
    model = tf.keras.models.load_model("auralize_model.keras", None, True)
    model.predict
