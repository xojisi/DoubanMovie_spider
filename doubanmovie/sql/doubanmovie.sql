USE doubanmovie;

DROP TABLE IF EXISTS `turns`;
CREATE TABLE `turns` (
    `id` INT PRIMARY KEY,
    `mark_time` TIMESTAMP NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
表: 热门电影(popularmovie)
字段:  编号(p_id),电影名(film_title),导演(director),主演(actor),制片国/地区(region),
      上映日期(release_date),类型(film_types),评分(grade),简介(intro),海报(poster),年份(yyyy)
*/
DROP TABLE IF EXISTS `popularmovie`;
CREATE TABLE popularmovie(
  id INT UNSIGNED,
  film_title VARCHAR(50) NOT NULL,
  director VARCHAR (20),
  actor VARCHAR(200),

  region VARCHAR(20),
  release_date VARCHAR(100),
  film_types VARCHAR(20),
  grade FLOAT(2,1),
  intro TEXT,
  poster VARCHAR(100),
  yyyy YEAR,
  turn INT NOT NULL,
  PRIMARY KEY (id,turn)
);

/*
表: 最新电影(newmovie)
字段:  编号(n_id),电影名(film_title),导演(director),主演(actor),制片国/地区(region),
      上映日期(release_date),类型(film_types),评分(grade),简介(intro),海报(poster),年份(yyyy)
*/
DROP TABLE IF EXISTS `newmovie`;
CREATE TABLE newmovie(
  id INT UNSIGNED,
  film_title VARCHAR(50) NOT NULL,
  director VARCHAR (20),
  actor VARCHAR(200),
  region VARCHAR(20),
  release_date VARCHAR(100),
  film_types VARCHAR(20),
  grade FLOAT(2,1),
  intro TEXT,
  poster VARCHAR(100),
  yyyy YEAR,
  turn INT NOT NULL,
  PRIMARY KEY (id,turn)
);


/*
表: 正在上映(nowplaying)
字段:  编号(np_id),电影名(film_title),导演(director),主演(actor),制片国/地区(region),
      上映日期(release_date),类型(film_types),评分(grade),简介(intro),海报(poster),年份(yyyy)
*/
DROP TABLE IF EXISTS `nowplaying`;
CREATE TABLE nowplaying(
  id INT UNSIGNED,
  film_title VARCHAR(50) NOT NULL,
  director VARCHAR (20),
  actor VARCHAR(200),
  region VARCHAR(20),
  release_date VARCHAR(100),
  film_types VARCHAR(20),
  grade FLOAT(2,1),
  intro TEXT,
  poster VARCHAR(100),
  yyyy YEAR,
  city VARCHAR(10),
  turn INT NOT NULL,
  PRIMARY KEY (id,city,turn)
);


/*
表: 即将上映(upcoming)
字段:  编号(u_id),电影名(film_title),导演(director),主演(actor),制片国/地区(region),
      上映日期(release_date),类型(film_types),评分(grade),简介(intro),海报(poster),年份(yyyy)
*/
DROP TABLE IF EXISTS `upcoming`;
CREATE TABLE upcoming(
  id INT UNSIGNED ,
  film_title VARCHAR(50) NOT NULL,
  director VARCHAR (20),
  actor VARCHAR(200),
  region VARCHAR(20),
  release_date VARCHAR(100),
  film_types VARCHAR(20),
  intro TEXT,
  poster VARCHAR(100),
  yyyy YEAR,
  turn INT NOT NULL,
  PRIMARY KEY (id,turn)
);


