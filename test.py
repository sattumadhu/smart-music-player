import streamlit as st
import cv2
from PIL import Image

# Define a function to capture an image from the webcam and save it as photo.png
def capture_image():
    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam.")
        return

    # Read a single frame
    ret, frame = cap.read()
    if ret:
        # Save the frame as 'photo.png'
        cv2.imwrite('images/photo.png', frame)
        st.success("Image captured successfully!")
    else:
        st.error("Failed to capture image.")

    # Release the webcam
    cap.release()

# Streamlit UI for Auto Mood Selector
st.title("Smart Music Player")

# Auto Mood Selector Button
if st.button("Auto Mood Selector"):
    capture_image()  # Capture the image when the button is clicked
    
    # Display the captured image
    st.image("images/photo.png", caption="Captured Image", use_column_width=True)
