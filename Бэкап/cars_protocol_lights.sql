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
-- Table structure for table `protocol_lights`
--

DROP TABLE IF EXISTS `protocol_lights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocol_lights` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `protocol_id` bigint unsigned NOT NULL,
  `low_beam_count` smallint unsigned DEFAULT NULL,
  `high_beam_count` smallint unsigned DEFAULT NULL,
  `front_fog_count` smallint unsigned DEFAULT NULL,
  `reverse_light_count` smallint unsigned DEFAULT NULL,
  `turn_signal_count` smallint unsigned DEFAULT NULL,
  `front_position_light_count` smallint unsigned DEFAULT NULL,
  `rear_position_light_count` smallint unsigned DEFAULT NULL,
  `main_brake_signal_count` smallint unsigned DEFAULT NULL,
  `additional_brake_signal_count` smallint unsigned DEFAULT NULL,
  `rear_fog_count` smallint unsigned DEFAULT NULL,
  `plate_light_count` smallint unsigned DEFAULT NULL,
  `daytime_running_light_count` smallint unsigned DEFAULT NULL,
  `parking_light_count` smallint unsigned DEFAULT NULL,
  `headlight_type` enum('halogen','xenon','led','other') DEFAULT NULL,
  `low_beam_upper_point_mm` decimal(10,2) DEFAULT NULL,
  `low_beam_lower_point_mm` decimal(10,2) DEFAULT NULL,
  `fog_light_upper_point_mm` decimal(10,2) DEFAULT NULL,
  `fog_light_lower_point_mm` decimal(10,2) DEFAULT NULL,
  `fog_light_left_distance_mm` decimal(10,2) DEFAULT NULL,
  `fog_light_right_distance_mm` decimal(10,2) DEFAULT NULL,
  `brake_signal_upper_point_mm` decimal(10,2) DEFAULT NULL,
  `brake_signal_lower_point_mm` decimal(10,2) DEFAULT NULL,
  `brake_signal_left_distance_mm` decimal(10,2) DEFAULT NULL,
  `brake_signal_right_distance_mm` decimal(10,2) DEFAULT NULL,
  `additional_brake_signal_from_glass_edge_mm` decimal(10,2) DEFAULT NULL,
  `additional_brake_signal_from_support_surface_mm` decimal(10,2) DEFAULT NULL,
  `additional_brake_signal_optical_center_shift_mm` decimal(10,2) DEFAULT NULL,
  `rear_fog_upper_point_mm` decimal(10,2) DEFAULT NULL,
  `rear_fog_lower_point_mm` decimal(10,2) DEFAULT NULL,
  `headlight_washer_present` tinyint(1) DEFAULT NULL,
  `left_34v_cd` decimal(12,2) DEFAULT NULL,
  `left_52h_cd` decimal(12,2) DEFAULT NULL,
  `left_high_beam_cd` decimal(12,2) DEFAULT NULL,
  `right_34v_cd` decimal(12,2) DEFAULT NULL,
  `right_52h_cd` decimal(12,2) DEFAULT NULL,
  `right_high_beam_cd` decimal(12,2) DEFAULT NULL,
  `turn_signal_frequency_per_min` decimal(10,2) DEFAULT NULL,
  `turn_signal_frequency_hz` decimal(10,2) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_protocol_lights_protocol_id` (`protocol_id`),
  CONSTRAINT `fk_protocol_lights_protocol` FOREIGN KEY (`protocol_id`) REFERENCES `protocols` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocol_lights`
--

LOCK TABLES `protocol_lights` WRITE;
/*!40000 ALTER TABLE `protocol_lights` DISABLE KEYS */;
INSERT INTO `protocol_lights` VALUES (1,1,2,2,2,2,4,2,2,2,1,1,2,2,2,'led',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,90.00,1.50,'2026-04-17 03:36:54','2026-04-17 03:37:35');
/*!40000 ALTER TABLE `protocol_lights` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-17 17:20:06
