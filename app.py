# import streamlit as st
# import numpy as np
# import tensorflow as tf
# import json
# import uuid
# from PIL import Image

# # Load the model
# model = tf.keras.models.load_model("model/plant_disease_detect_model_pwp.keras")

# # Load the labels
# with open("plant_disease.json", 'r') as file:
#     plant_disease = json.load(file)

# # Function to process the image and prepare it for the model
# def extract_features(image):
#     image = image.resize((160, 160))
#     feature = tf.keras.utils.img_to_array(image)
#     feature = np.expand_dims(feature, axis=0)
#     return feature

# # Prediction function
# def model_predict(image):
#     img = extract_features(image)
#     prediction = model.predict(img)
#     prediction_label = plant_disease[np.argmax(prediction)]
#     return prediction_label

# # App interface
# st.title("🌿 Plant Disease Detection")

# uploaded_file = st.file_uploader("Upload a leaf image here", type=["jpg", "png", "jpeg"])

# if uploaded_file is not None:
#     # Show image
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)

#     # Predict when button is clicked
#     if st.button("🔍 Analyze Image"):
#         prediction = model_predict(image)
#         st.success(f"✅ Predicted Result: **{prediction}**")













# from flask import Flask, render_template,request,redirect,send_from_directory,url_for
# import numpy as np
# import json
# import uuid
# import tensorflow as tf

# app = Flask(__name__)
# model = tf.keras.models.load_model("model/plant_disease_detect_model_pwp.keras")
# label = ['Apple___Apple_scab',
#  'Apple___Black_rot',
#  'Apple___Cedar_apple_rust',
#  'Apple___healthy',
#  'Background_without_leaves',
#  'Blueberry___healthy',
#  'Cherry___Powdery_mildew',
#  'Cherry___healthy',
#  'Corn___Cercospora_leaf_spot Gray_leaf_spot',
#  'Corn___Common_rust',
#  'Corn___Northern_Leaf_Blight',
#  'Corn___healthy',
#  'Grape___Black_rot',
#  'Grape___Esca_(Black_Measles)',
#  'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
#  'Grape___healthy',
#  'Orange___Haunglongbing_(Citrus_greening)',
#  'Peach___Bacterial_spot',
#  'Peach___healthy',
#  'Pepper,_bell___Bacterial_spot',
#  'Pepper,_bell___healthy',
#  'Potato___Early_blight',
#  'Potato___Late_blight',
#  'Potato___healthy',
#  'Raspberry___healthy',
#  'Soybean___healthy',
#  'Squash___Powdery_mildew',
#  'Strawberry___Leaf_scorch',
#  'Strawberry___healthy',
#  'Tomato___Bacterial_spot',
#  'Tomato___Early_blight',
#  'Tomato___Late_blight',
#  'Tomato___Leaf_Mold',
#  'Tomato___Septoria_leaf_spot',
#  'Tomato___Spider_mites Two-spotted_spider_mite',
#  'Tomato___Target_Spot',
#  'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
#  'Tomato___Tomato_mosaic_virus',
#  'Tomato___healthy']

# with open("plant_disease.json",'r') as file:
#     plant_disease = json.load(file)

# # print(plant_disease[4])

# @app.route('/uploadimages/<path:filename>')
# def uploaded_images(filename):
#     return send_from_directory('./uploadimages', filename)

# @app.route('/',methods = ['GET'])
# def home():
#     return render_template('home.html')

# def extract_features(image):
#     image = tf.keras.utils.load_img(image,target_size=(160,160))
#     feature = tf.keras.utils.img_to_array(image)
#     feature = np.array([feature])
#     return feature

# def model_predict(image):
#     img = extract_features(image)
#     prediction = model.predict(img)
#     # print(prediction)
#     prediction_label = plant_disease[prediction.argmax()]
#     return prediction_label

# @app.route('/upload/',methods = ['POST','GET'])
# def uploadimage():
#     if request.method == "POST":
#         image = request.files['img']
#         temp_name = f"uploadimages/temp_{uuid.uuid4().hex}"
#         image.save(f'{temp_name}_{image.filename}')
#         print(f'{temp_name}_{image.filename}')
#         prediction = model_predict(f'./{temp_name}_{image.filename}')
#         return render_template('home.html',result=True,imagepath = f'/{temp_name}_{image.filename}', prediction = prediction )
    
#     else:
#         return redirect('/')
        
    
# if __name__ == "__main__":
#     app.run(debug=True)




















from flask import Flask, render_template, request, redirect, send_from_directory
import numpy as np
import json
import uuid
import tensorflow as tf
import os
import requests

app = Flask(__name__)


model_path = "plant_disease_model.keras"
dropbox_url = "https://www.dropbox.com/scl/fi/yrs0or7j0cz0vk0zu7mg8/plant_disease_detect_model_pwp.keras?rlkey=s5h8wlv3qv0boanxslg4iv4bu&st=vly81w8e&dl=1"

if not os.path.exists(model_path):
    print("Downloading model from Dropbox...")
    r = requests.get(dropbox_url)
    with open(model_path, "wb") as f:
        f.write(r.content)

model = tf.keras.models.load_model(model_path)

with open("plant_disease.json", 'r') as file:
    plant_disease = json.load(file)

@app.route('/uploadimages/<path:filename>')
def uploaded_images(filename):
    return send_from_directory('./uploadimages', filename)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

def extract_features(image):
    image = tf.keras.utils.load_img(image, target_size=(160, 160))
    feature = tf.keras.utils.img_to_array(image)
    feature = np.array([feature])
    return feature

def model_predict(image):
    img = extract_features(image)
    prediction = model.predict(img)
    prediction_label = plant_disease[prediction.argmax()]
    return prediction_label

@app.route('/upload/', methods=['POST', 'GET'])
def uploadimage():
    if request.method == "POST":
        image = request.files['img']
        filename = f"{uuid.uuid4().hex}_{image.filename}"
        filepath = os.path.join("uploadimages", filename)
        image.save(filepath)

        prediction = model_predict(filepath)

        return render_template(
            'home.html',
            result=True,
            imagepath=f'/uploadimages/{filename}',
            prediction=prediction
        )
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)




























# from flask import Flask, request, jsonify
# import numpy as np
# import json
# import uuid
# import tensorflow as tf
# import os

# app = Flask(__name__)
# model = tf.keras.models.load_model("model/plant_disease_detect_model_pwp.keras")

# with open("plant_disease.json", 'r') as file:
#     plant_disease = json.load(file)

# def extract_features(image):
#     image = tf.keras.utils.load_img(image, target_size=(160,160))
#     feature = tf.keras.utils.img_to_array(image)
#     feature = np.array([feature])
#     return feature

# def model_predict(image_path):
#     img = extract_features(image_path)
#     prediction = model.predict(img)
#     prediction_label = plant_disease[prediction.argmax()]
#     return prediction_label

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'img' not in request.files:
#         return jsonify({'error': 'No image uploaded'}), 400
    
#     image = request.files['img']
#     filename = f"uploadimages/temp_{uuid.uuid4().hex}_{image.filename}"
#     os.makedirs("uploadimages", exist_ok=True)
#     image.save(filename)

#     prediction = model_predict(filename)

#     os.remove(filename)  # نحذف الصورة بعد التنبؤ

#     return jsonify({'prediction': prediction})

# if __name__ == "__main__":
#     app.run(debug=True)
