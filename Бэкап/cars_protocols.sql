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
-- Table structure for table `protocols`
--

DROP TABLE IF EXISTS `protocols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocols` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `protocol_number` varchar(100) NOT NULL,
  `protocol_date` date NOT NULL,
  `status` enum('draft','in_progress','completed','approved','cancelled') DEFAULT 'draft',
  `user_id` bigint unsigned NOT NULL,
  `car_id` bigint unsigned DEFAULT NULL,
  `owner_type` enum('individual','company') DEFAULT 'individual',
  `owner_name` varchar(255) NOT NULL,
  `owner_address` varchar(500) DEFAULT NULL,
  `owner_document` varchar(255) DEFAULT NULL,
  `owner_phone` varchar(50) DEFAULT NULL,
  `appendix_number` varchar(100) DEFAULT NULL,
  `commercial_name` varchar(255) DEFAULT NULL,
  `brand_name` varchar(255) DEFAULT NULL,
  `vehicle_category` enum('M1','N1') DEFAULT NULL,
  `body_type` varchar(255) DEFAULT NULL,
  `vin` varchar(50) DEFAULT NULL,
  `chassis_number` varchar(50) DEFAULT NULL,
  `body_number` varchar(50) DEFAULT NULL,
  `engine_number` varchar(50) DEFAULT NULL,
  `registration_number` varchar(50) DEFAULT NULL,
  `wheel_marking_front` varchar(100) DEFAULT NULL,
  `wheel_marking_rear` varchar(100) DEFAULT NULL,
  `tire_season` enum('summer','winter') DEFAULT NULL,
  `has_spikes` tinyint(1) DEFAULT NULL,
  `manufacture_year` int DEFAULT NULL,
  `color` varchar(100) DEFAULT NULL,
  `inspection_place` varchar(255) DEFAULT NULL,
  `comment` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `dash_fields` json NOT NULL DEFAULT (_utf8mb4'[]'),
  `locked_at` datetime(6) DEFAULT NULL,
  `locked_by_id` int DEFAULT NULL,
  `manufacturer_info` longtext,
  `owner_first_name` varchar(150) DEFAULT NULL,
  `owner_last_name` varchar(150) DEFAULT NULL,
  `owner_middle_name` varchar(150) DEFAULT NULL,
  `cancelled_at` datetime(6) DEFAULT NULL,
  `cancelled_by_id` int DEFAULT NULL,
  `returned_for_revision` tinyint(1) NOT NULL,
  `revision_comment` longtext,
  PRIMARY KEY (`id`),
  KEY `protocols_locked_by_id_cf6314bc_fk_auth_user_id` (`locked_by_id`),
  KEY `protocols_cancelled_by_id_7685c3dc_fk_auth_user_id` (`cancelled_by_id`),
  CONSTRAINT `protocols_cancelled_by_id_7685c3dc_fk_auth_user_id` FOREIGN KEY (`cancelled_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `protocols_locked_by_id_cf6314bc_fk_auth_user_id` FOREIGN KEY (`locked_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocols`
--

LOCK TABLES `protocols` WRITE;
/*!40000 ALTER TABLE `protocols` DISABLE KEYS */;
INSERT INTO `protocols` VALUES (1,'00003','2026-05-22','draft',1,6218,'individual','Не указано',NULL,NULL,NULL,NULL,'X5','BMW',NULL,'SUV',NULL,NULL,NULL,NULL,NULL,'275/35R22','315/30R22',NULL,NULL,2023,NULL,NULL,NULL,'2026-05-03 14:58:26','2026-05-22 03:59:34','[]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(2,'1202605040002','2026-05-04','draft',1,NULL,'individual','Не указано',NULL,NULL,NULL,'TMP-1-20260504-0002','RIO','KIA','M1','CB 41','Z94CB41BBHR327751',NULL,NULL,NULL,NULL,'185/65 R15','185/65 R15','winter',0,2016,'белый',NULL,NULL,'2026-05-03 15:09:59','2026-05-26 01:43:30','[]',NULL,NULL,NULL,NULL,NULL,NULL,'2026-05-26 01:43:30.299167',7,1,'Не'),(3,'1202605080001','2026-05-08','approved',1,53773,'individual','Не указано',NULL,NULL,NULL,NULL,'DAYZ','Nissan','M1','Хэтчбек 5 дв.','B43W-0105450',NULL,NULL,NULL,NULL,'155/65R14','155/65R14',NULL,NULL,2019,NULL,NULL,NULL,'2026-05-07 23:44:39','2026-05-26 01:22:34','[]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(4,'00001','2026-05-10','cancelled',1,53773,'individual','Не указано',NULL,NULL,NULL,NULL,'DAYZ','Nissan','M1','B43W','B43W-0105450',NULL,NULL,NULL,NULL,'155/65R14','155/65R14','summer',0,2020,'серый',NULL,NULL,'2026-05-09 17:36:10','2026-05-26 01:24:28','[]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(5,'01101','2026-05-14','draft',1,69502,'individual','Не указано',NULL,NULL,NULL,'1101','Escudo','Suzuki',NULL,'TDA4W',NULL,NULL,NULL,NULL,NULL,'225/60R18','225/60R18',NULL,NULL,2008,NULL,NULL,NULL,'2026-05-22 03:09:07','2026-05-23 10:07:31','[]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(6,'00006','2026-05-23','draft',6,NULL,'individual','Не указано',NULL,NULL,NULL,NULL,'Escudo','Suzuki',NULL,'Джип/SUV 5 дв.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-05-22 17:53:19','2026-05-23 10:23:12','[]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(7,'00007','2026-05-23','draft',1,126890,'individual','Не указано',NULL,NULL,NULL,'00007','Voxy','Toyota','M1','AZR65G',NULL,NULL,NULL,NULL,NULL,'195/65R15','195/65R15','summer',0,2006,'Серый',NULL,NULL,'2026-05-22 23:21:25','2026-05-26 01:24:46','[]',NULL,NULL,'Русская 98','Виктор','Олейник','Витальевич',NULL,NULL,0,NULL);
/*!40000 ALTER TABLE `protocols` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-26 12:45:39
