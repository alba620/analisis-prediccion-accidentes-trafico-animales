-- Se elimina la tabla accidentes_animales_final si existiera
DROP TABLE IF EXISTS accidentes_animales_final;

-- Se crea la tabla accidentes_animales_final que es una copia de accidentes_solo_animales_decodificado para trabajar (Updated Rows	165452)
create table accidentes_animales_final
as 
select *
from accidentes_solo_animales_decodificado;

-- Se crea el índice espacial
CREATE INDEX gist_accidentes_animales_final ON public.accidentes_animales_final USING gist (geom);

-- Se crean las nuevas columnas para poblarlas después
ALTER TABLE public.accidentes_animales_final ADD longitud float NULL;
ALTER TABLE public.accidentes_animales_final ADD latitud float NULL;
ALTER TABLE public.accidentes_animales_final ADD geom geometry NULL;
ALTER TABLE public.accidentes_animales_final ADD dia_semana int NULL;
ALTER TABLE public.accidentes_animales_final ADD nombre_dia_semana varchar NULL;
ALTER TABLE public.accidentes_animales_final ADD tipo_dia varchar NULL;
ALTER TABLE public.accidentes_animales_final ADD parte_dia varchar NULL;
ALTER TABLE public.accidentes_animales_final ADD luna integer NULL;
ALTER TABLE public.accidentes_animales_final ADD prec float NULL;
ALTER TABLE public.accidentes_animales_final ADD tmed float8 NULL;
ALTER TABLE public.accidentes_animales_final ADD tmin float NULL;
ALTER TABLE public.accidentes_animales_final ADD tmax float NULL;
ALTER TABLE public.accidentes_animales_final ADD sol float NULL;
ALTER TABLE public.accidentes_animales_final ADD uso_suelo varchar NULL;
ALTER TABLE public.accidentes_animales_final ADD altitud float NULL;
ALTER TABLE public.accidentes_animales_final ADD pendiente float NULL;
ALTER TABLE public.accidentes_animales_final ADD imd_total float NULL;
ALTER TABLE public.accidentes_animales_final ADD maxspeed integer NULL;