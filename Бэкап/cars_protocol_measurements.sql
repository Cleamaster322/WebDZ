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
-- Table structure for table `protocol_measurements`
--

DROP TABLE IF EXISTS `protocol_measurements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocol_measurements` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `protocol_id` bigint unsigned NOT NULL,
  `wheel_formula` enum('4x2_front','4x2_rear','4x4') DEFAULT NULL,
  `mufflers_count` smallint unsigned DEFAULT NULL,
  `seats_count` smallint unsigned DEFAULT NULL,
  `suspension_present` tinyint(1) DEFAULT NULL,
  `engine_layout` enum('transverse','longitudinal') DEFAULT NULL,
  `cylinder_layout` enum('inline','opposed','v_shape') DEFAULT NULL,
  `cylinders_count` smallint unsigned DEFAULT NULL,
  `fuel_type` enum('petrol','diesel','hybrid','electric','other') DEFAULT NULL,
  `turbo_present` tinyint(1) DEFAULT NULL,
  `transmission_type` enum('automatic','cvt','manual','robot','reducer','other') DEFAULT NULL,
  `tire_depth_fl_mm` decimal(6,2) DEFAULT NULL,
  `tire_depth_fr_mm` decimal(6,2) DEFAULT NULL,
  `tire_depth_rl_mm` decimal(6,2) DEFAULT NULL,
  `tire_depth_rr_mm` decimal(6,2) DEFAULT NULL,
  `bumper_to_body_distance_mm` decimal(6,2) DEFAULT NULL,
  `protruding_elements_doors_mm` decimal(6,2) DEFAULT NULL,
  `protruding_elements_other_mm` decimal(6,2) DEFAULT NULL,
  `glass_transparency_right_pct` decimal(5,2) DEFAULT NULL,
  `glass_transparency_left_pct` decimal(5,2) DEFAULT NULL,
  `glass_transparency_windshield_pct` decimal(5,2) DEFAULT NULL,
  `sun_strip_width_mm` decimal(6,2) DEFAULT NULL,
  `steering_backlash_deg` decimal(6,2) DEFAULT NULL,
  `speed_by_speedometer_kmh` decimal(6,2) DEFAULT NULL,
  `actual_speed_kmh` decimal(6,2) DEFAULT NULL,
  `exhaust_noise_db` decimal(6,2) DEFAULT NULL,
  `co_min_pct` decimal(6,3) DEFAULT NULL,
  `co_max_pct` decimal(6,3) DEFAULT NULL,
  `light_absorption_1` decimal(8,3) DEFAULT NULL,
  `light_absorption_2` decimal(8,3) DEFAULT NULL,
  `light_absorption_3` decimal(8,3) DEFAULT NULL,
  `light_absorption_4` decimal(8,3) DEFAULT NULL,
  `light_absorption_5` decimal(8,3) DEFAULT NULL,
  `light_absorption_6` decimal(8,3) DEFAULT NULL,
  `vehicle_length_mm` decimal(10,2) DEFAULT NULL,
  `vehicle_width_mm` decimal(10,2) DEFAULT NULL,
  `vehicle_height_mm` decimal(10,2) DEFAULT NULL,
  `vehicle_weight_kg` decimal(10,2) DEFAULT NULL,
  `axle1_load_kg` decimal(10,2) DEFAULT NULL,
  `axle2_load_kg` decimal(10,2) DEFAULT NULL,
  `stand_axle1_load_kg` decimal(10,2) DEFAULT NULL,
  `stand_axle2_load_kg` decimal(10,2) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_protocol_measurements_protocol_id` (`protocol_id`),
  CONSTRAINT `fk_protocol_measurements_protocol` FOREIGN KEY (`protocol_id`) REFERENCES `protocols` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocol_measurements`
--

LOCK TABLES `protocol_measurements` WRITE;
/*!40000 ALTER TABLE `protocol_measurements` DISABLE KEYS */;
INSERT INTO `protocol_measurements` VALUES (1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,5.50,5.40,5.30,5.20,NULL,NULL,NULL,79.10,78.50,75.00,NULL,2.00,60.00,59.80,72.30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,4650.00,1800.00,1420.00,1450.00,NULL,NULL,NULL,NULL,'2026-04-17 03:36:54','2026-04-17 03:37:28');
/*!40000 ALTER TABLE `protocol_measurements` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-17 17:20:09
