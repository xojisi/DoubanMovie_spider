create database if not exists `doubanmovie`;

grant usage on *.* to 'douban'@'localhost';
drop user 'douban'@'localhost';

create user 'douban'@'localhost' identified by '12306';
grant all privileges on `doubanmovie`.* to 'douban'@'localhost';

