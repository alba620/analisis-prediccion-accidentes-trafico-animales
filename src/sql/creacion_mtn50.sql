-- Se elimina la tabla mtn50 si existiera
DROP TABLE IF EXISTS mtn50;

-- Se crea la tabla mtn50 definiendo los campos
CREATE TABLE public.mtn50 (
	id serial4 NOT NULL,
	geom public.geometry(multipolygon) NULL,
	mtn50_clas varchar(50) NULL,
	nombre_50 varchar(50) NULL,
	ccff50 varchar(50) NULL,
	CONSTRAINT mtn50_pkey PRIMARY KEY (id)
);
CREATE INDEX gist_mtn50 ON public.mtn50 USING gist (geom);