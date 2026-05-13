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
-- Table structure for table `protocol_measurements`
--

DROP TABLE IF EXISTS `protocol_measurements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocol_measurements` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `protocol_id` bigint unsigned DEFAULT NULL,
  `wheel_formula` enum('4x2_front','4x2_rear','4x4') DEFAULT NULL,
  `mufflers_count` int DEFAULT NULL,
  `seats_count` varchar(50) DEFAULT NULL,
  `steps_present` tinyint(1) DEFAULT NULL,
  `engine_model` varchar(255) DEFAULT NULL,
  `engine_power_kw` int DEFAULT NULL,
  `engine_layout` enum('transverse','longitudinal') DEFAULT NULL,
  `cylinder_layout` enum('inline','opposed','v_shape') DEFAULT NULL,
  `cylinders_count` int DEFAULT NULL,
  `fuel_type` enum('petrol','diesel','hybrid','electric') DEFAULT NULL,
  `turbo_present` tinyint(1) DEFAULT NULL,
  `steering_booster_type` enum('hydraulic','electric') DEFAULT NULL,
  `transmission_type` enum('automatic','variator','manual','robot','reductor') DEFAULT NULL,
  `tire_depth_fl_mm` float DEFAULT NULL,
  `tire_depth_fr_mm` float DEFAULT NULL,
  `tire_depth_rl_mm` float DEFAULT NULL,
  `tire_depth_rr_mm` float DEFAULT NULL,
  `bumper_bends_to_body` tinyint(1) DEFAULT NULL,
  `bumper_to_body_distance_mm` float DEFAULT NULL,
  `opening_roof_present` tinyint(1) DEFAULT NULL,
  `fuel_tank_leak_protection_measure` varchar(255) DEFAULT NULL,
  `protruding_elements_doors_mm` float DEFAULT NULL,
  `protruding_elements_other_mm` float DEFAULT NULL,
  `glass_transparency_right_pct` float DEFAULT NULL,
  `glass_transparency_left_pct` float DEFAULT NULL,
  `glass_transparency_windshield_pct` float DEFAULT NULL,
  `sun_strip_width_mm` float DEFAULT NULL,
  `steering_backlash_deg` float DEFAULT NULL,
  `speed_by_speedometer_kmh` float DEFAULT NULL,
  `actual_speed_kmh` float DEFAULT NULL,
  `exhaust_noise_constant_db` float DEFAULT NULL,
  `exhaust_noise_deceleration_db` decimal(8,2) DEFAULT NULL,
  `co_min_pct` float DEFAULT NULL,
  `co_max_pct` float DEFAULT NULL,
  `light_absorption_1` float DEFAULT NULL,
  `light_absorption_2` float DEFAULT NULL,
  `light_absorption_3` float DEFAULT NULL,
  `light_absorption_4` float DEFAULT NULL,
  `light_absorption_5` float DEFAULT NULL,
  `light_absorption_6` float DEFAULT NULL,
  `vehicle_length_mm` float DEFAULT NULL,
  `vehicle_width_mm` float DEFAULT NULL,
  `vehicle_height_mm` float DEFAULT NULL,
  `vehicle_weight_kg` float DEFAULT NULL,
  `axle1_load_kg` float DEFAULT NULL,
  `axle2_load_kg` float DEFAULT NULL,
  `stand_axle1_load_kg` float DEFAULT NULL,
  `stand_axle2_load_kg` float DEFAULT NULL,
  `mileage_km` float DEFAULT NULL,
  `spare_wheel_present` tinyint DEFAULT NULL,
  `steering_lock_present` tinyint DEFAULT NULL,
  `gas_equipment_present` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `protocol_id` (`protocol_id`),
  CONSTRAINT `protocol_measurements_ibfk_1` FOREIGN KEY (`protocol_id`) REFERENCES `protocols` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocol_measurements`
--

LOCK TABLES `protocol_measurements` WRITE;
/*!40000 ALTER TABLE `protocol_measurements` DISABLE KEYS */;
INSERT INTO `protocol_measurements` VALUES (1,1,NULL,NULL,'2/2/3',NULL,'B57D30B',9,NULL,'inline',6,'diesel',NULL,NULL,'automatic',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,4935,2005,1770,2370,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,2,'4x2_front',1,'2/3',0,'G4FC',NULL,'transverse','inline',4,'petrol',0,'hydraulic','automatic',6,6,6,6,1,1,0,'other_measure',25,16,80.7,80.9,82.3,90,2,20,20,82,80.00,0,0,NULL,NULL,NULL,NULL,NULL,NULL,4377,1700,1470,1240,740,500,740,500,NULL,NULL,NULL,NULL),(3,3,'4x2_front',NULL,'2/2',NULL,'BR06DE',38,NULL,'inline',3,'petrol',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,3395,1475,1640,830,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,4,'4x2_front',1,'2/2',1,'BR06DE',38,'transverse','inline',3,'petrol',0,'electric','variator',6,6,6,6,NULL,1,0,NULL,20,10,79.4,79.2,80.5,90,2,21,20,82,80.00,0,0,NULL,NULL,NULL,NULL,NULL,NULL,3395,1475,1640,830,NULL,NULL,NULL,NULL,98000,1,1,0);
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

-- Dump completed on 2026-05-13 21:31:08
