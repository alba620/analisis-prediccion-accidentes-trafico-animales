-- Se generan las fechas con días aleatorios para los registros extraídos de los accidentes con víctimas teniendo en cuenta el campo de año y mes (y los días de cada mes)
update accidentes_no 
set fecha_accidente = 
	(CONCAT(anyo, '-', mes_1f, '-31 23:59:59')::timestamp - random() * INTERVAL '31 days')::date
where id_num > 73875
and nombre_mes = 'Enero'
or  nombre_mes = 'Marzo'
or  nombre_mes = 'Mayo'
or  nombre_mes = 'Julio'
or  nombre_mes = 'Agosto'
or  nombre_mes = 'Octubre'
or  nombre_mes = 'Diciembre'

update accidentes_no 
set fecha_accidente =  
	(CONCAT(anyo, '-', mes_1f, '-30 23:50:59')::timestamp - random() * INTERVAL '30 days')::date
where id_num > 73875
and nombre_mes = 'Abril'
or  nombre_mes = 'Junio'
or  nombre_mes = 'Septiembre'
or  nombre_mes = 'Noviembre'

update accidentes_no 
set fecha_accidente =  
	(CONCAT(anyo, '-', mes_1f, '-28 23:50:59')::timestamp - random() * INTERVAL '28 days')::date
where id_num > 73875
and nombre_mes = 'Febrero'


-- Se generan los minutos de forma aleatoria para los registros extraídos de los accidentes con víctimas
update accidentes_no 
set hora_accidente =
	CONCAT(hora_accidente, ':', LPAD(floor(random() * (59-0+1) + 0)::text, 2, '0'))::time
where id_num > 73875


-- Se generan las fecha y hora de forma aleatoria para los registros generados aleatoriamente
update accidentes_no 
set fecha_accidente =
	(timestamp '2021-12-31 23:59:59' - random() * INTERVAL '6 years')::date,
set hora_accidente =
	(timestamp '2021-12-31 23:59:59' - random() * INTERVAL '6 years')::time  
where id_num <= 73875