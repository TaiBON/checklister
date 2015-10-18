create or replace view nomenclature.jp_ylist_view as (
    select  
        j.family,
        j.family_wamei family_cname,
        j.wamei cname,
        j.name,
        j.fullname,
        j.plant_type,
        j.endemic_int endemic,
        i.category iucn_category,
        ecoinfo source from jp_ylist j 
    left outer join jp_iucn_redlist i on j.name=i.name order by 
    plant_type,family,name);
