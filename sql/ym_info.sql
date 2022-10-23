SELECT FIO, city, telephone FROM postavchik join
(select * from postavka join service on id_service = S_id) as nn on id_p = id_postovchik
where month(date_zak) = "$month" and year(date_zak) = "$year"
group by id_p
