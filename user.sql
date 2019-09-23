CREATE TABLE `user` (
  `username` varchar(16) NOT NULL,
  `password` varchar(16) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `file` varchar(255) DEFAULT NULL,
  `wordcount` int(11) DEFAULT NULL,
  PRIMARY KEY (`username`)
);

ALTER TABLE `users`.`user` 
ADD COLUMN `file` VARCHAR(255) NULL AFTER `email`,
ADD COLUMN `wordcount` INT NULL AFTER `file`;