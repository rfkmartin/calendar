drop database if exists cal;
create database cal;
use cal;

create table menu (
   menu_date date,
   menu varchar(1024),
   primary key (menu_date)
);

create table kv (
   id int not null auto_increment,
   k varchar(32),
   v varchar(32),
   primary key (id)
);

insert into kv(k,v) values ('last_checked','2023/11/26');