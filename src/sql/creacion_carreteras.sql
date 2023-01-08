-- Se elimina la tabla carreteras si existiera
DROP TABLE IF EXISTS carreteras;

-- Se crea la tabla carreteras definiendo los campos
CREATE TABLE public.carreteras (
	id int4 NOT NULL DEFAULT nextval('carreteras_dgt_id_seq'::regclass),
	geom public.geometry(multilinestringm, 3857) NULL,
	objectid int8 NULL,
	ddtram_cod float8 NULL,
	ddcar_codi float8 NULL,
	ddcar_deno varchar(254) NULL,
	ddtram_den varchar(254) NULL,
	ddtram_tip varchar(254) NULL,
	ddtram_tit varchar(254) NULL,
	ddtram_t_1 varchar(254) NULL,
	ddtram_lon float8 NULL,
	pk_ini float8 NULL,
	pk_fin float8 NULL,
	idtipovian varchar(254) NULL,
	ddprov_pro varchar(50) NULL,
	ddcom_comu varchar(50) NULL,
	color int4 NULL,
	ddcar_carr varchar(50) NULL,
	ddtvia_ord int4 NULL,
	pkinigis float8 NULL,
	pkfingis float8 NULL,
	shape_leng float8 NULL,
	CONSTRAINT carreteras_dgt_pkey PRIMARY KEY (id)
);