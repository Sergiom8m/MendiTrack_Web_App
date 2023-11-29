CREATE DATABASE IF NOT EXISTS `appDb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `appDb`;

CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE(`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2;


CREATE TABLE IF NOT EXISTS `rutas` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(100) NOT NULL,
    `nombre` varchar(255) NOT NULL,
    `public` BOOLEAN NOT NULL DEFAULT FALSE,
    `dificultad` int(11) NOT NULL,
    `distancia` double NOT NULL,
    `desnivel` int(11) NOT NULL,
    `link` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2;

INSERT INTO `rutas` (`id`, `email`, `nombre`, `public`, `dificultad`, `distancia`, `desnivel`, `link`) VALUES ('1', 'sergiomartinportillo8@gmail.com', 'Faro del caballo', 1,  '4', '9.28', '624', 'https://www.strava.com/activities/10025666374');
INSERT INTO `rutas` (`id`, `email`, `nombre`, `public`, `dificultad`, `distancia`, `desnivel`, `link`) VALUES ('2', 'sergiomartinportillo8@gmail.com', 'Gallarraga desde La Quadra', 1, '7', '13.68', '930', 'https://www.strava.com/activities/9271843453');
INSERT INTO `rutas` (`id`, `email`, `nombre`, `public`, `dificultad`, `distancia`, `desnivel`, `link`) VALUES ('3', 'iker02@gmail.com', 'Ganekogorta desde Rekalde', 1,  '7', '18.07', '1004', 'https://es.wikiloc.com/rutas-senderismo/ganeko-desde-rekalde-ida-vuelta-10987585');
INSERT INTO `rutas` (`id`, `email`, `nombre`, `public`, `dificultad`, `distancia`, `desnivel`, `link`) VALUES ('4', 'josusanturtzi@gmail.com', 'Serantes igoera', 1,  '5', '3.94', '231', 'https://es.wikiloc.com/rutas-senderismo/serantes-desde-barrio-los-heros-abanto-y-ciervana-11139351');




