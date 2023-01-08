#!/bin/python

'''
Transform provincia, carretera, pk to loc
'''
import requests
import logging
import os

def get_token():
    '''
    It returns token
    parameters:
    returns:
        token: str
    '''
    urlGetTokenArcgis = f"{os.environ['URL_GET_TOKEN_ARCGIS']}"
    try:
        payload = {'f':'json',
                    'username':f"{os.environ['GIS_USERNAME']}",
                    'password':f"{os.environ['GIS_PASSWORD']}",
                    'client': f"{os.environ['URL_GET_TOKEN_ARCGIS']}",
                    'referer' : 'arcgis.com',
                    'expiration' : '50000'
                    }
        resp_token = requests.post(urlGetTokenArcgis,data=payload).json()
        logging.debug(resp_token)
        return resp_token['token']
    except Exception as e:
        logging.error(e)
        return None

def get_xy(provincia, carretera, pk):

    '''
        Returns location from nomminal KP
        parameters:
            provincia: int province id in provincias table
            carretera: str road name
            pk: float kilemtric point
        returns:
            loc[]: [lon, lat]
    '''

    urlPKaXY = f"{os.environ['URL_PK2XY']}"
    token = get_token()
    try:
        payload = {'token':token,
                    'Provincia': str(provincia).zfill(2),
                    'Carretera': carretera,
                    'Km': pk,
                    'env:outSR' : '4326',
                    'env:processSR' : '4326',
                    'returnZ' : 'false',
                    'returnM' : 'false',
                    'f' : 'json'
                    }
        resp = requests.post(urlPKaXY,data=payload).json()
        logging.debug(resp)
        if resp['results']:
            if resp['results'][1]['value'] == "Sin incidencias":
                lon = resp['results'][2]['value']
                lat = resp['results'][3]['value']
                loc = []
                loc.append(lon)
                loc.append(lat)
                return loc
            elif resp['results'][1]['value'] == "No existe informaci?n de la carretera":
                return None
            else:
                logging.error(f"No se encuentra la posición para ese PK para {payload}")
                return None
        else:
            logging.error(f"No existe posicion para {payload}")
            return None
    except Exception as e:
        logging.error(e)
        return None

