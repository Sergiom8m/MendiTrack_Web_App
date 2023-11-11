CREATE DATABASE IF NOT EXISTS `appDb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `appDb`;

CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2;


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

INSERT INTO `rutas` (`id`, `email`, `nombre`, `dificultad`, `distancia`, `desnivel`, `link`) VALUES ('1', 'sergiomartinportillo8@gmail.com', 'Faro del caballo', '4', '9.28', '624', 'https://www.strava.com/activities/10025666374');
INSERT INTO `rutas` (`id`, `email`, `nombre`, `dificultad`, `distancia`, `desnivel`, `link`) VALUES ('2', 'sergiomartinportillo8@gmail.com', 'Gallarraga desde La Quadra', '7', '13.68', '930', 'https://www.strava.com/activities/9271843453');




