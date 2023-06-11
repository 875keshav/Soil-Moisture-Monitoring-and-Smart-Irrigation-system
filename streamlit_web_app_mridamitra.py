import requests
import time
import json
import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# API URL
endpoint = "https://api.thingspeak.com/channels/2054475/feeds/last.json?api_key=ENXUTSE126BOWSD9"
response = requests.get(endpoint)
data_disc=json.loads(response.text)
Moisture=(1-int(data_disc['field1'])/1024)*100
Humidity=data_disc['field2']
Temperature=data_disc['field3']

# Importing trained model
final_model = pickle.load(open('trained_model1.pkl', 'rb'))

# Sidebar
rad=st.sidebar.radio("Navigation",["Home","Previous Readings","Prediction"],key="Navigation")
if rad=="Home":
        # st.title("Smart Irrigation System !")
        st.title("MridaMitra!")
        st.image('soil-moisture.jpg')
        st.markdown(
        """
            MridaMitra is based on the soil moisture monitoring system. It helps the farmers by giving the idea about when to irrigate the field or when to not. 
            It also help framers to maintain a constant moisture level in the field.
        """
         )
elif rad=="Previous Readings":
            # fetching the url for field1
            endpoint = "https://api.thingspeak.com/channels/2054475/fields/1.json?api_key=ENXUTSE126BOWSD9&results=100"
            response = requests.get(endpoint)
            data=json.loads(response.text)
            # print(data)
            a=data["feeds"]
            list=[]
            for i in range(len(a)):
                b=a[i]
                list.append(b)
            print(list)
            list1=[]
            list2=[]
            list3=[]
            for i in range(len(list)):
                c=list[i]
                field1_time=c["created_at"]
                field1_entry_no=c["entry_id"]
                field1_moisture=c["field1"]
                list1.append(field1_time)
                list2.append(field1_entry_no) 
                list3.append((1-int(field1_moisture)/1024)*100 )   
            
            # Fetching the url for field2
            endpoint = "https://api.thingspeak.com/channels/2054475/fields/2.json?api_key=ENXUTSE126BOWSD9&results=100"
            response = requests.get(endpoint)
            data=json.loads(response.text)
            #print(data)
            a=data["feeds"]
            list=[]
            for i in range(len(a)):
                b=a[i]
                list.append(b)
            print(list)
            list4=[]
            for i in range(len(list)):
                c=list[i]
                field1_humidity=c["field2"]
                list4.append(field1_humidity) 

            # fetching url for field3
            endpoint = "https://api.thingspeak.com/channels/2054475/fields/3.json?api_key=ENXUTSE126BOWSD9&results=100"
            response = requests.get(endpoint)
            data=json.loads(response.text)
            print(data)
            a=data["feeds"]
            list=[]
            for i in range(len(a)):
                b=a[i]
                list.append(b)
            print(list)
            list5=[]
            for i in range(len(list)):
                c=list[i]
                field1_temperature=c["field3"]
                list5.append(field1_temperature)  


            df=pd.DataFrame([list1,list2,list5,list4,list3])
            df.index=["Time","Entry No.","Temperature","Humidity","Moisture"]
            st.subheader("Previous entries :")
            st.write(df)
            st.subheader("")
            # st.write(" Moisture vs Temperature")

            # fig, ax = plt.subplots(figsize=(8,4))
            # ax.scatter(list5[-12:-1:1], list3[-12:-1:1])
            # plt.xlabel("Temperature")
            # plt.ylabel("Moisture")
            
            # st.pyplot(fig)
            # st.subheader("")
            # st.write(" Moisture vs Humidity")
            # fig, ax = plt.subplots(figsize=(8,4))
            # ax.scatter(list4[-12:-1:1], list3[-12:-1:1])
            # plt.xlabel("Humidity")
            # plt.ylabel("Moisture")
            # st.pyplot(fig)


                    
elif rad=="Prediction":
        st.header("Pump status prediction")

        st.subheader(" Current data fetched from the soil moisture monitoring system")
        st.write("Temperature= "+str(Temperature))
        st.write("Humidity= "+str(Humidity))
        st.write("Moisture= "+str(Moisture) )
        temperature= float(Temperature)
        humidity=float(Humidity)
        moisture=Moisture
        btn=st.button("predict")
        if btn:
            if temperature==0 or humidity==0:
                st.text("Processing, please wait .....")
                st.text("WARNING⚠️")
                st.text("Kindly enter correct data (No zero value should be passed)")
            else:
                st.text("Processing, please wait .....")
                pred=(final_model.predict(np.array([[temperature,humidity,moisture]])))
                x=pred[0]
            if pred[0]==0:
                st.subheader("Soil is wet.")
                st.subheader("Need not to irrigate the crop!")
            else:
                st.subheader("Soil is dry.")
                st.subheader("Required to irrigate the crop!")
            
#footer
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )
    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )
    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )
    st.markdown(style, unsafe_allow_html=True)
    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        "©️ Keshavagrawal",
        br(),
        link("https://www.linkedin.com/in/keshav-kumar-agrawal-1a791523a?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BOGogIyiCTl2f%2FoGEejvoVA%3D%3D", image('https://icons.getbootstrap.com/assets/icons/linkedin.svg') ),
        br(),
        link("https://www.instagram.com/875keshav/",image('https://icons.getbootstrap.com/assets/icons/instagram.svg')),
    ]
    layout(*myargs)

if __name__ == "__main__":
    footer()           
            
                                

            