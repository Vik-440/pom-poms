INSERT INTO directory_of_order (id_order, data_order,data_plane_order, id_client, doc_add_order,
Data_send_order, fulfilled_order, discont_order, id_recipient, sum_payment)
VALUES
	(537,	'2022-02-17',	'2022-04-15',	11,	FALSE,	'2022-04-07', FALSE, 0, 11, 780),
	(538,	'2022-02-18',	'2022-03-23',	12,	FALSE,	'2022-04-08', FALSE, 0, 12, 840),
	(539,	'2022-02-19',	'2022-03-23',	13,	FALSE,	'2022-04-09', FALSE, 0, 13, 6930),
	(540, 	'2022-02-22',	'2022-03-24',	14,	TRUE,	'2022-04-10', FALSE, 0, 14, 3080),
	(541,	'2022-02-23',	'2022-03-25',	15,	FALSE,	'2022-04-11', FALSE, 0, 15, 1950);	


INSERT INTO directory_of_client (id_client, phone_client, second_name_client, first_name_client,
surname_client, sity, np_number, team, coach)
VALUES
	(11, 381111111111, 'Козинець', 'Олена', 'Василівна', 'Донецьк', 111, 'Соколи', 'Козинець'),
	(12, 382222222222, 'Коробенко','Ольга',	'Вячеславівна',	'Київ', 112, 'Переможці','Коробенко' ),
    (13, 383333333333, 'Гаврушко', 'Ліля', 'Остапівна',	'Львів', 113, 'Ангели', 'Тимошенко'),
    (14, 384444444444, 'Тимошенко',	'Світлана',	'Петрівна',	'Буча',	114, 'Матроси', 'Тимошенко'),
    (15, 385555555555, 'Блажко', 'Наталія', 'Андріївна', 'Тернопіль', 115, 'Красуні','Блажко');

INSERT INTO directory_of_team (id_team, name_team, id_sity, id_client)
VALUES
    (31, 'Motodor', 21,	41),
    (32, 'Angels', 22, 42),
    (33, 'Unior', 23, 43),
    (34, 'Nika', 23, 44),
    (35, 'Red_Dac',	24,	45);

INSERT INTO directory_of_model (id_model, kod_model, kolor_model, price_model, id_color_1, id_color_part_1,
id_color_2, id_color_part_2)
VALUES
    (51, '190-B21',	'Бірюзовий', '390',	69,	100, 0, 0),		
    (52, '170-70', 'Червоний', 280,	62,	100, 0, 0),
    (53, '190-B09',	'Синій', 390, 68, 100, 0, 0),		
    (54, '190-73', 'Бірюзовий', 300, 63, 100, 0, 0),		
    (55, '230-7780', 'Білий + Синій', 330, 64, 50, 66, 50),
    (56, '272-4578-70/30', 'Срібний_гол + Рожевий',	280, 61, 70, 65, 30),
    (57, '190-B05',	'Малиновий', 390, 67, 100, 0, 0);

INSERT INTO directory_of_group (id_group_model, id_model, id_order, quantity_pars_model, phase_1_model,
phase_2_model, phase_3_model)
VALUES
    (71, 51, 537, 2, TRUE, FALSE, FALSE),
    (72, 52, 538, 3, FALSE, FALSE, FALSE),
    (73, 53, 539, 5, TRUE, FALSE, FALSE),
    (74, 54, 539, 7, TRUE, FALSE, FALSE),
    (75, 55, 539, 9, TRUE, TRUE, TRUE),
    (76, 56, 540, 11, TRUE, TRUE, FALSE),
    (77, 57, 541, 5, TRUE, FALSE, FALSE);

INSERT INTO directory_of_payment (id_payment, id_order, payment, metod_payment, data_payment)
VALUES
    (81, 540, 1080, 'cash', '2022-02-19'),
    (82, 541, 1950, 'iban', '2022-02-20'),
    (83, 537, 300, 'iban', '2022-02-21'),
    (84, 540, 2000, 'iban', '2022-02-24'),
    (85, 539, 2000, 'iban', '2022-02-25');

INSERT INTO directory_of_sity (id_sity, sity)
VALUES 
    (21, 'Кам’янське'),
    (22, 'Львів'),
    (23, 'Київ'),
    (24, 'Ровно'),
    (25, 'Київ=самовивіз');
		
INSERT INTO directory_of_color (id_color, name_color, kod_color, width_color, thickness_color,
bab_quantity_color, bab_weight_color, weight_color, manufacturer_color, reserve_color, weight_10m_color)
VALUES
    (61, '45-Срібний_гол', 45, 23, 30, 6, 130, 3045, 'Rovno',0 , 12.67),
    (62, '70-Червоний', 70, 23, 36, 4, 130, 1256, 'Rovno',0 , 11.8),
    (63, '73-Бірюзовий', 73, 22, 36, 2, 130, 1672, 'Rovno',0 , 10.29),
    (64, '77-Білий', 77, 25, 36, 11, 130, 14034, 'Rovno',0 , 11.15),
    (65, '78-Рожевий', 78, 23, 30, 3, 130, 2005, 'Rovno',0 , 9.64),
    (66, '80-Синій', 80, 23, 36, 2, 130, 1893, 'Rovno',0 , 12.78),
    (67, 'B05-Малиновий', 'B05', 660, 35, 4, 40, 2640, 'Itak',0 ,0), 
    (68, 'B09-Синій', 'B09', 660, 35, 0, 0, 0, 'Itak',0 ,0), 
    (69, 'B21-Бірюзовий', 'B21', 660, 35, 1, 10, 660, 'Itak',0 ,0);

INSERT INTO directory_of_outlay (id_outlay, data_outlay, id_outlay_class, money_outlay, quantity_outlay,
type_pc_outlay)
VALUES
    (101, '2022-02-01', 91, 1303, 1, 'платіж'),
    (102, '2022-02-03', 93, 102, 2, 'шт.'),
    (103, '2022-02-10', 94, 45, 1, 'шт.'),
    (104, '2022-02-17', 96, 99, 1, 'місяць'),
    (105, '2022-02-24', 92, 2925, 15, 'кг');

INSERT INTO directory_of_outlay_class (id_outlay_class, outlay_class)
VALUES
    (91, 'податок'),
    (92, 'матеріали основні'),
    (93, 'матеріали домоміжні'),
    (94, 'інструмент'),
    (95, 'оплта роботи'),
    (96, 'реклама');