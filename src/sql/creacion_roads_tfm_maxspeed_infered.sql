-- Se elimina la tabla roads_tfm si existiera
DROP TABLE IF EXISTS roads_tfm;

-- Se crea la tabla roads_tfm que es una copia de roads para trabajar (Updated Rows	2634249)
create table roads_tfm
as 
select *
from roads_osm r;

-- Se crea el índice espacial
CREATE INDEX gist_roads_tfm ON public.roads_tfm USING gist (geom);

-- Se crea la nueva columna
ALTER TABLE public.roads_tfm ADD maxspeed_infered integer NULL;

-- Se actualiza el valor del campo de la nueva columna con el valor de maxspeed si es mayor que 0 (Updated Rows 138.277)
UPDATE roads_tfm 
set maxspeed_infered = maxspeed 
where maxspeed > 0;

-- Se infiere motorway y trunk (Updated Rows 33.272)
UPDATE roads_tfm 
set maxspeed_infered = 120 
where maxspeed = 0 and fclass in ('motorway', 'trunk');

-- Se infiere primary (Updated Rows	37.368)
UPDATE roads_tfm 
set maxspeed_infered = 90 
where maxspeed = 0 and fclass in ('primary');

-- Se infiere secondary, tertiary, unclassified (Updated Rows 349.788)
UPDATE roads_tfm 
set maxspeed_infered = 80 
where maxspeed = 0 and fclass in ('secondary', 'tertiary', 'unclassified');

-- Se infiere residential (Updated Rows	875.594)
UPDATE roads_tfm 
set maxspeed_infered = 50 
where maxspeed = 0 and fclass in ('residential');

-- Se infiere 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link' (Updated Rows 72.875)
UPDATE roads_tfm 
set maxspeed_infered = 60 
where maxspeed = 0 and fclass in ('motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link');

-- Se infiere 'living_street', 'service' y todas las opciones de 'track' (Updated Rows	874.777)
UPDATE roads_tfm 
set maxspeed_infered = 30 
where maxspeed = 0 and fclass in ('living_street', 'service', 'track', 'track_grade1', 'track_grade2', 'track_grade3', 'track_grade4', 'track_grade5');