-- Se actualiza el campo coordinateuncertaintyinmeters para poder tratarlo
update animales_gbif set coordinateuncertaintyinmeters = 0 where coordinateuncertaintyinmeters = '';
update animales_gbif set coordinateuncertaintyinmeters = 1000 where coordinateuncertaintyinmeters = '0';

-- Se crea el contenido del campo geom
update 	animales_gbif set geom = ST_SetSRID(ST_Point(replace(decimallongitude,',','.')::double precision , replace(decimallatitude,',','.')::double precision),4326) 
where decimallongitude != ''
and length(decimallatitude) < 9;

-- Se crea el contenido del campo buff
update animales_gbif set buff = st_buffer(geom::geography, replace(coordinateuncertaintyinmeters ,',','.')::double precision)::geometry
where geom is not null 
and  replace(coordinateuncertaintyinmeters ,',','.')::double precision < 28000;

-- Sentencia para visualizar el geom o el buff en QGIS y comprobar el resultado
select
	row_number() over () as id 
	, ag.taxonkey 
	, etiqueta
	, geom
	, replace(coordinateuncertaintyinmeters ,',','.')::double precision
	, st_buffer(geom::geography, replace(coordinateuncertaintyinmeters ,',','.')::double precision) buff
from animales_gbif ag 
inner join aux_tipo_animal_1 as aa
on aa.taxonkey = ag.taxonkey
where geom is not null 
and  replace(coordinateuncertaintyinmeters ,',','.')::double precision < 28000