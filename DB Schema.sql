Create database tracker_db;

use tracker_db;

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `pwd` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);


DROP TABLE IF EXISTS `tracker`;

CREATE TABLE `tracker` (
  `id` int DEFAULT NULL,
  `src` varchar(255) DEFAULT NULL,
  `amt` varchar(255) DEFAULT NULL,
  `src_type` varchar(255) DEFAULT NULL
)

describe users;