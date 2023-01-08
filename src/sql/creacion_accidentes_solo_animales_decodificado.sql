-- public.accidentes_solo_animales_decodificado definition

-- Se elimina la tabla accidentes_solo_animales_decodificado si existiera

DROP TABLE IF EXISTS public.accidentes_solo_animales_decodificado;

-- Se crea la tabla accidentes_solo_animales_decodificado decodificando los cambios necesarios
CREATE TABLE accidentes_solo_animales_decodificado
AS
SELECT 
	id_num,
	ind_accda,
	aia.etiqueta nombre_ind_accd,
	ind_acciv,
	aia2.etiqueta nombre_ind_acciv,
	total_mu30df,
	total_hg30df,
	total_hl30df,
	fecha_accidente,
	hora_accidente,
	mes_1f,
	am.etiqueta nombre_mes,
	anyo,
	ccaa_1f,
	ac.etiqueta nombre_ccaa,
	provincia_1f,
	acp.etiqueta nombre_provincia,	
	cod_municipio,
	acmi.etiqueta nombre_municipio,	
	carretera,
	km,
	sentido_1f,
	as2.etiqueta nombre_sentido,
	tipo_via_3f,
	atvf.etiqueta nombre_tipo_via,
	titularidad_via_2f,
	atv.etiqueta nombre_titularidad_via,
	tipo_animal_1f,
	ata.etiqueta nombre_tipo_animal_1f,
	ata.taxonkey taxonkey,
	tipo_animal_2f,
	ata2.etiqueta nombre_tipo_animal_2f
FROM public.accidentes_solo_animales asa
left join
	aux_mes am on am.valor = asa.mes_1f 
left join
	aux_cod_provincia acp on acp.valor = asa.provincia_1f 
left join
	aux_cod_municipios_ine acmi on acmi.valor = asa.cod_municipio
left join 
	aux_sentido as2 on as2.valor = asa.sentido_1f
left join 
	aux_titularidad_via atv on atv.valor = asa.titularidad_via_2f
left join 
	aux_ind_accda aia on aia.valor = asa.ind_accda
left join 
	aux_ind_acciv aia2 on aia2.valor = asa.ind_acciv 
left join 
	aux_ccaa ac on ac.valor = asa.ccaa_1f 
left join 
	aux_tipo_via_3f atvf on atvf.valor = asa.tipo_via_3f
left join 
	aux_tipo_animal_1 ata on ata.valor = asa.tipo_animal_1f
left join 
	aux_tipo_animal_2 ata2 on ata2.valor = asa.tipo_animal_2f