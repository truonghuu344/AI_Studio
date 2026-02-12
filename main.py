import streamlit as st
from Database.Database import init_db
from CSS import local_css
from Tabs.Generate_Image import render_Generate_Image
from Tabs.Lifestyle_Shot import render_Lifestyle_Shot
from Tabs.AI_Chatbot import render_AI_Chatbot
from Tabs.Sidebar import render_side_bar
from Tabs.History_Tab import render_History_Tab

local_css()

init_db()



# Sidebar
render_side_bar()


# Tabs
st.title("Text to image")
GenerateImage, LifestyleShot, HistoryTab = st.tabs(["Generate Image", "Lifestyle Shot", "History Tab"])

render_AI_Chatbot()

#Tab1
with GenerateImage:
    render_Generate_Image()
#Tab2
with LifestyleShot:
    render_Lifestyle_Shot()
#Tab3
with HistoryTab:
    render_History_Tab()




