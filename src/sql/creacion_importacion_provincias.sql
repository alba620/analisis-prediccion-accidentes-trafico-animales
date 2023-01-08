CREATE TABLE public.provincias (
	id int8 NOT NULL,
	"name" varchar(255) NULL,
	name_ine varchar(255) NULL,
	ccaa_id int8 NOT NULL,
	CONSTRAINT provincias_pkey PRIMARY KEY (id)
);

INSERT INTO public.provincias (id,"name",name_ine,ccaa_id) VALUES
	 (2,'ALBACETE','Albacete',8),
	 (3,'ALICANTE','Alicante/Alacant',10),
	 (4,'ALMERIA','Almería',1),
	 (5,'AVILA','Ávila',7),
	 (6,'BADAJOZ','Badajoz',11),
	 (7,'BALEARS, ILLES','Balears, Illes',4),
	 (8,'BARCELONA','Barcelona',9),
	 (9,'BURGOS','Burgos',7),
	 (10,'CACERES','Cáceres',11),
	 (11,'CADIZ','Cádiz',1);
INSERT INTO public.provincias (id,"name",name_ine,ccaa_id) VALUES
	 (12,'CASTELLON','Castellón/Castelló',10),
	 (13,'CIUDAD REAL','Ciudad Real',8),
	 (14,'CORDOBA','Córdoba',1),
	 (15,'A CORUÑA','Coruña, A',12),
	 (16,'CUENCA','Cuenca',8),
	 (17,'GIRONA','Girona',9),
	 (18,'GRANADA','Granada',1),
	 (19,'GUADALAJARA','Guadalajara',8),
	 (20,'GIPUZKOA','Gipuzkoa',16),
	 (21,'HUELVA','Huelva',1);
INSERT INTO public.provincias (id,"name",name_ine,ccaa_id) VALUES
	 (22,'HUESCA','Huesca',2),
	 (23,'JAEN','Jaén',1),
	 (24,'LEON','León',7),
	 (25,'LLEIDA','Lleida',9),
	 (26,'LA RIOJA','Rioja, La',17),
	 (27,'LUGO','Lugo',12),
	 (28,'MADRID','Madrid',13),
	 (29,'MALAGA','Málaga',1),
	 (30,'MURCIA','Murcia',14),
	 (31,'NAVARRA','Navarra',15);
INSERT INTO public.provincias (id,"name",name_ine,ccaa_id) VALUES
	 (32,'OURENSE','Ourense',12),
	 (33,'ASTURIAS','Asturias',3),
	 (34,'PALENCIA','Palencia',7),
	 (35,'LAS PALMAS','Palmas, Las',5),
	 (36,'PONTEVEDRA','Pontevedra',12),
	 (37,'SALAMANCA','Salamanca',7),
	 (38,'SANTA CRUZ DE TENERIFE','Santa Cruz de Tenerife',5),
	 (39,'CANTABRIA','Cantabria',6),
	 (40,'SEGOVIA','Segovia',7),
	 (41,'SEVILLA','Sevilla',1);
INSERT INTO public.provincias (id,"name",name_ine,ccaa_id) VALUES
	 (42,'SORIA','Soria',7),
	 (43,'TARRAGONA','Tarragona',9),
	 (44,'TERUEL','Teruel',2),
	 (45,'TOLEDO','Toledo',8),
	 (46,'VALENCIA','Valencia/València',10),
	 (47,'VALLADOLID','Valladolid',7),
	 (48,'BIZKAIA','Bizkaia',16),
	 (49,'ZAMORA','Zamora',7),
	 (50,'ZARAGOZA','Zaragoza',2),
	 (51,'CEUTA','Ceuta',18);
INSERT INTO public.provincias (id,"name",name_ine,ccaa_id) VALUES
	 (52,'MELILLA','Melilla',19),
	 (1,'ALAVA','Alava',16);