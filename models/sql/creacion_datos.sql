
-- Se crea el campo target con 0 en los registros sin accidentes con animales y 1 para los que sí
ALTER TABLE public.accidentes_no ADD predict int NULL;
UPDATE accidentes_no 
SET target = 0;

ALTER TABLE public.accidentes_si ADD predict int NULL;
UPDATE accidentes_si 
SET target = 1;

-- Se elimina la tabla datos si existiera
DROP TABLE IF EXISTS public.datos;

-- Se crea la tabla datos, resultado de la unión de accidentes_si y accidentes_no
CREATE TABLE public.datos AS
(select * from accidentes_si
union
select * from accidentes_no);

-- Se crea la columna geohash6
ALTER TABLE public.datos ADD geohash6 varchar NULL;
COMMENT ON COLUMN public.datos.geohash6 IS 'geohash from geom';

-- Se actualiza la columna geohash6 con este valor a partir de la columna geom
update datos set geohash6 = st_geohash(geom,6)

-- Se crea la columna geohash5
ALTER TABLE public.datos ADD geohash5 varchar NULL;
COMMENT ON COLUMN public.datos.geohash6 IS 'geohash from geom';

-- Se actualiza la columna geohash5 con este valor a partir de la columna geom
update datos set geohash5 = st_geohash(geom,5)

-- Se crea la columna geohash7
ALTER TABLE public.datos ADD geohash7 varchar NULL;
COMMENT ON COLUMN public.datos.geohash7 IS 'geohash from geom';

-- Se actualiza la columna geohash7 con este valor a partir de la columna geom
update datos set geohash7 = st_geohash(geom,7)
