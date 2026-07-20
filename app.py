
import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px

st.set_page_config(page_title="Customer Feedback Dashboard",layout="wide")
st.title("📊 Customer Feedback Dashboard")

uploaded=st.file_uploader("Upload CSV",type="csv")
if uploaded:
    df=pd.read_csv(uploaded)
else:
    df=pd.read_csv("customer_feedback.csv")

if "Feedback" not in df.columns:
    st.error("CSV must contain a Feedback column.")
    st.stop()

def get_sentiment(text):
    p=TextBlob(str(text)).sentiment.polarity
    if p>0: return "Positive"
    if p<0: return "Negative"
    return "Neutral"

df["Sentiment"]=df["Feedback"].apply(get_sentiment)

search=st.text_input("Search feedback")
if search:
    df=df[df["Feedback"].str.contains(search,case=False,na=False)]

choice=st.selectbox("Filter",["All","Positive","Neutral","Negative"])
if choice!="All":
    df=df[df["Sentiment"]==choice]

c1,c2,c3=st.columns(3)
c1.metric("Total Feedback",len(df))
c2.metric("Positive",(df["Sentiment"]=="Positive").sum())
c3.metric("Negative",(df["Sentiment"]=="Negative").sum())

st.subheader("Feedback")
st.dataframe(df,use_container_width=True)

pie=px.pie(df,names="Sentiment",title="Sentiment Distribution")
st.plotly_chart(pie,use_container_width=True)

bar=px.bar(df["Sentiment"].value_counts().reset_index(),
           x="Sentiment",y="count",
           labels={"index":"Sentiment","count":"Count"},
           title="Sentiment Count")
st.plotly_chart(bar,use_container_width=True)

csv=df.to_csv(index=False).encode()
st.download_button("Download Results",csv,"results.csv","text/csv")
