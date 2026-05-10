import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=.;"
        "DATABASE=GatheringSystem;"
        "Trusted_Connection=yes;"
    )
