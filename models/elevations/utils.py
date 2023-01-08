import psycopg2
import logging
import os
from models import Sheet_data
import numpy as np

def conn():
    '''
    It opens connection to tfm database
    parameters:
    returns:
        the connection
    '''
    global connect
    try:

        connect = psycopg2.connect(f"dbname='{os.environ['POSTGRES_DATABASE']}' user='{os.environ['POSTGRES_USER']}' host='{os.environ['POSTGRES_HOST']}' port='{os.environ['POSTGRES_PORT']}' password='{os.environ['POSTGRES_PASSWORD']}'")
        logging.info("Connected to database")
        return connect
    except Exception as e:
        logging.error('Trying to connecto to BD' + str(e))
        return None

def close():
    '''
    It closes connection to tfm database
    parameters:
    returns:
    '''
    global connect
    connect.close()

def read():
    '''
    It returns array with data to get location
    parameters:
    returns:
        array: Incidence
    '''
    global connect

    try:
        sql= f"""
                select 
                    id_num, longitud, latitud
                from  
                    accidentes_no aaf 
                where 
                    geom is not null
                    and altitud is null
                order by id_num
        """

        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = []
        if len(rows) > 0:
            for row in rows:
                inci = []
                inci.append(row[0])
                inci.append(row[1])
                inci.append(row[2])

                ret.append(inci)
        return ret
    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return None

def get_hoja(lon, lat):
    '''
    It returns sheet number from MTN50 
    parameters:
        lon: float
        lat: float
    returns:
        str: sheet number
    '''
    global connect


    try:
        sql_object = f"select mtn50_clas from mtn50 m where st_within(ST_SetSRID(ST_Point({lon}, {lat}),4326), geom_polygon)"
        cur = connect.cursor()
        cur.execute(sql_object)
        rows = cur.fetchall()
        mtn50_clas = rows[0][0]
        return mtn50_clas
    except Exception as e:
        logging.error(f'cannot get sheet number {e}')	
        return None
    
def get_datos_hoja(sheet):
    '''
    It returns data asociated to sheet 
    parameters:
        sheet: str
    returns:
        str: sheet number
    '''
    global connect

    try:
        sql_object = f"select fichero, hoja, epsg from mtn50_hojas_alturas where hoja = '{sheet}'"
        cur = connect.cursor()
        cur.execute(sql_object)
        rows = cur.fetchall()
        sheet_data = Sheet_data
        sheet_data.filename = rows[0][0]
        sheet_data.sheet = sheet
        sheet_data.epsg = rows[0][2]
        return sheet_data
    except Exception as e:
        logging.error(f'cannot get sheet data {e}')	

        return None

def get_datos_fichero(sheet_data: Sheet_data, lon, lat):
    '''
    Returns height data
    parameters:
        sheet_data: Sheet_data
        lon: float
        lat: float
    returns:
        height
    '''

    try:
        path = f"{os.environ['PATH_ELEVATION']}{sheet_data.filename}"
        data_file = open(path)
        lines = data_file.readlines()

        # It reads header data
        num_linea = 1
        for line in lines:
            if num_linea == 1:
                ncols = float(line.split(' ')[1].replace('\n',''))
            if num_linea == 2:
                nrows = float(line.split(' ')[1].replace('\n',''))
            if num_linea == 3:
                xllCenter = float(line.split(' ')[1].replace('\n',''))
            if num_linea == 4:
                yllCenter = float(line.split(' ')[1].replace('\n',''))
            if num_linea == 5:
                cellsize = float(line.split(' ')[1].replace('\n',''))
                break
            num_linea = num_linea + 1

        # Displacement from center to corner
        xllCorner = xllCenter - (ncols / 2)
        yllCorner = yllCenter - (nrows / 2)
        cellY = int((lat - yllCorner) / cellsize)
        cellX = int((xllCorner - lon) / cellsize)
        line = lines[cellY]

        # Line is being evaluated/separated at every " "
        myArray = np.fromstring(line, dtype = float, sep = ' ')

        # Pick out the right "column" from my array
        cellValue = myArray[cellX] 

        return cellValue

    except Exception as e:
        logging.error(f'cannot get file data {e}')	
        return None

def update_record(altitud, id):
    '''
    Update altitud record
    parameters:
        altitud: float
        id: int
    returns:
        True
    '''
    global connect

    try:
        sql= f"""
            update accidentes_no set altitud = {altitud}  where id_num = {id}
        """
        cur= connect.cursor()
        cur.execute(sql)
        connect.commit()
    except Exception as e:
        logging.error(f'cannot update incidence \n{sql} \{e}')	
        connect.rollback()
        return False

    return True