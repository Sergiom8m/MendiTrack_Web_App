CREATE DATABASE IF NOT EXISTS `appDb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `appDb`;

CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2;

INSERT INTO `users` (`id`, `username`, `password`, `email`) VALUES (1, 'root', '02be4d57999261838cebe45ec83ba6c1beb1457a', 'root@root.com');

CREATE TABLE IF NOT EXISTS `rutas` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(100) NOT NULL,
    `nombre` varchar(255) NOT NULL,
    `dificultad` int(11) NOT NULL,
    `distancia` double NOT NULL,
    `desnivel` double NOT NULL,
    `link` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2;

INSERT INTO `rutas` (`id`, `email`, `nombre`, `dificultad`, `distancia`, `desnivel`, `link`) VALUES ('1', 'root@root.com', 'bilabno', '1', '12', '12', 'https://www.ehu.eus');




