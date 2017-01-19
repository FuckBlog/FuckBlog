
drop database if exists fuckblog;

create database fuckblog;

use fuckblog;
grant select, insert, update, delete on fuckblog.* to 'fuck'@'localhost' identified by 'www-data';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `password` varchar(50) not null,
    `admin_flag` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_time` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_time` (`created_time`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `blog_title` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_time` real not null,
	`tag` mediumtext not null,
    key `idx_created_time` (`created_time`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_time` real not null,
    key `idx_created_time` (`created_time`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table oauth (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `created_time` real not null,
    key `idx_created_time` (`created_time`),
    unique key `idx_uid` (`user_id`),
    primary key (`id`)
) engine=innodb default charset=utf8;
