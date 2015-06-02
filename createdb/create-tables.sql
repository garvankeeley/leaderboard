CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;

CREATE TABLE TILE (
    tile_pk serial NOT NULL,
    country_fk int NOT NULL,
    CONSTRAINT tile_pk_constraint PRIMARY KEY(tile_pk)
);
SELECT AddGeometryColumn('tile', 'wkb_geometry', 3785, 'POLYGON', 2);

CREATE TABLE USERINFO (
    userinfo_pk bigserial  NOT NULL,
    name varchar(200) NOT NULL,
    email varchar(200) NOT NULL,
    bearer_token varchar(64),
    total_observations bigint,
    CONSTRAINT USERINFO_pk PRIMARY KEY (userinfo_pk)
);
ALTER TABLE userinfo ADD UNIQUE(name);

