use Restaurant;
-- 删除已存在的表
drop table if exists fixedpackage;

create table fixedpackage(
id int primary key auto_increment,
cname varchar(30) not null,
cprice float not null,
points int not null comment "积分",
peicai varchar(200) null comment "配菜",
type varchar(50) not null comment "种类",
stock int not null comment "库存",
images Text not null,
mealmeans varchar(200) not null
)comment "固定套餐信息表";

insert into fixedpackage(cname,cprice,points,peicai,type,stock,mealmeans,images) values
('超值双拼饭',16.00,16,'','经济套餐',29,'固定套餐','images/1256713249.jpg'),
('招牌照烧煎鸡饭',16.00,16,'','经济套餐',28,'固定套餐','images/1256714813.jpg'),
('招牌黑椒煎鸡饭',16.00,16,'','经济套餐',30,'固定套餐','images/1256714813.jpg'),
('经济套餐',8.00,8,'随机','经济套餐',99,'固定套餐','images/1257469703.jpg'),
('白领精英商务套餐',15.00,15,'鱼香小滑肉＋酸辣白菜＋清炒油麦菜','商务套餐',25,'固定套餐','images/1252398682.jpg'),
('商务套餐I',10.00,10,'','商务套餐',100,'固定套餐','images/1257469860.jpg'),
('商务套餐II',12.00,12,'','商务套餐',100,'固定套餐','images/1257469896.jpg'),
('商务套餐III',15.00,15,'','商务套餐',100,'固定套餐','images/1257469936.jpg'),
('精品回锅肉盖浇饭',12.00,12,'回锅肉＋酸辣土豆丝＋小白菜','精品盖饭',40,'固定套餐','images/1252397853.jpg'),
('白油鸡丝盖饭',13.00,13,'','精品盖饭',30,'固定套餐','images/1254189848.jpg');

