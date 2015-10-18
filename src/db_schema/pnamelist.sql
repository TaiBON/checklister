-- create plant namelist "pnamelist"
DROP TABLE IF EXISTS dao_pnamelist_apg3;
CREATE TABLE dao_pnamelist_apg3 (
  id integer primary key,
  family varchar,
  family_cname varchar,
  cname varchar,
  name varchar,
  fullname varchar,
  plant_type integer,
  endemic integer,
  iucn_category varchar,
  source varchar
);
DROP TABLE IF EXISTS dao_pnamelist;
CREATE TABLE dao_pnamelist (
  id integer primary key,
  family varchar,
  family_cname varchar,
  cname varchar,
  name varchar,
  fullname varchar,
  plant_type integer,
  endemic integer,
  iucn_category varchar,
  source varchar
);
DROP TABLE IF EXISTS dao_jp_ylist;
CREATE TABLE dao_jp_ylist (
  id integer primary key,
  family varchar,
  family_cname varchar,
  cname varchar,
  name varchar,
  fullname varchar,
  plant_type integer,
  endemic integer,
  iucn_category varchar,
  source varchar
);


DROP TABLE IF EXISTS dao_plant_type;
CREATE TABLE dao_plant_type (
  plant_type integer,
  pt_name varchar
);
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (1, '苔蘚地衣類植物 Mosses and Lichens');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (1, '蕨類植物 Ferns and Lycophytes');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (2, '裸子植物 Gymnosperms');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (3, "雙子葉植物 'Dicotyledons'");
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (4, '單子葉植物 Monocotyledons'); 

