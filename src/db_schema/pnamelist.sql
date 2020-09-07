-- create plant namelist "pnamelist"
DROP TABLE IF EXISTS dao_pnamelist_pg;
CREATE TABLE dao_pnamelist_pg (
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
DROP TABLE IF EXISTS dao_pnamelist_pg_synonym;
CREATE TABLE dao_pnamelist_pg_synonym (
  id integer,
  accepted_namecode varchar,
  namecode varchar,
  fullname varchar,
  cname varchar,
  synonyms varchar
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
DROP TABLE IF EXISTS dao_twredlist2017;
CREATE TABLE dao_twredlist2017 (
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
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (0, '苔蘚地衣類植物 Mosses and Lichens');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (1, '石松類植物 Lycophytes');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (2, '蕨類植物 Monilophytes');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (3, '裸子植物 Gymnosperms');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (4, '單子葉植物 Monocots');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (5, '真雙子葉植物姊妹群 Sister groups of Eudicots');
INSERT INTO dao_plant_type (plant_type, pt_name) VALUES (6, '真雙子葉植物 Eudicots');
