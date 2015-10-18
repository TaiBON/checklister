-- create bird namelist "bnamelist"
DROP TABLE IF EXISTS dao_bnamelist;
CREATE TABLE dao_bnamelist (
      id integer primary key,
      family varchar,
      family_cname varchar,
      cname varchar,
      name varchar,
      endemic integer,
      consv_status varchar,
      source varchar
);

