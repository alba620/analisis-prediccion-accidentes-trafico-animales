-- creacion del mapa forestal sobre el buffer de 500 a lo ancho de carreteras
create table mapa_forestal_carreteras
as
with nomcarr as
(
	select distinct ddcar_carr nom from carreteras c
	order by ddcar_carr
	limit 2
),carr as
(
	select ddcar_carr , geom_4326 , ddcar_codi , ddtram_cod , st_buffer(geom_4326::geography,500) buff -- buffer de 500 metros a cada lado de la carretera
	    , st_transform(  
	    st_envelope(  
	        st_buffer(  
	        	geom
	        ,1000
	            )  
	    ),4326   
	) as bbox  
	from carreteras c , nomcarr
	where ddcar_carr  = nomcarr.nom
	order by ddcar_carr 
), mf_intersectado as 
(
select mf.id, mf.geom , carr.bbox, carr.geom_4326, carr.buff
from mapa_forestal mf , carr
where st_intersects(mf.geom, carr.bbox)
)
select id, geom, buff, st_intersection(ST_MakeValid(geom),buff) buffinal
from mf_intersectado
where buff is not null
and st_astext(st_intersection(ST_MakeValid(geom),buff)) != 'POLYGON EMPTY'