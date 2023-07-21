from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib as mpl
import threading

import webbrowser
import shutil

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']
git_path = "https://github.com/Ruben-van-Breda/PandaDataAnalyser/tree/main"

mpl.rcParams['xtick.major.pad'] = 8

st.set_page_config(page_title="Pick n Pay", page_icon="🦌", layout="wide")
st.title("Pick n Pay")

st.cache(allow_output_mutation=True, persist=False)
def load_file():
    uploaded_file = st.file_uploader("Upload a file", type=['csv'])
    return uploaded_file

uploaded_file = load_file()
response = ""
def chat(df, prompt):
    # start thread and run method chat_with_data
    thread = threading.Thread(target=chat_with_data, args=(df, prompt))
    thread.start()
    thread.join()


    pass

def chat_with_data(df, prompt):
    llm = OpenAI(api_token=API_KEY)
    pandas_ai = PandasAI(llm, save_charts=True, save_charts_path=f"{git_path}/picknpay" , enforce_privacy=True)
    response = pandas_ai.run(df, prompt=prompt)
    return response




if uploaded_file is not None:
    st.write(uploaded_file)
    df = pd.read_csv(uploaded_file)
    st.write(df)

    prompt = st.text_area("Enter you query")

    if st.button("Ask"):
        if prompt:
            st.write("Processing query")
            response = chat_with_data(df, prompt)
            print(response)
            st.write(response)
        else:
            st.warning("Please enter a query")
else:
    st.warning("Please upload a file")

# show side bar of the page
st.sidebar.title("About")

# show a list of files in directory 
st.sidebar.subheader("Files")
curr_dir = os.getcwd()



# check if there are files in directory
if os.path.exists(f"{git_path}/picknpay/exports/charts/") and os.listdir(f"{git_path}/picknpay/exports/charts/"):

    if st.sidebar.button("Delete All", key="deleteAll"):
        # current directory
        curr_dir = os.getcwd()
        # delete all files in directory
        try:
            shutil.rmtree(f"{git_path}/picknpay/")
            # for i in os.listdir("./picknpay/exports/charts/"):
            #     os.remove(f"{curr_dir}/picknpay/exports/charts/{i}")
            # st.sidebar.write("All files deleted")
        except Exception as e:
            st.sidebar.write("No files found", e)
            pass

try:
    for i in os.listdir(f"{git_path}/picknpay/exports/charts/"):
        st.sidebar.write(i)

        for chart in os.listdir(f"{git_path}/picknpay/exports/charts/{i}"):
            # create a container
            if st.sidebar.button("Delete", i+'delete'):
                # current directory
                curr_dir = os.getcwd()
                os.remove(f"{git_path}/picknpay/exports/charts/{i}")
                st.sidebar.write("File deleted")
            # load image data
            image = open(f"{git_path}/picknpay/exports/charts/{i}/{chart}", 'rb').read()
            st.sidebar.download_button(label="Download", key=i+'download' ,data=image, file_name=chart)

            if st.sidebar.button("Open", i+chart):
                # download file
                curr_dir = os.getcwd()
                webbrowser.open_new_tab(f"{git_path}/picknpay/exports/charts/{i}/{chart}")
                
                
except Exception as e:
    st.sidebar.write("No files found")
                # webbrowser.open_new_tab(f"./picknpay/exports/charts/{i}/{chart}")


