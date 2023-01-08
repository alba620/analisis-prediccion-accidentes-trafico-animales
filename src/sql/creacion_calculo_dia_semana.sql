-- Se actualiza el día de la semana en númerico
update accidentes_animales_final  
set dia_semana = extract(dow from fecha_accidente::timestamp);

-- Se reemplazan los 0 de los domingos por 7
update accidentes_animales_final 
set dia_semana = 7
where dia_semana = 0;

-- Mediante la tabla auxiliar 'aux_dia_semana', se imputa el nombre de cada día de la semana según su número
update accidentes_animales_final 
set nombre_dia_semana = subquery.etiqueta
from 
(
select aaf.id_num , aaf.dia_semana , ads.etiqueta 
from accidentes_animales_final aaf 
inner join aux_dia_semana ads on ads.valor = aaf.dia_semana 
) as subquery
where accidentes_animales_final.id_num = subquery.id_num
