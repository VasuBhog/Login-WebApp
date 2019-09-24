SET SQL_SAFE_UPDATES = 0;
Select * from `users`.`user` where username=2;
DELETE FROM `users`.`user`;
Update `users`.`user` set wordcount=3 WHERE username = 2;
Select file from `users`.`user` where username=2