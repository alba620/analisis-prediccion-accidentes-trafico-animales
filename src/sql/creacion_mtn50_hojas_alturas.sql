-- Se elimina la tabla mtn50_hojas_alturas si existiera
DROP TABLE IF EXISTS mtn50_hojas_alturas;

-- Se crea la tabla mtn50_hojas_alturas definiendo los campos
CREATE TABLE public.mtn50_hojas_alturas (
	fichero varchar NULL,
	hoja varchar NULL,
	epsg varchar NULL
);