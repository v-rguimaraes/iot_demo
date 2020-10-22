import logging
import azure.functions as func
import os

import pyodbc


def main(msg: func.ServiceBusMessage, doc: func.Out[func.Document]):
    logging.info('Python ServiceBus queue trigger processed message: %s',msg.user_properties)

    #Insere no CosmosDB
    item = {
        "id": msg.message_id,
        "device_id": msg.user_properties.get("id"),
        "temperatura_c": msg.user_properties.get("temperatura"),
        "temperatura_f": msg.user_properties.get("temperatura")*1.8+32
    }
    doc.set(func.Document.from_dict(item))

    server = os.environ["sql_server"]
    database = os.environ["sql_database"]
    username = os.environ["sql_username"]
    password = os.environ["sql_password"]
   
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    c = cnxn.cursor()

    temp = msg.user_properties.get("temperatura")
    sla = 'NORMAL'
    if (temp > 24 & temp < 31):
        sla = "WARNING"
    elif (temp >= 30 ):
        sla = "CRITICAL"

    sql_statement = "insert into devices (device_id,temperatura,sla) values ('"+msg.user_properties.get("id")+"',"+str(msg.user_properties.get("temperatura"))+",'"+sla+"' )"
    logging.info(sql_statement)
    c.execute(sql_statement )
    c.commit()

    logging.info(item)

