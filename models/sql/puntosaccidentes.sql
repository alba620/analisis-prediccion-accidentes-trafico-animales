-- Se generan los puntos aleatorios dentro de las geometrías de las carreteras
insert into puntosnoaccidentes (geom)
select 
ST_LineInterpolatePoint(ST_LineMerge(
	        ST_SnapToGrid(
	            geom_4326,
	            0.001))
	        , random()) 
from 
	carreteras c 
where 
geom_4326 is not null
and ST_GeometryType(ST_LineMerge(
	        ST_SnapToGrid(
	            geom_4326,
	            0.001)
	        )) = 'ST_LineString'

-- Se pueblan los campos de lon y lat a partir del geom	        
update puntosnoaccidentes set lon = st_x(geom), lat = st_y(geom)

-- Se intertan los campos generados en la tabla accidentes_no
insert into accidentes_no (id_num , geom, longitud, latitud)
select row_number() over(), geom, lon, lat from puntosnoaccidentes