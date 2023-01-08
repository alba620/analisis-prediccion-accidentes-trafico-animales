-- Se actualizan los campos con el del día a partir de la fecha generada para los accidentes creados aleatoriamente
update accidentes_no
set dia_semana = extract(dow from fecha_accidente::timestamp)
where id_num <= 73875

-- Se reemplazan los 0 de los domingos por 7
update accidentes_no 
set dia_semana = 7
where dia_semana = 0
and id_num <= 73875

-- Se decodifica el valor numérico del día con la tabla auxiliar aux_dia_semana y clasifica el tipo de día del que se trata
update accidentes_no 
set 
	nombre_dia_semana = subquery.etiqueta,
	tipo_dia = subquery.tipo_dia
from 
(
select aaf.id_num , aaf.dia_semana , ads.etiqueta, ads.tipo_dia
from accidentes_no aaf 
inner join aux_dia_semana ads on ads.valor = aaf.dia_semana 
) as subquery
where accidentes_no.id_num = subquery.id_num

-- Se actualizan los campos con el número de mes y de año a partir de la fecha generada para los accidentes creados aleatoriamente
update accidentes_no 
set 
	mes_1f = date_part('month', fecha_accidente)::numeric,
	anyo = date_part('year', fecha_accidente)::numeric
where id_num <= 73875

-- Se decodifica el valor numérico del mes con la tabla auxiliar aux_mes
update accidentes_no 
set nombre_mes = sub.etiqueta
from 
(select valor, etiqueta  from aux_mes) as sub
where accidentes_no.id_num <= 73875
and accidentes_no.mes_1f = sub.valor