CREATE OR REPLACE VIEW nomenclature.twnamelist_view AS 
 SELECT 
    n.family_apg3,
    n.family_apg3_zh,
    n.zh_name[1] AS zh_name,
    n.name,
    n.fullname,
    n.plant_type,
    n.endemic,
    i.category,
    n.source
   FROM namelist n
     LEFT JOIN iucn_redlist i ON n.name::text = i.name::text
  ORDER BY n.plant_type, n.family_apg3, n.name;
