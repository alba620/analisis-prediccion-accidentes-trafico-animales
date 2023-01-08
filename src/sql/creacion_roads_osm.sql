-- Se elimina la tabla roads_tfm si existiera
DROP TABLE IF EXISTS roads_osm;

-- Se crea la tabla roads_osm definiendo los campos
CREATE TABLE public.roads_osm (
	osm_id varchar NOT NULL,
	geom public.geometry(multilinestring, 4326) NULL,
	code int4 NULL,
	fclass varchar(28) NULL,
	"name" varchar(100) NULL,
	"ref" varchar(20) NULL,
	oneway varchar(1) NULL,
	maxspeed int4 NULL,
	layer varchar(254) NULL,
	bridge varchar(1) NULL,
	tunnel varchar(1) NULL,
	id int8 NULL,
	"path" varchar(254) NULL,
	CONSTRAINT roads_osm_pkey PRIMARY KEY (osm_id)
);