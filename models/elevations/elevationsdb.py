#!/bin/python

'''
Update table accidentes_no with altura data
'''
import logging
import psycopg2
import os
from models import Sheet_data  
import utils
from pyproj import Proj, transform
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def update_height(incidences):
    '''
    It updates height in incidences table
    parameters: 
        incidences: array
    returns:
    '''

    for inci in incidences:

        id = inci[0]
        lon = inci[1]
        lat = inci[2]
        logging.info(f"Processing id_num = {id}")
    
        # Get the sheet 
        num_sheet = utils.get_hoja(lon, lat)
        if num_sheet != '1105/1108':
            sheet_data = utils.get_datos_hoja(num_sheet)
        else:
            sheet_data = utils.get_datos_hoja('1105-1108')
        
        # Reproject lon, lat of our position to X, Y of sheet
        if sheet_data is not None:
            in_proj = Proj(init='epsg:4326')
            out_proj = Proj(init=f'epsg:{sheet_data.epsg}')
            x,y = transform(in_proj,out_proj,lon,lat)
            altitud = utils.get_datos_fichero(sheet_data, x, y)

            # Update the record
            utils.update_record(altitud, id)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("------------------- Starting process update_height ------------------- ")
    connect = utils.conn()
    incidences = utils.read()
    update_height(incidences)
    utils.close()
    logging.info("------------------- End process------------------- ")    