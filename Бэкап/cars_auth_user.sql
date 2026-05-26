-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: cars
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$ry4MWYbQgHyYHnB2WX0L1h$kwNygcZ4Q7/JDUyMJo6tk8c/ftl++Ib9et8yYmRfB2Y=','2025-05-21 07:50:49.246343',1,'admin','','','',1,1,'2025-05-16 07:08:50.476294'),(4,'pbkdf2_sha256$1000000$VhtElx4Ye4kh6xZ5UY3NBH$n1dSLnhUP6lynJo1xCScDQjn3z+RO7QhqDqBPB5O6LU=',NULL,0,'test1','test1','test1','test1@mail.ru',0,1,'2026-05-23 03:36:26.788831'),(5,'pbkdf2_sha256$1000000$tbK5S0NPBCap4XoYBY5YuT$cMHXxfI11C/7yTDbAeVqz3YHkRIlVkXgklPlDuYO5Os=',NULL,0,'test2','test2','test2','test2@mail.ru',0,1,'2026-05-23 03:36:38.493486'),(6,'pbkdf2_sha256$1000000$A0zi0FGU8alAvLk400Y6f8$XNLGT+pDDx+W+EBfnlsDKEeQbsnyreZYnTYXB1YzvB8=',NULL,0,'test3','test3','test3','test3@mail.ru',0,1,'2026-05-23 03:36:51.892084'),(7,'pbkdf2_sha256$1000000$fvki9YMcZTRoAYVbNlMq83$Z/qlpRbuRF4ziqZ4T5epycDJW8tpT0mSgFyG5juEj1k=',NULL,0,'test4','test4','test4','test4@mail.ru',0,1,'2026-05-26 01:05:20.891132');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-26 12:45:43
