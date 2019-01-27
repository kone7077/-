use Restaurant;
-- 删除已存在的表
drop table if exists goodsreplace;
create table goodsreplace(
    id primary key auto_increment,
    goodsname varchar(30) not null,
    points_price int not null,
    images Text not null,
)comment "积分换赠赠品信息表"