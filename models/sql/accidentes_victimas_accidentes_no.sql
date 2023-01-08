-- Se insertan en accidentes_no 13869 registros de 2016
INSERT INTO public.accidentes_no
(id_num, total_mu30df, total_hg30df, total_hl30df, hora_accidente, mes_1f, nombre_mes, anyo, provincia_1f, nombre_provincia, cod_municipio, nombre_municipio, carretera, km, sentido_1f, nombre_sentido, titularidad_via_2f, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana)

SELECT 73875 + row_number() over(), total_mu30df, total_hg30df, total_hl30df, hora, mes, nombre_mes, anyo, cod_provincia, nombre_provincia, cod_municipio, nombre_codigo_municipio, carretera, km::REAL, sentido_1f, nombre_sentido, titularidad_via, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana
FROM public.accidentes_decodificado
where geom is not null
and nombre_tipo_accidente != 'Atropello a animales'
and anyo = 2016
limit 13869

-- Se insertan en accidentes_no 13870 registros de 2017 con el id_num siguiente al último
INSERT INTO public.accidentes_no
(id_num, total_mu30df, total_hg30df, total_hl30df, hora_accidente, mes_1f, nombre_mes, anyo, provincia_1f, nombre_provincia, cod_municipio, nombre_municipio, carretera, km, sentido_1f, nombre_sentido, titularidad_via_2f, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana)

SELECT 87744 + row_number() over(), total_mu30df, total_hg30df, total_hl30df, hora, mes, nombre_mes, anyo, cod_provincia, nombre_provincia, cod_municipio, nombre_codigo_municipio, carretera, km::REAL, sentido_1f, nombre_sentido, titularidad_via, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana
FROM public.accidentes_decodificado
where geom is not null
and nombre_tipo_accidente != 'Atropello a animales'
and anyo = 2017
limit 13870

-- Se insertan en accidentes_no 13870 registros de 2018 con el id_num siguiente al último
INSERT INTO public.accidentes_no
(id_num, total_mu30df, total_hg30df, total_hl30df, hora_accidente, mes_1f, nombre_mes, anyo, provincia_1f, nombre_provincia, cod_municipio, nombre_municipio, carretera, km, sentido_1f, nombre_sentido, titularidad_via_2f, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana)

SELECT 101614 + row_number() over(), total_mu30df, total_hg30df, total_hl30df, hora, mes, nombre_mes, anyo, cod_provincia, nombre_provincia, cod_municipio, nombre_codigo_municipio, carretera, km::REAL, sentido_1f, nombre_sentido, titularidad_via, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana
FROM public.accidentes_decodificado
where geom is not null
and nombre_tipo_accidente != 'Atropello a animales'
and anyo = 2018
limit 13870

-- Se insertan en accidentes_no 13870 registros de 2019 con el id_num siguiente al último
INSERT INTO public.accidentes_no
(id_num, total_mu30df, total_hg30df, total_hl30df, hora_accidente, mes_1f, nombre_mes, anyo, provincia_1f, nombre_provincia, cod_municipio, nombre_municipio, carretera, km, sentido_1f, nombre_sentido, titularidad_via_2f, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana)

SELECT 115484 + row_number() over(), total_mu30df, total_hg30df, total_hl30df, hora, mes, nombre_mes, anyo, cod_provincia, nombre_provincia, cod_municipio, nombre_codigo_municipio, carretera, km::REAL, sentido_1f, nombre_sentido, titularidad_via, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana
FROM public.accidentes_decodificado
where geom is not null
and nombre_tipo_accidente != 'Atropello a animales'
and anyo = 2019
limit 13870

-- Se insertan en accidentes_no 13870 registros de 2020 con el id_num siguiente al último
INSERT INTO public.accidentes_no
(id_num, total_mu30df, total_hg30df, total_hl30df, hora_accidente, mes_1f, nombre_mes, anyo, provincia_1f, nombre_provincia, cod_municipio, nombre_municipio, carretera, km, sentido_1f, nombre_sentido, titularidad_via_2f, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana)

SELECT 129354 + row_number() over(), total_mu30df, total_hg30df, total_hl30df, hora, mes, nombre_mes, anyo, cod_provincia, nombre_provincia, cod_municipio, nombre_codigo_municipio, carretera, km::REAL, sentido_1f, nombre_sentido, titularidad_via, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana
FROM public.accidentes_decodificado
where geom is not null
and nombre_tipo_accidente != 'Atropello a animales'
and anyo = 2020
limit 13870

-- Se insertan en accidentes_no 13870 registros de 2021 con el id_num siguiente al último
INSERT INTO public.accidentes_no
(id_num, total_mu30df, total_hg30df, total_hl30df, hora_accidente, mes_1f, nombre_mes, anyo, provincia_1f, nombre_provincia, cod_municipio, nombre_municipio, carretera, km, sentido_1f, nombre_sentido, titularidad_via_2f, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana)

SELECT 143224 + row_number() over(), total_mu30df, total_hg30df, total_hl30df, hora, mes, nombre_mes, anyo, cod_provincia, nombre_provincia, cod_municipio, nombre_codigo_municipio, carretera, km::REAL, sentido_1f, nombre_sentido, titularidad_via, nombre_titularidad_via, longitud, latitud, geom, dia_semana, nombre_dia_semana
FROM public.accidentes_decodificado
where geom is not null
and nombre_tipo_accidente != 'Atropello a animales'
and anyo = 2021
limit 13870