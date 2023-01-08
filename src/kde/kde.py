
import psycopg2
import logging
import os
from kde_maps import kde_grid
import numpy as np
import matplotlib.pyplot as plt
import pysal as ps
from numpy import savetxt

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

def getlocations(taxonkey):
    '''
    It returns an array with locations for a taxonkey
    parameters:
        taxonkey: array(int)
    returns:
        array: (lon, lat)
    '''
    global connect
    try:
        sql= f"""
                select 
                    st_x(geom), st_y(geom)
                from  
                    accidentes_animales_final
                where geom is not null
                    and taxonkey = '{taxonkey}'
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
                ret.append(inci)
        return ret

    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return None

def compute_kde(locations, animal):
    '''
    It computes KDE
    parameters:
        locations: Array(lon, lat)
    returns:
        plot
    '''

    pts = np.array(locations)
    xyz, gdim = kde_grid(pts, spaced=0.01)
    x = xyz[:, 0].reshape(gdim)
    y = xyz[:, 1].reshape(gdim)
    z = xyz[:, 2].reshape(gdim)

    # Save x,y,z 
    savetxt(f"./kde/img/{animal}.csv", xyz, delimiter=',')

    # Create graphics
    levels = np.linspace(0, z.max(), 100)
    f = plt.figure(figsize=(8, 4))
    ax1 = f.add_subplot(121)
    ax1.contourf(x, y, z, levels=levels, cmap=plt.cm.YlOrRd)
    ax1.set_title(f"KDE Animal = {animal}")
    ax1.set_xlabel("Longitude")
    ax1.set_ylabel("Latitude")
    ax2 = f.add_subplot(122)
    ax2.scatter(pts[:, 0], pts[:, 1], s=1)
    ax2.set_title("Original locations")
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")
    f.savefig(f"./kde/img/{animal}.png", dpi=300)

    plt.close(f)
    

def process_kde():
    '''
    It computes KDEs
    parameters:
    returns:
    '''
    global connect
    try:
        sql= f"""
                 select 
                    distinct taxonkey, nombre_tipo_animal_1f 
                from 
                    accidentes_animales_final 
                where taxonkey != ''
                order by taxonkey
        """

        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) > 0:
            for row in rows:
                taxonkey = row[0]
                animal = row[1]
                logging.info(f"Processing taxonkey = {taxonkey} animal = {animal}")
                locations = getlocations(taxonkey)
                compute_kde(locations, animal)

    except Exception as e:
        logging.error(f'cannot process {taxonkey} {e}')	
        return None

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("----------------- Starting process ----------------- ")
    connect = ''
    connect = conn()
    process_kde()
    close()
    logging.info("-----------------  End process ----------------- ")    