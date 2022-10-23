select S_id, name, cost, spec_cost, spec_col_vo from
service join tovar on tovar_id = id_tovar
where S_id = "$id"
