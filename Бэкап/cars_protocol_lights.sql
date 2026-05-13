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
-- Table structure for table `protocol_lights`
--

DROP TABLE IF EXISTS `protocol_lights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocol_lights` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `protocol_id` bigint unsigned DEFAULT NULL,
  `low_beam_count` int DEFAULT NULL,
  `low_beam_color` varchar(50) DEFAULT NULL,
  `high_beam_count` int DEFAULT NULL,
  `high_beam_color` varchar(50) DEFAULT NULL,
  `front_fog_count` int DEFAULT NULL,
  `front_fog_color` varchar(50) DEFAULT NULL,
  `reverse_light_count` int DEFAULT NULL,
  `reverse_light_color` varchar(50) DEFAULT NULL,
  `turn_signal_count` int DEFAULT NULL,
  `turn_signal_color` varchar(50) DEFAULT NULL,
  `front_position_light_count` int DEFAULT NULL,
  `front_position_light_color` varchar(50) DEFAULT NULL,
  `rear_position_light_count` int DEFAULT NULL,
  `rear_position_light_color` varchar(50) DEFAULT NULL,
  `main_brake_signal_count` int DEFAULT NULL,
  `main_brake_signal_color` varchar(50) DEFAULT NULL,
  `additional_brake_signal_count` int DEFAULT NULL,
  `additional_brake_signal_color` varchar(50) DEFAULT NULL,
  `rear_fog_count` int DEFAULT NULL,
  `rear_fog_color` varchar(50) DEFAULT NULL,
  `plate_light_count` int DEFAULT NULL,
  `plate_light_color` varchar(50) DEFAULT NULL,
  `daytime_running_light_count` int DEFAULT NULL,
  `daytime_running_light_color` varchar(50) DEFAULT NULL,
  `parking_light_count` int DEFAULT NULL,
  `parking_light_color` varchar(50) DEFAULT NULL,
  `headlight_type` enum('halogen','xenon','led','other') DEFAULT NULL,
  `low_beam_upper_point_mm` float DEFAULT NULL,
  `low_beam_lower_point_mm` float DEFAULT NULL,
  `fog_light_upper_point_mm` float DEFAULT NULL,
  `fog_light_lower_point_mm` float DEFAULT NULL,
  `fog_light_left_distance_mm` float DEFAULT NULL,
  `fog_light_right_distance_mm` float DEFAULT NULL,
  `brake_signal_upper_point_mm` float DEFAULT NULL,
  `brake_signal_lower_point_mm` float DEFAULT NULL,
  `brake_signal_left_distance_mm` float DEFAULT NULL,
  `brake_signal_right_distance_mm` float DEFAULT NULL,
  `additional_brake_signal_from_glass_edge_mm` float DEFAULT NULL,
  `additional_brake_signal_from_support_surface_mm` float DEFAULT NULL,
  `additional_brake_signal_optical_center_shift_mm` float DEFAULT NULL,
  `rear_fog_upper_point_mm` float DEFAULT NULL,
  `rear_fog_lower_point_mm` float DEFAULT NULL,
  `headlight_washer_present` tinyint(1) DEFAULT NULL,
  `left_34v_cd` float DEFAULT NULL,
  `left_52h_cd` float DEFAULT NULL,
  `left_high_beam_cd` float DEFAULT NULL,
  `right_34v_cd` float DEFAULT NULL,
  `right_52h_cd` float DEFAULT NULL,
  `right_high_beam_cd` float DEFAULT NULL,
  `turn_signal_frequency_per_min` float DEFAULT NULL,
  `turn_signal_frequency_hz` float DEFAULT NULL,
  `rear_parking_light_count` int DEFAULT NULL,
  `rear_parking_light_color` varchar(50) DEFAULT NULL,
  `adaptive_front_lighting_count` int DEFAULT NULL,
  `adaptive_front_lighting_color` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `protocol_id` (`protocol_id`),
  CONSTRAINT `protocol_lights_ibfk_1` FOREIGN KEY (`protocol_id`) REFERENCES `protocols` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocol_lights`
--

LOCK TABLES `protocol_lights` WRITE;
/*!40000 ALTER TABLE `protocol_lights` DISABLE KEYS */;
INSERT INTO `protocol_lights` VALUES (1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,2,2,'белый',2,'белый',NULL,NULL,2,'белый',2,'желтый',2,'белый',2,'красный',2,'красный',1,'красный',2,'красный',2,'белый',2,'белый',NULL,NULL,'halogen',780,630,NULL,NULL,NULL,NULL,955,890,150,150,10,1140,0,940,850,1,450,3500,19000,470,3800,21000,84,1.4,NULL,NULL,NULL,NULL),(3,3,2,'белый',2,'белый',NULL,'белый',NULL,'белый',2,'автожелтый',2,'белый',2,'красный',2,'красный',NULL,'красный',NULL,'красный',NULL,'белый',NULL,'белый',NULL,'белый',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'красный',NULL,'белый'),(4,4,2,'белый',2,'белый',0,'белый',2,'белый',2,'автожелтый',2,'белый',2,'красный',2,'красный',1,'красный',0,'красный',2,'белый',0,'белый',0,'белый','halogen',985,818,NULL,NULL,NULL,NULL,1190,1070,100,100,5,1136,0,0,0,0,553,12300,34900,560,14600,37500,84,1.4,0,'красный',0,'белый');
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

-- Dump completed on 2026-05-13 21:31:06
