import pickle as pk
import streamlit as st
import string
import re
import nltk
import joblib
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer as ps 


model =pk.load(open('model.pkl', 'rb'))
tfidf=pk.load(open('tfid.pkl','rb'))

st.title("Email-sms spam Classifier")
input_sms = st.text_area("Enter the message")
if st.button("Classify"):
# Proccessing of msg

    input_sms=re.sub(r'[^\w\s]','',input_sms)
    stopwords_list=stopwords.words('english')
    input_words_list=input_sms.split()
    filtered_words=[word for word in input_words_list if word not in stopwords_list]
    l=[]
    for i in filtered_words:
        l.append(ps().stem(i))
    l=" ".join(l)
    
#Vecorisation

    vector=tfidf.transform([l])
    
# Model Predict

    result=model.predict(vector)[0]

    if result==1:
        st.header('It is Spam')
    elif result==0:
        st.header('It is not Spam')