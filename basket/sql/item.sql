select FIO, name, cost, spec_cost, spec_col_vo from postavchik join (select S_id, name, cost, spec_cost, spec_col_vo, id_postovchik from
service join tovar on tovar_id = id_tovar
where S_id = "$id") as nn on id_p = id_postovchik