"""
--Data ingestor engine for thingspeak API
--Please read the README of the project to 
--set your enviroment
@autor: Eng. Francis Zavaleta
"""
from ast import If
from dotenv import load_dotenv
import objects.DataUtils as du
import objects.DatabaseUtils as db
import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import streamlit as st

load_dotenv()


class ingestor_engine:
    def __init__(self) -> None:
        pass

    def main(self):

        self.__build_databases_tables()
        destinity_table = self.__get_parameters("SQL_MAIN_TABLE")
        data_to_insert = self.generate_dataframe()
        len_of_data = data_to_insert.shape[0]
        print("[engine] Searching new data to insert in database . . .")
        if self.__ingest_discriminator(data_to_insert, destinity_table) == "ok":
            print("[engine] inserting rows in database . . .")
            for row in range(0, len_of_data):
                values = data_to_insert.iloc[row].to_dict()
                try:
                    db.database().ingest(
                        values=values,
                        query_str=self.__build_insert_query(values, destinity_table),
                    )
                except:
                    print("[engine] got error on {} row".format(row))
        else:
            print("[engine] Nothing to fetch")
        print("[engine] All done, we are finished")

    def generate_dataframe(self):
        get_data_from_channel = requests.get(self.__build_url()).json()
        all_data_feed = get_data_from_channel["feeds"]

        sensor = du.operators(
            col=self.__get_parameters("ROW_FEED_FIELDS").split("+"),
            json_data=all_data_feed,
        )
        sensor_df = sensor.gen_dataframe()

        return sensor.clean_data(
            sensor_df, new_col=self.__get_parameters("ROW_DATABASE_FIELDS").split("+")
        )

    def __build_url(self):
        base_url = "{base}{channel}/feed.json?results={nrows}"
        return base_url.format(
            base=self.__get_parameters("THING_SPEAKS_URL"),
            channel=self.__get_parameters("THING_SPEAKS_CHANNEL_ID"),
            nrows=self.__get_parameters("THING_SPEAKS_ROWS"),
        )

    def __ingest_discriminator(self, df_, table):
        last_id_entry = df_["entry_id"].max()
        query_last_row = db.database().execute_from_str(
            "select max(entry_id) from {};".format(table)
        )
        if query_last_row[0][0] == None:
            query_last_row = [[0]]
        return "ok" if last_id_entry > query_last_row[0][0] else "no"

    def __get_parameters(self, parameter):
        return os.environ.get(parameter)

    def __build_databases_tables(self):
        data_engine = db.database()
        try:
            data_engine.execute_from_query(
                sql_file=self.__get_parameters("FILE_SQL_NAME")
            )
        except:
            print("[engine] Database tables already exist!!!")

    def __build_insert_query(self, dict_data, table):
        insert_str = "insert into {table} {fields} values {values};"
        fields = "{}".format(tuple(dict_data.keys()))
        values = "{}".format(tuple(dict_data.values()))

        return insert_str.format(table=table, fields=fields, values=values).replace(
            "'", ""
        )


ingestor_engine().main()


datautils = db.database()
dataframe = datautils.select_air_quality_sensors('air_quality_sensors') 


    
def generate_model(X, y):
    regr = make_pipeline(StandardScaler(), LinearRegression())
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    regr.fit(x_train,y_train)
    y_pred = regr.predict(x_test)
    r2 = metrics.r2_score( y_pred, y_test)
    return regr, r2




##modelo 2
X = dataframe[['Air_pressure', 'Humidity', 'temperature_', "Controller_temperature", "G"]]
y = dataframe['eCO2']

modelo1, r2_modelo1 = generate_model(X, y)



##modelo 2
X = dataframe[['Air_pressure', 'Humidity', 'temperature_', "Controller_temperature", "G"]]
y = dataframe['eTVOC']

modelo2, r2_modelo2 = generate_model(X, y)



st.header("Modelagem Regressão linear")
st.write("R2 Score Modelo eTVOC: ", r2_modelo2)
st.write("R2 Score Modelo eCO2: ", r2_modelo1)


col1, col2, col3 = st.columns(3)

with col1:
    st.write("Grafico Pressão do Ar e eTVOC")
    fig, ax = plt.subplots()
    ax.scatter(dataframe['Air_pressure'], dataframe['eTVOC'])
    st.pyplot(fig)

with col2:
    st.write("Grafico Temperatura e eTVOC")
    fig, ax = plt.subplots()
    ax.scatter(dataframe['temperature_'], dataframe['eTVOC'])
    st.pyplot(fig)

with col3:
    st.write("Grafico Umidade e eTVOC")
    fig, ax = plt.subplots()
    ax.scatter(dataframe['Humidity'], dataframe['eTVOC'])
    st.pyplot(fig)



col1, col2, col3 = st.columns(3)

with col1:
    st.write("Grafico Pressão do Ar e eCO2")
    fig, ax = plt.subplots()
    ax.scatter(dataframe['Air_pressure'], dataframe['eCO2'])
    st.pyplot(fig)

with col2:
    st.write("Grafico Temperatura e eCO2")
    fig, ax = plt.subplots()
    ax.scatter(dataframe['temperature_'], dataframe['eCO2'])
    st.pyplot(fig)

with col3:
    st.write("Grafico Umidade e eCO2")
    fig, ax = plt.subplots()
    ax.scatter(dataframe['Humidity'], dataframe['eCO2'])
    st.pyplot(fig)





