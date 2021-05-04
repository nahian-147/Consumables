create database if not exists CONSUMABLES;

use CONSUMABLES;

create table if not exists consumables  (id int not null auto_increment,
                                         type varchar(10) not null,
                                         name varchar(100) not null,
                                         consStart date not null,
                                         consEnd date,
					                     rating float default 0.0,
                                         consTime float default 0.0,
					                     total_days int default 0,
				                         primary key(id));

create table if not exists deleteds     (id int not null,
                                         type varchar(10) not null,
                                         name varchar(100) not null,
                                         consStart date not null,
                                         consEnd date,
					                     rating float default 0.0,
                                         consTime float default 0.0,
					                     total_days int default 0);

create table if not exists total (total_time float default 0.0,
			          total_days int default 0);

insert into total value (0,0);
