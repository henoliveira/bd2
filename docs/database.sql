CREATE TABLE departments (
	id		int,
	title	varchar(50),
	PRIMARY KEY (id)
);

CREATE TABLE artwork_types (
	id		int,
	title	varchar(50),
	PRIMARY KEY (id)
);

CREATE TABLE categories (
	id		int,
	title	varchar(100),
	subtype	varchar(50),
	PRIMARY KEY (id)
);

CREATE TABLE artists (
	id				int,
	title			varchar(100),
	sort_title		varchar(100),
	is_artist		bool,
	birth_date		int,
	death_date		int,
	description		text,
	PRIMARY KEY (id)
);

CREATE TABLE artworks (
	id					int,
	id_artist			int,
	id_department		int,
	id_artwork_type		int,
	date_start			int,
	date_end			int,
	date_display		varchar(300),
	place_of_origin		varchar(300),
	title				text,
	medium_display		text,
	dimensions			text,
	api_link			varchar(300),
	PRIMARY KEY (id),
	FOREIGN KEY(id_artist) REFERENCES artists(id),
	FOREIGN KEY(id_department) REFERENCES departments(id),
	FOREIGN KEY(id_artwork_type) REFERENCES artwork_types(id)
);

CREATE TABLE artworks_categories (
	id			serial,
	id_artwork	int,
	id_category	int,
	PRIMARY KEY (id),
	FOREIGN KEY(id_category) REFERENCES categories(id),
	FOREIGN KEY(id_artwork) REFERENCES artworks(id)
);

CREATE TABLE exhibitions (
	id			serial,
	title		varchar(300),
	description	text,
	date_start	date,
	date_end	date,
	location	varchar(300),
	PRIMARY KEY (id)
);

CREATE TABLE artworks_exhibitions (
	id				serial,
	id_artwork		int,
	id_exhibition	int,
	PRIMARY KEY (id),
	FOREIGN KEY(id_artwork) REFERENCES artworks(id),
	FOREIGN KEY(id_exhibition) REFERENCES exhibitions(id)
);

CREATE OR REPLACE VIEW show_artists AS
SELECT
	a.id, b.title as artist, c.title as artwork_type,
	d.title as department, a.date_start, a.date_end,
	a.place_of_origin, a.dimensions, a.title, a.api_link
FROM artworks a
INNER JOIN artists b ON b.id = a.id_artist
INNER JOIN artwork_types c ON c.id = a.id_artwork_type
INNER JOIN departments d ON d.id = a.id_artwork_type;
	
CREATE ROLE	"Admin";
GRANT ALL ON ALL TABLES IN SCHEMA "public" TO "Admin";

CREATE ROLE "Manager";
GRANT SELECT, UPDATE, DELETE, INSERT
ON departments, artwork_types, categories, artists, artworks,
   artworks_categories, exhibitions, artworks_exhibitions
TO "Manager";

CREATE ROLE "ExhibitionOrganizer";
GRANT SELECT, UPDATE, DELETE, INSERT
ON exhibitions, artworks_exhibitions TO "ExhibitionOrganizer";

CREATE ROLE "User";
GRANT SELECT ON show_artists, exhibitions, show_artists TO "User";

--Tests
-- select * from show_artists where artwork_type = 'Painting'
-- select * from departments;
-- select * from artists;
-- select * from artworks;
-- select * from artworks_categories;

-- delete from artworks_categories;
-- delete from artworks;
-- delete from departments;
-- delete from artwork_types;
-- delete from categories;
-- delete from artists;