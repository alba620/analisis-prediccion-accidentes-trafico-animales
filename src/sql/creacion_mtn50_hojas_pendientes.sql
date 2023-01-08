-- Se elimina la tabla mtn50_hojas_pendientes si existiera
DROP TABLE IF EXISTS mtn50_hojas_pendientes;

-- Se crea la tabla mtn50_hojas_pendientes definiendo los campos
CREATE TABLE public.mtn50_hojas_pendientes (
	fichero varchar NULL,
	hoja varchar NULL,
	epsg varchar NULL
);