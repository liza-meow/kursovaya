insert postavka(id_service, service_price, col_vo, date_zak, date_post, confirm)
values("$id", "$price", "$col_vo", current_date(), DATE_ADD(current_date(), INTERVAL "$date" DAY), '0')