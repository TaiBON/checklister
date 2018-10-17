
CREATE OR REPLACE VIEW nomenclature.taicol_view AS
 SELECT n.name_code id,
	n.iconic_taxon,
	n.iconic_taxon_vname,
	n.subhier_id,
    n.subhier,
	n.subhier_vname,
    n.family,
    n.family_c AS family_vname,
    n.common_name AS vernacular_name,
    n.name,
    n."scientificName" AS fullname,
    n.is_endemic AS endemic,
    n.iucn_category,
	n.conserv_status,
    n.native
   FROM nomenclature.taicol_raw n
  ORDER BY n.iconic_taxon, n.subhier_id, n.family, n.name;
