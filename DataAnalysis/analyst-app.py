
import streamlit as st
import pandas as pd
import pathlib as path
import os

st.title("Data scientist assistant")

st.write("""
          ##### Assist with data preparation / model building"""
         )
def upload_file(file):
    try:

        with st.spinner("Processing the file..."):
            # Read the content of the uploaded file
            file_content = file.read()

        # Now, you can use the file_content or save it to a specific location
        # For example, save it to a temporary directory
        temp_dir = "datasets"  # Replace with your desired temporary directory
        os.makedirs(temp_dir, exist_ok=True)

        # Save the uploaded file to the temporary directory
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as temp_file:
            temp_file.write(file_content)
        return file_path
    except:
        return None



# read in excel or csv file
def validate_file(source):
    if path.Path(source).is_file():
        if path.Path(source).suffix in [".csv",".xlsx"]:
            print("file is valid")
            return True
        else:
            print("unaccepted file format")
            print(path.Path(source).suffix)
            return False
    else:
        print("file is invalid")
        return False
    
# read input 
def read_input(source):
    is_valid = validate_file(source)
    if is_valid:
        if path.Path(source).suffix == ".csv":
            data = pd.read_csv(source)
            return (data,source)

        elif path.Path(source).suffix == ".xlsx":
            data = pd.read_excel(source)
            return (data,source)
    return (None,source)

#read input

file = st.file_uploader("pick a file")

if file and upload_file(file) is not None:
    input = read_input(upload_file(file))

    if input[0] is None:
        st.write("Provided file ' {} ' in ivalid".format(input[1]))
    else:
        st.write("Loaded dataset {}".format(file))
        data = input[0]

        st.write("Plotting columns {}".format(data.columns[1]))
        st.line_chart(data[data.columns[1]])
