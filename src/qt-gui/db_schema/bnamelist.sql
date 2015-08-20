-- create bird namelist "bnamelist"
DROP TABLE IF EXISTS dao_bnamelist;
CREATE TABLE dao_bnamelist (
      id integer primary key,
      family varchar,
      family_zh varchar,
      zh_name varchar,
      name varchar,
      endemic integer,
      consv_status varchar,
      source varchar
);

