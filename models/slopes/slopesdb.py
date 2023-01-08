#!/bin/python

'''
Update table accidentes_no with pendiente data
'''
import logging
import psycopg2
import os
from models import Sheet_data  
import utils
from pyproj import Proj, transform
import numpy as np
import warnings
import statistics
warnings.simplefilter(action='ignore', category=FutureWarning)


def update_slopes(incidences):
    '''
    It updates 'pendiente' in accidentes_no table
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
            logging.info(f"antes get_datos_fichero")
            slope = utils.get_datos_fichero(sheet_data, x, y)
            
            # Update the record
            utils.update_record(slope, id)


def update_slopes_opt():
    '''
    It updates 'pendiente' in accidentes_no table
    parameters: 
        incidences: array
    returns:
    '''
    global connect

    try:
        sql_object = f" select distinct hoja from pendientes_mtn50 pm2"
        cur = connect.cursor()
        cur.execute(sql_object)
        rows = cur.fetchall()
        for row in rows:
            hoja = row[0]
            
            try:
                # Red data from that sheet
                sheet_data = utils.get_datos_hoja(hoja)
                path = f"{os.environ['PATH_SLOPES']}{sheet_data.filename}"
                data_file = open(path)
                lines = data_file.readlines()

                # Read header data
                num_linea = 1
                for line in lines:
                    if num_linea == 1:
                        ncols = float(line.split('     ')[1].replace('\n',''))
                    if num_linea == 2:
                        nrows = float(line.split('     ')[1].replace('\n',''))
                    if num_linea == 3:
                        xllCenter = float(line.split('     ')[1].replace('\n',''))
                    if num_linea == 4:
                        yllCenter = float(line.split('     ')[1].replace('\n',''))
                    if num_linea == 5:
                        cellsize = float(line.split('     ')[1].replace('\n',''))
                        break
                    num_linea = num_linea + 1

                # Displacement from center to corner
                xllCorner = xllCenter - (ncols / 2)
                yllCorner = yllCenter - (nrows / 2)
            except Exception as e:
                logging.error(f'cannot get header from file {e}')



            # Calculate median slope for each point
            sql_ids = f"select id_num, st_x(geom), st_y(geom) from pendientes_mtn50 where hoja = '{hoja}' and pendiente is null"
            cur_ids = connect.cursor()
            cur_ids.execute(sql_ids)
            rows_ids = cur_ids.fetchall()
            for row_id in rows_ids:
                id_num = row_id[0]
                lon = row_id[1]
                lat = row_id[2]
                
                logging.info(f"Processing id = {id_num}")

                try:
                    # Reproject lon, lat of our position to X, Y of sheet
                    in_proj = Proj(init='epsg:4326') 
                    out_proj = Proj(init=f'epsg:{sheet_data.epsg}')
                    x,y = transform(in_proj,out_proj,lon,lat)
                    lon = x
                    lat = y
                
                    # Calculate median slope in 30-meter area 
                    limarea = 30
                    cellY = int((lat - yllCorner) / cellsize)
                    cellX = int((xllCorner - lon) / cellsize)
                    xmin = cellX - limarea
                    ymin = cellY - limarea
                    xmax = cellX + limarea
                    ymax = cellY + limarea
                    slopes = []
                    for dx in range (limarea):
                        for dy in range(limarea):
                            cellX = xmin + dx
                            cellY = ymin + dy
                            line = lines[cellY]
                            myArray = np.fromstring(line, dtype = float, sep = ' ')
                            cellValue = myArray[cellX]
                            slopes.append(cellValue)
                    median_slope = statistics.median(slopes)

                    # Update the record
                    utils.update_record(median_slope, id_num)
                except Exception as e:
                    logging.error(f'cannot process {e}')
                    utils.update_record(-9999, id_num)	

    except Exception as e:
        logging.error(f'cannot get data {e}')	
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("------------------- Starting process update_slope ------------------- ")
    connect = utils.conn()
    update_slopes_opt()
    utils.close()
    logging.info("------------------- End process------------------- ")    