-- Se elimina la tabla accidentes_solo_animales si existiera
DROP TABLE IF EXISTS accidentes_solo_animales;

-- Se crea la tabla accidentes_solo_animales atendiendo a las características de cada campo
CREATE TABLE public.accidentes_solo_animales (
	id_num int8 NULL,
	ind_accda int4 NULL,
	ind_acciv int4 NULL,
	total_mu30df int4 NULL,
	total_hg30df int4 NULL,
	total_hl30df int4 NULL,
	fecha_accidente date NULL,
	hora_accidente varchar NULL,
	mes_1f int4 NULL,
	anyo int4 NULL,
	ccaa_1f int4 NULL,
	provincia_1f int4 NULL,
	cod_municipio int4 NULL,
	carretera varchar(50) NULL,
	km float4 NULL,
	sentido_1f int4 NULL,
	tipo_via_3f int4 NULL,
	titularidad_via_2f int4 NULL,
	tipo_animal_1f int4 NULL,
	tipo_animal_2f int4 NULL
);