use Restaurant;
-- 删除已存在的表
drop table if exists orderrecord;

create table orderrecord(
    id int primary key auto_increment,
    username varchar(30) not null,
    cname varchar(30) not null,
    cprice float not null,
    type varchar(15) not null comment "种类",
    mealmeans varchar(200) not null,
    ordertime datetime not null
)comment "用户点餐记录表";