-- Se elimina la tabla aemet_estaciones si existiera
DROP TABLE IF EXISTS aemet_estaciones;

-- Se crea la tabla aemet_estaciones definiendo los campos
CREATE TABLE public.aemet_estaciones (
	id serial4 NOT NULL,
	geom public.geometry(point, 4326) NULL,
	indicativo varchar(254) NULL,
	nombre varchar(254) NULL,
	provincia varchar(254) NULL,
	altitud float8 NULL,
	coord_x float8 NULL,
	coord_y float8 NULL,
	var_obsver varchar(254) NULL,
	datum varchar(254) NULL,
	tipo varchar(50) NULL,
	layer varchar(254) NULL,
	"path" varchar(254) NULL,
	CONSTRAINT aemet_estaciones_pkey PRIMARY KEY (id)
);