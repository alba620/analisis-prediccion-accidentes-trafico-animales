import psycopg2
import logging
import os
import requests
import json
import urllib.parse
import pk2loc

URL_GEOMETRY = safe_string = urllib.parse.quote_plus('{"xmin":-2245414.0942030605,"ymin":3081941.0052346983,"xmax":587036.432889899,"ymax":5459438.364081839,"spatialReference":{"wkid":102100}}')
dict_url = {
    "2015" : f"https://mapas.fomento.gob.es/arcgis/rest/services/MapaTrafico/Mapa2015web/MapServer/2/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=4891&geometry={URL_GEOMETRY}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=OBJECTID%2Cprovincia%2Cnombre%2Ctipo_carretera%2Cpk_inicio%2Cpk_fin%2Clongitud%2Cvh_km_total%2Cvh_km_ligeros%2Cvh_km_pesados%2Cimd_total%2Cimd_ligeros%2Cimd_pesados&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A4891%2C%22extent%22%3A%7B%22type%22%3A%22extent%22%2C%22xmin%22%3A23816.994099999778%2C%22ymin%22%3A3902418.0131%2C%22xmax%22%3A1007380.8782000002%2C%22ymax%22%3A4847940.832699999%2C%22spatialReference%22%3A%7B%22wkid%22%3A25830%2C%22latestWkid%22%3A25830%7D%7D%7D",
    "2016" : f"https://mapas.fomento.gob.es/arcgis/rest/services/MapaTrafico/Mapa2016web/MapServer/2/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=4891&geometry={URL_GEOMETRY}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=OBJECTID%2Cprovincia%2Cnombre%2Ctipo_carretera%2Cpk_inicio%2Cpk_fin%2Clongitud%2Cvh_km_total%2Cvh_km_ligeros%2Cvh_km_pesados%2Cimd_total%2Cimd_ligeros%2Cimd_pesados&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A4891%2C%22extent%22%3A%7B%22type%22%3A%22extent%22%2C%22xmin%22%3A23816.994099999778%2C%22ymin%22%3A3902418.0131%2C%22xmax%22%3A1007380.8782000002%2C%22ymax%22%3A4847940.832699999%2C%22spatialReference%22%3A%7B%22wkid%22%3A25830%2C%22latestWkid%22%3A25830%7D%7D%7D",
    "2017" : f"https://mapas.fomento.gob.es/arcgis/rest/services/MapaTrafico/Mapa2017web/MapServer/2/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=4891&geometry={URL_GEOMETRY}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=OBJECTID%2Cprovincia%2Cnombre%2Ctipo_carretera%2Cpk_inicio%2Cpk_fin%2Clongitud%2Cvh_km_total%2Cvh_km_ligeros%2Cvh_km_pesados%2Cimd_total%2Cimd_ligeros%2Cimd_pesados&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A4891%2C%22extent%22%3A%7B%22type%22%3A%22extent%22%2C%22xmin%22%3A23816.994099999778%2C%22ymin%22%3A3902418.0131%2C%22xmax%22%3A1007380.8782000002%2C%22ymax%22%3A4847940.832699999%2C%22spatialReference%22%3A%7B%22wkid%22%3A25830%2C%22latestWkid%22%3A25830%7D%7D%7D",
    "2018" : f"https://mapas.fomento.gob.es/arcgis/rest/services/MapaTrafico/Mapa2018web/MapServer/2/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=4891&geometry={URL_GEOMETRY}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=OBJECTID%2Cprovincia%2Cnombre%2Ctipo_carretera%2Cpk_inicio%2Cpk_fin%2Clongitud%2Cvh_km_total%2Cvh_km_ligeros%2Cvh_km_pesados%2Cimd_total%2Cimd_ligeros%2Cimd_pesados&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A4891%2C%22extent%22%3A%7B%22type%22%3A%22extent%22%2C%22xmin%22%3A23816.994099999778%2C%22ymin%22%3A3902418.0131%2C%22xmax%22%3A1007380.8782000002%2C%22ymax%22%3A4847940.832699999%2C%22spatialReference%22%3A%7B%22wkid%22%3A25830%2C%22latestWkid%22%3A25830%7D%7D%7D",
    "2019" : f"https://mapas.fomento.gob.es/arcgis/rest/services/MapaTrafico/Mapa2019web/MapServer/2/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=4891&geometry={URL_GEOMETRY}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=OBJECTID%2CProvincia%2CNombre%2CTipo_de_ca%2CPk_inicio%2CPk_fin%2CLongitud%2Cvh_km_tota%2Cvh_km_lige%2Cvh_km_pesa%2CID%2CTipo%2CIMD_total%2CIMD_ligero%2CIMD_pesado&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A4891%2C%22extent%22%3A%7B%22type%22%3A%22extent%22%2C%22xmin%22%3A23817.173499999568%2C%22ymin%22%3A3902546.972100001%2C%22xmax%22%3A1007492.8156000003%2C%22ymax%22%3A4847946.387800001%2C%22spatialReference%22%3A%7B%22wkid%22%3A25830%2C%22latestWkid%22%3A25830%7D%7D%7D",
    "2020" : f"https://mapas.fomento.gob.es/arcgis/rest/services/MapaTrafico/Mapa2020web/MapServer/1/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=4891&geometry={URL_GEOMETRY}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=id_trafico%2Cgeom%2Cvia%2Cclase%2Cprovincia%2Cpkinicio_t%2Cpkfin_t%2Clongitud%2Cvhkmtot%2Cvhkmlig%2Cvhkmpes%2Cimdtot%2Cimdlig%2Cimdpes%2Cesri_oid&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A4891%2C%22extent%22%3A%7B%22type%22%3A%22extent%22%2C%22xmin%22%3A23817.173499999568%2C%22ymin%22%3A3902546.972100001%2C%22xmax%22%3A1007490.1045000004%2C%22ymax%22%3A4847205.210200001%2C%22spatialReference%22%3A%7B%22wkid%22%3A25830%2C%22latestWkid%22%3A25830%7D%7D%7D",
}

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

