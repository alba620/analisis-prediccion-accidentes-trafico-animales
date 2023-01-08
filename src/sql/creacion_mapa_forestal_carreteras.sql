-- Se elimina la tabla mapa_forestal_carreteras si existiera
DROP TABLE IF EXISTS mapa_forestal_carreteras;

-- Se crea la tabla mapa_forestal_carreteras definiendo los campos
CREATE TABLE public.mapa_forestal_carreteras (
	id int4 NULL,
	geom public.geometry NULL,
	roadname varchar NULL
);