from flask import Flask, request
import pandas as pd
from pymongo import MongoClient
from crimeModel import crimeModel





app = Flask(__name__)


client = MongoClient("mongodb+srv://sysadmin:dinosaurio12@cluster0.tqljnl8.mongodb.net/python?retryWrites=true&w=majority")
db = client["python"]
collection = db["server"]




model = crimeModel()


@app.route("/service", methods=["POST","GET","OPTIONS"])


def index():
    if request.method == "POST" or request.method == "OPTIONS":

        post_data = request.get_json()
        
        print("-------")
        
        
        collection.insert_one(post_data)

        results = collection.find()


        df = pd.DataFrame(list(results))
        df = df.drop('_id', axis=1)

        model_df = df.iloc[-1]


        p = model.crimePrediction(list(model_df))
        print(df)
    

        return p

    return "Welcome to my Flask and MongoDB Atlas application!"


@app.route('/consulta', methods=["GET"])

def consulta():
    
    results = collection.find()


    df = pd.DataFrame(list(results))
    df = df.drop('_id', axis=1)

    model_df = df.iloc[-1]


    p = model.crimePrediction(list(model_df))
    print(df)
    
    return p

if __name__ == "__main__":
    app.run()
