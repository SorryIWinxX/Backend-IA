from flask import Flask, request
import pandas as pd
from pymongo import MongoClient
from crimeModel import crimeModel





app = Flask(__name__)


client = MongoClient("mongodb+srv://sysadmin:dinosaurio12@cluster0.tqljnl8.mongodb.net/python?retryWrites=true&w=majority")
db = client["python"]
collection = db["server"]




model = crimeModel()


@app.route("/service", methods=["POST"])


def index():
    if request.method == "POST":

        post_data = request.get_json()
        collection.insert_one(post_data)


        return "Post saved successfully!"


    return "Welcome to my Flask and MongoDB Atlas application!"


@app.route('/consulta', methods=["GET"])

def consulta():
    # Obtén la colección donde se encuentran los datos que deseas consultar

    # Define los filtros de búsqueda para la consulta

    

    # Realiza la consulta a la base de datos utilizando los filtros definidos
    results = collection.find()


    # Crea un dataframe a partir de los resultados obtenidos
    df = pd.DataFrame(list(results))
    df = df.drop('_id', axis=1)

    model_df = df.loc[2]


    p = model.crimePrediction(list(model_df))
    print(df)

    # Devuelve el dataframe al cliente
    return p 





if __name__ == "__main__":
    app.run()
