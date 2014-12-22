

## 同物異名處理

array 拆解，取名
    select id,name,p from (select id,name,unnest(zh_name) as p from namelist) as t where p like '狗尾%';

## 資料結構

baselist 改成 json format?
