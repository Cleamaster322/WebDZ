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
-- Table structure for table `protocol_photos`
--

DROP TABLE IF EXISTS `protocol_photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protocol_photos` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `protocol_id` bigint unsigned DEFAULT NULL,
  `photo_type` enum('front_view','rear_view','left_view','right_view','vin_photo','nameplate_photo','tire_size_label_photo','odometer_photo','gas_test_photo','noise_test_photo','stand_test_photo','other') DEFAULT NULL,
  `file_path` varchar(500) DEFAULT NULL,
  `sort_order` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `protocol_id` (`protocol_id`),
  CONSTRAINT `protocol_photos_ibfk_1` FOREIGN KEY (`protocol_id`) REFERENCES `protocols` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocol_photos`
--

LOCK TABLES `protocol_photos` WRITE;
/*!40000 ALTER TABLE `protocol_photos` DISABLE KEYS */;
INSERT INTO `protocol_photos` VALUES (4,1,'noise_test_photo','protocol_photos/1/noise_test_photo_b7cc099d456b494badc60ceb4638ff9c.png',3,'2026-05-22 01:59:46'),(5,2,'stand_test_photo','protocol_photos/2/stand_test_photo_7d5f699669694eadabe03f63bf065317.png',1,'2026-05-22 02:02:14'),(6,1,'stand_test_photo','protocol_photos/1/stand_test_photo_24f22fc35a1a4703b5dfdd04d92d609b.jpg',1,'2026-05-22 02:07:54'),(7,1,'gas_test_photo','protocol_photos/1/gas_test_photo_50b1a8bd3ac5486f903f0079bacb3465.jpg',2,'2026-05-22 02:11:44'),(8,1,'other','protocol_photos/1/other_8c8b4c111d7047ff974e98638a68821e.png',10,'2026-05-22 02:25:14');
/*!40000 ALTER TABLE `protocol_photos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-26 12:45:42
