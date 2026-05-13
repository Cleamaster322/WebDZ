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
-- Table structure for table `protocol_brakes`
--

DROP TABLE IF EXISTS `protocol_brakes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocol_brakes` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `protocol_id` bigint unsigned DEFAULT NULL,
  `service_brake_type` enum('disc_disc','disc_drum','other') DEFAULT NULL,
  `parking_brake_type` enum('mechanical_hand','mechanical_pedal','electric','other') DEFAULT NULL,
  `service_brake_control_force_axle1_n` float DEFAULT NULL,
  `service_brake_control_force_axle2_n` float DEFAULT NULL,
  `parking_brake_control_force_n` float DEFAULT NULL,
  `axle_1_brake_difference_pct` float DEFAULT NULL,
  `axle_2_brake_difference_pct` float DEFAULT NULL,
  `service_brake_front_left_kn` float DEFAULT NULL,
  `service_brake_front_right_kn` float DEFAULT NULL,
  `service_brake_rear_left_kn` float DEFAULT NULL,
  `service_brake_rear_right_kn` float DEFAULT NULL,
  `parking_brake_left_kn` float DEFAULT NULL,
  `parking_brake_right_kn` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `protocol_id` (`protocol_id`),
  CONSTRAINT `protocol_brakes_ibfk_1` FOREIGN KEY (`protocol_id`) REFERENCES `protocols` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocol_brakes`
--

LOCK TABLES `protocol_brakes` WRITE;
/*!40000 ALTER TABLE `protocol_brakes` DISABLE KEYS */;
INSERT INTO `protocol_brakes` VALUES (1,1,'disc_disc',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,2,'disc_drum','mechanical_hand',198,147,156,5,10,2.21,2.09,1.48,1.33,1.39,1.23),(3,3,'disc_drum',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,4,'disc_drum','mechanical_hand',117,283,215,2,8,2090,2210,1330,1480,1230,1390);
/*!40000 ALTER TABLE `protocol_brakes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-13 21:31:08
