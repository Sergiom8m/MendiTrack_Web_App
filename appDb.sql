CREATE DATABASE IF NOT EXISTS `appDb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `appDb`;

CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `users` (`id`, `username`, `password`, `email`) VALUES (1, 'root', '02be4d57999261838cebe45ec83ba6c1beb1457a', 'root@root.com');