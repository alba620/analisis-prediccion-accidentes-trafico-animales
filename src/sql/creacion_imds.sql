-- Se elimina la tabla imds si existiera
DROP TABLE IF EXISTS imds;

-- Se crea la tabla imds definiendo los campos
CREATE TABLE public.imds (
	id serial4 NOT NULL,
	objectid bigint NULL,
	provincia varchar NULL,
	nombre varchar NULL,
	year int4 NULL,
	tipo_carretera varchar NULL,
	pk_inicio numeric NULL,
	pk_fin numeric NULL,
	longitud numeric NULL,
	vh_km_total int4 NULL,
	vh_km_ligeros int4 NULL,
	vh_km_pesados int4 NULL,
	imd_total int4 NULL,
	imd_ligeros int4 NULL,
	imd_pesados int4 NULL,
	geom geometry NULL,
	CONSTRAINT imds_pk PRIMARY KEY (id)
);