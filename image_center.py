import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def center(image_array):
    img = image_array
    original_height, original_width = img.shape[:2]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    non_white_mask = gray < 240

    coordinates = np.column_stack(np.where(non_white_mask))
    if len(coordinates) == 0:
        return img
    y_min, x_min = np.min(coordinates, axis=0)
    y_max, x_max = np.max(coordinates, axis=0)

    object_roi = img[y_min:y_max, x_min:x_max]
    object_height, object_width = object_roi.shape[:2]

    white_bg = np.ones((original_height, original_width, 3), dtype=np.uint8) * 255

    center_x = (original_width - object_width) // 2
    center_y = (original_height - object_height) // 2

    end_x = min(center_x + object_width, original_width)
    end_y = min(center_y + object_height, original_height)

    obj_end_x = object_width if center_x >= 0 else object_width + center_x
    obj_end_y = object_height if center_y >= 0 else object_height + center_y

    start_x = max(0, center_x)
    start_y = max(0, center_y)
    obj_start_x = max(0, -center_x)
    obj_start_y = max(0, -center_y)

    white_bg[start_y:end_y, start_x:end_x] = object_roi[obj_start_y:obj_end_y, obj_start_x:obj_end_x]

    return white_bg

st.title("Image Centering")
st.write("Upload an image to center the main object on a white background.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption='Original Image', use_column_width=True)

    centered_image = center(image)

    st.image(cv2.cvtColor(centered_image, cv2.COLOR_BGR2RGB), caption='Centered Image', use_column_width=True)