def insert_features(features, year, with_geom = False):
    '''
    It inserts IMD data into imds table of tfm database
    parameters:
        features: array with features
        with_geom: boolean True if geom is included in insert. Default False
    returns:
        True
    '''
    global connect

    conn()

    for feature in features:
        
        # Depending on the year, some features are evaluated due to format or name differences
        if year == '2020':
            objectid = feature['attributes']['id_trafico']
        else:
            objectid = feature['attributes']['OBJECTID']
        if year == '2019':
            provincia = feature['attributes']['Provincia']
        else:
            provincia = (feature['attributes']['provincia']).upper()
        if provincia == 'ORENSE':
            provincia = 'OURENSE'
        if year == '2019':
            nombre = feature['attributes']['Nombre']
        elif year == '2020':
            nombre = feature['attributes']['via']
        else:
            nombre = feature['attributes']['nombre']
        if year == '2019':
            tipo_carretera = feature['attributes']['Tipo_de_ca']
        elif year == '2020':
            tipo_carretera = feature['attributes']['clase']
        else:
            tipo_carretera = feature['attributes']['tipo_carretera']        
        if year == '2019':
            if feature['attributes']['Pk_inicio'] == '':
                pk_inicio = 0     # 0 will be equivalent to NA
            else:
                pk_inicio = int(feature['attributes']['Pk_inicio'].replace( "+", ""))
        elif year == '2020':
            pk_inicio = int(feature['attributes']['pkinicio_t'].replace( "+", ""))
        else:
            if feature['attributes']['pk_inicio'] == '' or feature['attributes']['pk_inicio'] == ' ':
                pk_inicio = 0     # 0 will be equivalent to NA
            else:
                pk_inicio= int(feature['attributes']['pk_inicio'].replace( "+", ""))  # Original format "202+500"
        if year == '2019':
            if feature['attributes']['Pk_fin'] == '':
                pk_fin = 0     # 0 will be equivalent to NA
            else:
                pk_fin = int(feature['attributes']['Pk_fin'].replace( "+", ""))
        elif year == '2020':
            pk_fin = int(feature['attributes']['pkfin_t'].replace( "+", ""))                 
        else:
            if feature['attributes']['pk_fin'] == ' ':
                pk_fin = 0     # 0 will be equivalent to NA
            else:
                pk_fin = int(feature['attributes']['pk_fin'].replace( "+", "")) 
        if year == '2019':
            longitud = feature['attributes']['Longitud']
        else:
            longitud = feature['attributes']['longitud']
        if year == '2019':
            vh_km_total = feature['attributes']['vh_km_tota']
        elif year == '2020':
             vh_km_total = feature['attributes']['vhkmtot']
        else:      
            vh_km_total = feature['attributes']['vh_km_total']
        if year == '2019':
            vh_km_ligeros = feature['attributes']['vh_km_lige']
        elif year == '2020':
            vh_km_ligeros = feature['attributes']['vhkmlig']
        else: 
            vh_km_ligeros = feature['attributes']['vh_km_ligeros']
        if year == '2019':
            vh_km_pesados = feature['attributes']['vh_km_pesa']
        elif year == '2020':
            vh_km_pesados = feature['attributes']['vhkmpes']
        else: 
            vh_km_pesados = feature['attributes']['vh_km_pesados']
        if year == '2019':
            imd_total = feature['attributes']['IMD_total']
        elif year == '2020':
            imd_total = feature['attributes']['imdtot']
        else: 
            imd_total = feature['attributes']['imd_total']
        if year == '2019':
            imd_ligeros = feature['attributes']['IMD_ligero']
        elif year == '2020':
            imd_ligeros = feature['attributes']['imdlig']
        else: 
            imd_ligeros = feature['attributes']['imd_ligeros']
        if year == '2019':
            imd_pesados = feature['attributes']['IMD_pesado']
        elif year == '2020':
            imd_pesados = feature['attributes']['imdpes']
        else: 
            imd_pesados = feature['attributes']['imd_pesados']
        
        logging.info(f"Processing year = {year} objectid = {objectid}")

        # check if year, objectid exists
        try:
            sql_object = f"select count(*) from imds where objectid = {objectid}"
            cur = connect.cursor()
            cur.execute(sql_object)
            rows = cur.fetchall()
            num_exists = rows[0][0]
            if num_exists > 0:
                break
        except Exception as e:
            logging.error(f'cannot get provincia {e}')	

        # get lon, lat from provincia, nombre, pk_inicio
        if with_geom:
            try:
                a,b = 'áéíóúüñÁÉÍÓÚÜ','aeiouunAEIOUU'   # without accents
                trans = str.maketrans(a,b)
                sql = f"""
                        select id from provincias where name = '{provincia.translate(trans)}'
                """
                cur = connect.cursor()
                cur.execute(sql)
                rows = cur.fetchall()
                num_provincia = rows[0][0]
            except Exception as e:
                logging.error(f'cannot get provincia {e}')	
            
            # Calculate mean value of segment
            pk_imd = pk_inicio + abs((pk_inicio - pk_fin) / 2)      
            loc = pk2loc.get_xy(num_provincia, nombre, pk_imd / 1000)
            if loc != None:
                geom = f"ST_SetSRID(ST_Point({loc[0]}, {loc[1]}),4326)"
            
            # Calculate mean value of segment correctign additional 0
            else:
                pks = [pk_inicio, pk_fin]
                pk_imd = min(pks) + abs((max(pks)/10 - min(pks)) / 2)
                loc = pk2loc.get_xy(num_provincia, nombre, pk_imd / 1000)
                
                if loc != None:
                    geom = f"ST_SetSRID(ST_Point({loc[0]}, {loc[1]}),4326)"
                
                # Calculate mean value of segment correcting additional 0 in each variable
                else: 
                    pk_imd = pk_inicio/10 + abs(((pk_inicio/10) - (pk_fin/10)) / 2)
                    loc = pk2loc.get_xy(num_provincia, nombre, pk_imd / 1000)
                    
                    if loc != None:
                        geom = f"ST_SetSRID(ST_Point({loc[0]}, {loc[1]}),4326)"
                
                    else:
                        geom = 'NULL'
        else:
            geom = 'NULL'

        try:
            sql= f"""INSERT INTO public.imds
                (objectid, provincia, nombre, tipo_carretera, pk_inicio, pk_fin, longitud, vh_km_total, vh_km_ligeros, vh_km_pesados, imd_total, imd_ligeros, imd_pesados, year, geom)
                VALUES({objectid},'{provincia}', '{nombre}', '{tipo_carretera}', {pk_inicio}, {pk_fin}, {longitud}, {vh_km_total}, {vh_km_ligeros}, {vh_km_pesados}, {imd_total}, {imd_ligeros}, {imd_pesados}, {year}, {geom});
                    """

            curIMD= connect.cursor()
            curIMD.execute(sql)
            connect.commit()
        except Exception as e:
            logging.error(f'cannot insert into imds \n{sql} \{e}')	
            connect.rollback()
            

    close()

    return True

