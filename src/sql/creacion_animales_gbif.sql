-- Se elimina la tabla animales_gbif si existiera

DROP TABLE IF EXISTS animales_gbif ;

-- Se crea la tabla animales_gbif definiendo los campos

CREATE TABLE public.animales_gbif (
	gbifid varchar(10) NULL,
	datasetkey varchar(40) NULL,
	occurrenceid varchar(100) NULL,
	kingdom varchar(10) NULL,
	phylum varchar(10) NULL,
	"class" varchar(10) NULL,
	"order" varchar(15) NULL,
	"family" varchar(15) NULL,
	genus varchar(20) NULL,
	species varchar(30) NULL,
	infraspecificepithet varchar(15) NULL,
	taxonrank varchar(15) NULL,
	scientificname varchar(70) NULL,
	verbatimscientificname varchar(70) NULL,
	verbatimscientificnameauthorship varchar(20) NULL,
	countrycode varchar(2) NULL,
	locality varchar(1000) NULL,
	stateprovince varchar(30) NULL,
	occurrencestatus varchar(7) NULL,
	individualcount varchar(10) NULL,
	publishingorgkey varchar(40) NULL,
	decimallatitude varchar(50) NULL,
	decimallongitude varchar(10) NULL,
	coordinateuncertaintyinmeters varchar(20) NULL,
	coordinateprecision varchar(25) NULL,
	elevation varchar(10) NULL,
	elevationaccuracy varchar(10) NULL,
	"depth" varchar(10) NULL,
	depthaccuracy varchar(10) NULL,
	eventdate varchar(25) NULL,
	"day" varchar(25) NULL,
	"month" varchar(2) NULL,
	"year" varchar(4) NULL,
	taxonkey varchar(10) NULL,
	specieskey varchar(10) NULL,
	basisofrecord varchar(20) NULL,
	institutioncode varchar(70) NULL,
	collectioncode varchar(35) NULL,
	catalognumber varchar(40) NULL,
	recordnumber varchar(25) NULL,
	identifiedby varchar(200) NULL,
	dateidentified varchar(50) NULL,
	license varchar(30) NULL,
	rightsholder varchar(400) NULL,
	recordedby varchar(200) NULL,
	typestatus varchar(60) NULL,
	establishmentmeans varchar(40) NULL,
	lastinterpreted varchar(40) NULL,
	mediatype varchar(300) NULL,
	issue varchar(200) NULL,
	geom public.geometry NULL,
	buff public.geometry NULL
);

-- Se crea el índice espacial para el campo buff
CREATE INDEX gist_animales_gbif ON public.animales_gbif USING gist (buff);
