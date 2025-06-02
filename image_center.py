import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import zipfile

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

st.title("Batch Image Centering")
st.write("Upload multiple images to center the main object on a white background.")

uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            centered_image = center(image)

            # Display in Streamlit
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption=f'Original: {uploaded_file.name}')
            st.image(cv2.cvtColor(centered_image, cv2.COLOR_BGR2RGB), caption=f'Centered: {uploaded_file.name}')

            # Convert to PNG and write to ZIP
            img_pil = Image.fromarray(cv2.cvtColor(centered_image, cv2.COLOR_BGR2RGB))
            img_bytes = io.BytesIO()
            img_pil.save(img_bytes, format='PNG')
            zip_file.writestr(f'centered_{uploaded_file.name}', img_bytes.getvalue())

    st.download_button("Download All Centered Images as ZIP", data=zip_buffer.getvalue(), file_name="centered_images.zip", mime="application/zip")
