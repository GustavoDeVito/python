import streamlit as st
import pymongo
import pandas as pd

st.title('Usuários')

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()
db = client[st.secrets["mongo"]["database"]]

@st.cache_data(ttl=600)
def get_users():
    collection = db['users'].find({}, { "_id": 0, "type": 1, "register": 1 })
    df = pd.DataFrame(collection)

    df['Tipo'] = df['type'].apply(lambda x: "Colaborador" if str(x) == "EMPLOYEE" else "Médico")
    df['Registro/CRM'] = df["register"].map(str)
    
    del df["type"]
    del df["register"]
    
    df.set_index("Registro/CRM", inplace=True)

    df.reset_index()
    
    return df 

users = get_users()
st.write(users)