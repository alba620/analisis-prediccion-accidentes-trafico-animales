-- Se elimina la tabla puntosnoaccidentes si existiera
DROP TABLE IF EXISTS public.puntosnoaccidentes;

-- Se crea la tabla puntosnoaccidentes atendiendo a las características de cada campo
CREATE TABLE public.puntosnoaccidentes (
	id serial4 NOT NULL,
	geom public.geometry NULL,
	lon numeric NULL,
	lat numeric NULL
);