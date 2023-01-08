-- Se crean los campos maxspeed y geom_4326
ALTER TABLE public.carreteras ADD maxspeed integer NULL;
ALTER TABLE public.carreteras ADD geom_4326 public.geometry NULL;
update carreteras set geom_4326 = st_transform(geom,4326);

-- Se crea el índice espacial
CREATE INDEX gist_carreteras ON public.carreteras USING gist (geom_4326);

-- Actualizacion de la tabla de carreteras con el valor de maxspeed_infered de la tabla roads

UPDATE carreteras 
SET maxspeed=subquery.maxspeed
FROM (
				with area_carreteras as
				(
					select   
						ddcar_carr
						, st_transform(  
							st_envelope(  
								st_buffer(  
									st_transform(geom_4326 ,25830)
								,1000
									)  
							),4326   
						) as bbox  
						,st_transform(st_linemerge(geom_4326),25830) geom_25830
					from carreteras
				), res as
				(
					select 
						c.ddcar_carr
						,r.ref
						, r.maxspeed_infered 
					from roads_tfm r, area_carreteras as c
					where st_intersects(r.geom  ,c.bbox)
					and st_intersects(
									st_buffer( st_transform(r.geom,25830),100)
									,c.geom_25830
									)
					and st_astext(st_intersection(r.geom, st_transform(c.geom_25830,4326))) != 'LINESTRING EMPTY'
				)
				select ddcar_carr , max(maxspeed_infered) maxspeed
				from res
				group by ddcar_carr 

) AS subquery
WHERE carreteras.ddcar_carr=subquery.ddcar_carr;