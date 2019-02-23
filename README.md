# oodipoc
Proof-of-concept robotic design project for using a MiR 200 robot to guide customers to certain books and sections of the Oodi library in Helsinki

# database 

```
/usr/bin/sqlite3 mir.db
sqlite> create table positions(category Varchar, position Varchar);
sqlite> insert into positions values ("1", "pos_a_1");
sqlite> insert into positions values ("2", "pos_a_2");
sqlite> .quit
```
