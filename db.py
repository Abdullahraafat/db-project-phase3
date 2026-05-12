import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=.;"
        "Database=PremiumEventVenueDB;"
        "Trusted_Connection=yes;"
    )
