SELECT FIO, city, telephone FROM postavchik join
(select * from postavka join service on id_service = S_id) as nn on id_p = id_postovchik
where DATEDIFF(CURDATE(), date_zak) <= "$days"
group by id_p