-- Se elimina la tabla meteohis si existiera
DROP TABLE IF EXISTS meteohis;

-- Se crea la tabla meteohis definiendo los campos
CREATE TABLE public.meteohis (
	fecha date NULL,
	indicativo varchar NULL,
	nombre varchar NULL,
	provincia varchar NULL,
	altitud numeric NULL,
	tmedia numeric NULL,
	precipitacion numeric NULL,
	tmin numeric NULL,
	horatmin varchar NULL,
	tmax numeric NULL,
	horatmax varchar NULL,
	dir varchar NULL,
	velmedia varchar NULL,
	racha varchar NULL,
	horaracha varchar NULL,
	sol numeric NULL,
	presmax varchar NULL,
	horapresmax varchar NULL,
	presmin varchar NULL,
	horapresmin varchar NULL
);