def get_imd_fromurl(url):
    '''
    It retrieves data from DGT website
    parameter: 
        url: str
    returns:
        raw_data: array
    '''

    try:
        r = requests.get(url, verify = False)
        raw_data = json.loads(r.text)
        return raw_data
    except Exception as e:
        logging.error(f"Cannot get data from url {e}")
        return None

def query_imdfromdb(sql):
    '''
    It gets imd_total from location
    parameters:
        sql: str
    returns:
        int: imd_total value or 0 if not found
    '''
    global connect
    try:
        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = rows[0][0]
        return ret
    except Exception as e:
        logging.error(f'cannot get imd from db {e}')	
        return 0

def get_imd_fromdb(lon, lat, carretera, anyo):
    '''
    It gets imd_total from location
    parameters:
        lon: float
        lat: float
        carretera: str
        anyo: int
    returns:
        int: imd_total value or 0 if not found
    '''
    global connect
    try:
        sql= f"""
                select imd_total
                from 
                    imds i 
                where geom is not null
                and nombre = '{carretera}'
                and year = {anyo}
                order by st_distance(ST_SetSRID(ST_Point({lon}, {lat}),4326), geom)
                limit 1
        """
        imd = query_imdfromdb(sql)
        if imd == 0:
            sql= f"""
                select imd_total
                from 
                    imds i 
                where geom is not null
                and year = {anyo}
                order by st_distance(ST_SetSRID(ST_Point({lon}, {lat}),4326), geom)
                limit 1
             """
            imd = query_imdfromdb(sql)
        
        return imd

    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return 0