select S_id, name, cost from
service join tovar on tovar_id = id_tovar
where id_postovchik = "$id"
