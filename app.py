import streamlit as st
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load the saved model
model = tf.keras.models.load_model("resnet_vit_model.h5")

# Define class labels
class_labels = ['a_Good', 'b_Moderate', 'c_Unhealthy_for_Sensitive_Groups', 'd_Unhealthy', 'e_Very_Unhealthy', 'f_Severe']

# UI with Streamlit
st.title("Air Quality Classification")
st.write("Upload an image to classify air quality.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

def preprocess_image(image):
    """Preprocess image for both ResNet and ViT (same format)."""
    image = img_to_array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image  # Shape: (1, 224, 224, 3)

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Classify"):
        # Load and resize the image
        image = load_img(uploaded_file, target_size=(224, 224))

        # Preprocess image for both ResNet and ViT (same input format)
        image_resnet = preprocess_image(image)
        image_vit = preprocess_image(image)  # ViT also expects (batch, 224, 224, 3)

        # Make prediction with both inputs
        predictions = model.predict([image_resnet, image_vit])
        predicted_class = class_labels[np.argmax(predictions)]

        # Air quality descriptions
        aq_descriptions = {
            "a_Good": {"Range": "0-50", "Label": "Good", "Description": "Enjoy your usual outdoor activities"},
            "b_Moderate": {"Range": "51-100", "Label": "Moderate", "Description": "Extremely sensitive children and adults should refrain from strenuous outdoor activities."},
            "c_Unhealthy_for_Sensitive_Groups": {"Range": "101-150", "Label": "Unhealthy for Sensitive Groups", "Description": "Sensitive children and adults should limit prolonged outdoor activity."},
            "d_Unhealthy": {"Range": "151-200", "Label": "Unhealthy", "Description": "Sensitive groups should avoid outdoor exposure and others should limit prolonged outdoor activity."},
            "e_Very_Unhealthy": {"Range": "201-300", "Label": "Very Unhealthy", "Description": "Sensitive groups should stay indoors and others should avoid outdoor activity."},
            "f_Severe": {"Range": "301-500", "Label": "Hazardous", "Description": "Everyone should stay indoors and avoid physical activity."}
        }

        result = aq_descriptions[predicted_class]
        
        # Display results
        st.subheader(f"Prediction: {result['Label']} ({result['Range']})")
        st.write(result['Description'])
