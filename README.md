# oodipoc
Proof-of-concept robotic design project for using a MiR 200 robot to guide customers to certain books and sections of the Oodi library in Helsinki

# database 

```
/usr/bin/sqlite3 mir.db
sqlite> create table positions(category Varchar, position Varchar);
sqlite> insert into positions values ('a', 'e4537652-3b2b-11e9-9f5c-94c691a3a93e');
sqlite> insert into positions values ('b', '0d73ae4b-3b2c-11e9-9f5c-94c691a3a93e');
sqlite> insert into positions values ('c', '3aa7d61d-3b2c-11e9-9f5c-94c691a3a93e');
sqlite> insert into positions values ('d', '59c1c252-3b2c-11e9-9f5c-94c691a3a93e');
sqlite> .quit
```
