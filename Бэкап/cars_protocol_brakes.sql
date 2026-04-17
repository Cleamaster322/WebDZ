-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: cars
-- ------------------------------------------------------
-- Server version	8.0.35

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
  `protocol_id` bigint unsigned NOT NULL,
  `service_brake_type` enum('disc_disc','disc_drum','other') DEFAULT NULL,
  `parking_brake_type` enum('mechanical_hand','mechanical_pedal','electric','other') DEFAULT NULL,
  `service_brake_control_force_axle1_n` decimal(10,2) DEFAULT NULL,
  `service_brake_control_force_axle2_n` decimal(10,2) DEFAULT NULL,
  `parking_brake_control_force_n` decimal(10,2) DEFAULT NULL,
  `axle_1_brake_difference_pct` decimal(6,2) DEFAULT NULL,
  `axle_2_brake_difference_pct` decimal(6,2) DEFAULT NULL,
  `service_brake_front_left_kn` decimal(10,3) DEFAULT NULL,
  `service_brake_front_right_kn` decimal(10,3) DEFAULT NULL,
  `service_brake_rear_left_kn` decimal(10,3) DEFAULT NULL,
  `service_brake_rear_right_kn` decimal(10,3) DEFAULT NULL,
  `parking_brake_left_kn` decimal(10,3) DEFAULT NULL,
  `parking_brake_right_kn` decimal(10,3) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_protocol_brakes_protocol_id` (`protocol_id`),
  CONSTRAINT `fk_protocol_brakes_protocol` FOREIGN KEY (`protocol_id`) REFERENCES `protocols` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocol_brakes`
--

LOCK TABLES `protocol_brakes` WRITE;
/*!40000 ALTER TABLE `protocol_brakes` DISABLE KEYS */;
INSERT INTO `protocol_brakes` VALUES (1,1,NULL,NULL,NULL,NULL,NULL,NULL,1.50,2.345,2.300,1.980,2.010,1.200,1.180,'2026-04-17 03:36:54','2026-04-17 03:37:32');
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

-- Dump completed on 2026-04-17 17:33:23
