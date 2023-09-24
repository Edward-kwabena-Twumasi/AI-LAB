
import streamlit as st
import pandas as pd
import pathlib as path
import os
import time

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

        wait_time = 2  # seconds
        while not os.path.exists(file_path) or os.path.getsize(file_path) != len(file_content):
            time.sleep(wait_time)
    except:
       st.write("Exception occured reading file contents")



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

# summariise data
def describe_data(data):
    if len(data) > 0:
        """ ###
        Shape of dataset 
        """
        #Get shape of data
        shape = data.shape

        st.write(" ###### Dataset has {} rows and {} columns".format(shape[0],shape[1])) 
       
        # Take a peep at the data
        """ ### Explore your data
        View first 5 rows
        """

        st.write(data.head())

        """ ###
        Columns in dataset
        """
        #Get columns
        st.write(data.columns)

        """ ###
        Datatypes in dataset 
        """
        #Get data types
        st.write(data.dtypes)
        
        numerical_dtypes = ['int64', 'float64']  

        if all(dt in numerical_dtypes for dt in data.dtypes):
            st.write("Dataset contains only numerical data types")
            """ ###
           Summary  
             """
            st.write(data.describe())
        else:
            st.write(""" #### Dataset contains non-numerical data types""")

            """ ###
            Summary of numerical fields
            """
            #Descriptive summary
            st.write(data.describe())

            """ ###
            Summary of categorical fields
            """
            #Descriptive summary
            st.write(data.select_dtypes(exclude=['int64','float64']).describe())



#What fields have  null values

def get_null_stats(data):
    
    """ ###
         Missing values in dataset
    """
    #What is the percentage of these null values 
    null_fields = get_null_fields(data)[0]

    if len(null_fields) == 0:
        st.write("Dataset has no missing values")
        return

    null_fields_names = get_null_fields(data)[1]


    st.write(null_fields)
    
    for col in null_fields_names:
        null_fields[col] = null_fields[col]*100/len(data)

    null_fields = null_fields.rename("Missing Values %")
    st.write("(n_null/n_rows) % for each column")
    st.write(null_fields)


def get_null_fields(data):
    null_stats = data.isnull().sum()
    null_fields = null_stats[null_stats>0]

    null_fields = null_fields.rename("Missing Values")
    #What is the percentage of these null values 
    null_fields_names = null_fields.index

    return (null_fields,null_fields_names)


def plot_data(data):
     st.write("Plotting columns {}".format(data.columns[1]))
     st.line_chart(data[data.columns[1]])



#read input

file = st.file_uploader("pick a file")

if file:
    upload_file(file)

    file_path = os.path.join("datasets",file.name)
    input = read_input(file_path)

    if input[0] is None:
        st.write("Provided file ' {} ' in ivalid".format(input[1]))
    else:
        st.write("Loaded dataset {}".format(file_path))
        data = input[0]
       
        describe_data(data)

        get_null_stats(data)

       
