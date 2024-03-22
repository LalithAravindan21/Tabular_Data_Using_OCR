import numpy as np
import pandas as pd
import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import pytesseract

st.title("Tabular Data Extractor")
st.subheader("Application to Convert Tables in Images to Downloadable DataFrames")

ocr_img = st.checkbox("View what type of image to upload")
if ocr_img:
    img_1 = Image.open('Access-studentmarks.png')
    st.image(img_1, width=500, caption='Example of a clear table image')

############################# Sidebar ########################
st.sidebar.title("Guide")
st.sidebar.markdown("> Quality screenshot images of tables taken from phone, laptop, etc are preferred")
st.sidebar.markdown("> Images captured with a phone camera yield incomplete tables")
st.sidebar.markdown("""> Images affected by artifacts including partial occlusion, distorted perspective, 
                    and complex background yield incomplete tables""")
st.sidebar.markdown(""" > Handwriting recognition on images containing tables will be significantly harder
                       due to infinite variations of handwriting styles and limitations of optical character recognition""")

###################### loading images #######################
uploaded_file = st.file_uploader("Choose an image | Accepted formats: only jpg & jpeg & png files", type=("jpg", "png", "jpeg"))

########## Table Extraction #############################
# Read file
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    # Viewing image
    ocr_img2 = st.checkbox("View uploaded image")
    if ocr_img2:
        st.image(img, width=500)

    # Convert image to grayscale
    img_gray = img.convert('L')

    # Perform OCR using pytesseract
    ocr_text = pytesseract.image_to_string(img_gray)

    # Display extracted text
    st.subheader("Extracted Text")
    st.write(ocr_text)

    # Convert extracted text to DataFrame
    rows = ocr_text.strip().split('\n')
    data = [row.split() for row in rows]
    dataframe = pd.DataFrame(data)

    # Display DataFrame
    st.subheader("DataFrame")
    st.dataframe(dataframe)

    # Download options
    col1, col2 = st.beta_columns(2)

    download_csv = col1.button("Download CSV")
    if download_csv:
        csv_data = dataframe.to_csv(index=False)
        b64 = base64.b64encode(csv_data.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="dataframe.csv">Download CSV</a>'
        col1.markdown(href, unsafe_allow_html=True)

    download_excel = col2.button("Download Excel")
    if download_excel:
        excel_data = dataframe.to_excel(index=False)
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="dataframe.xlsx">Download Excel</a>'
        col2.markdown(href, unsafe_allow_html=True)
