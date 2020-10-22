import datetime
import logging
import os
import pyodbc

import azure.functions as func

from azure.servicebus import ServiceBusClient, Message

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    bus_service = ServiceBusClient.from_connection_string(os.environ["ServiceBusConnection"])

    server = os.environ["sql_server"]
    database = os.environ["sql_database"]
    username = os.environ["sql_username"]
    password = os.environ["sql_password"]

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    c = cnxn.cursor()
    sql_statement_warning = "Select top 20 percent * from devices where sla = 'WARNING'"
    c.execute(sql_statement_warning )
    #c.fetchall()

    for r in c:
        bus_service.get_topic('sensor-warning').send(Message(r))
        print(r)
        logging.info(r)
    
    sql_statement_critical = "Select top 20 percent * from devices where sla = 'CRITICAL'"
    c.execute(sql_statement_critical )
    c.fetchall()

    for x in c:
        bus_service.get_topic('sensor_critical').send(Message(x))
        print(x)
        logging.info(x)

    c.close()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
