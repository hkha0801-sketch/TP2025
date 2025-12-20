from flask import Flask
import gradio as gr
import tensorflow.keras as keras
import numpy as np
from PIL import Image

# Load model
model = keras.models.load_model("model/keras_model.h5", compile=False)

# Load labels
class_names = open("model/labels.txt", "r", encoding="utf-8").readlines()

def predict_gender(image):
    image = Image.fromarray(image).convert("RGB")
    image = image.resize((224, 224))

    img_array = np.asarray(image)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence = prediction[0][index]

    return f"Giới tính: {class_name}", f"Độ tin cậy: {confidence*100:.2f}%"

app = Flask(__name__)

interface = gr.Interface(
    fn=predict_gender,
    inputs=gr.Image(),
    outputs=["text", "text"],
    title="Gender Detection AI",
    description="Tải ảnh khuôn mặt để xác định giới tính bằng AI"
)

if __name__ == "__main__":
    interface.launch()
