CREATE TABLE iridium (
id INT(32) NOT NULL auto_increment,
in_rate INT(10),
in_rate_avg INT(10),
queue_len INT(10),
queue_len_max INT(10),
out_rate INT(10),
ok_ratio INT(10),
ok_rate INT(10),
ok_ratio_total INT(10),
ok_count_total INT(32),
ok_rate_avg INT(10),
drop_count_total INT(10),
ts VARCHAR(50)
primary KEY (id));