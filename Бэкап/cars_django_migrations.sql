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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-05-16 07:07:35.665767'),(2,'auth','0001_initial','2025-05-16 07:07:36.186240'),(3,'admin','0001_initial','2025-05-16 07:07:36.286331'),(4,'admin','0002_logentry_remove_auto_add','2025-05-16 07:07:36.291335'),(5,'admin','0003_logentry_add_action_flag_choices','2025-05-16 07:07:36.296340'),(6,'contenttypes','0002_remove_content_type_name','2025-05-16 07:07:36.397992'),(7,'auth','0002_alter_permission_name_max_length','2025-05-16 07:07:36.457047'),(8,'auth','0003_alter_user_email_max_length','2025-05-16 07:07:36.474062'),(9,'auth','0004_alter_user_username_opts','2025-05-16 07:07:36.478067'),(10,'auth','0005_alter_user_last_login_null','2025-05-16 07:07:36.520104'),(11,'auth','0006_require_contenttypes_0002','2025-05-16 07:07:36.521107'),(12,'auth','0007_alter_validators_add_error_messages','2025-05-16 07:07:36.526110'),(13,'auth','0008_alter_user_username_max_length','2025-05-16 07:07:36.572152'),(14,'auth','0009_alter_user_last_name_max_length','2025-05-16 07:07:36.623199'),(15,'auth','0010_alter_group_name_max_length','2025-05-16 07:07:36.635210'),(16,'auth','0011_update_proxy_permissions','2025-05-16 07:07:36.639213'),(17,'auth','0012_alter_user_first_name_max_length','2025-05-16 07:07:36.683253'),(18,'sessions','0001_initial','2025-05-16 07:07:36.707275'),(19,'cars','0001_initial','2025-05-21 01:15:44.808486'),(20,'cars','0002_alter_cardata_options_and_more','2025-05-21 01:15:44.810489'),(21,'token_blacklist','0001_initial','2025-05-21 01:15:50.597437'),(22,'token_blacklist','0002_outstandingtoken_jti_hex','2025-05-21 01:15:50.614452'),(23,'token_blacklist','0003_auto_20171017_2007','2025-05-21 01:15:50.622460'),(24,'token_blacklist','0004_auto_20171017_2013','2025-05-21 01:15:50.674507'),(25,'token_blacklist','0005_remove_outstandingtoken_jti','2025-05-21 01:15:50.716545'),(26,'token_blacklist','0006_auto_20171017_2113','2025-05-21 01:15:50.731559'),(27,'token_blacklist','0007_auto_20171017_2214','2025-05-21 01:15:50.867745'),(28,'token_blacklist','0008_migrate_to_bigautofield','2025-05-21 01:15:51.195044'),(29,'token_blacklist','0010_fix_migrate_to_bigautofield','2025-05-21 01:15:51.202050'),(30,'token_blacklist','0011_linearizes_history','2025-05-21 01:15:51.203051'),(31,'token_blacklist','0012_alter_outstandingtoken_user','2025-05-21 01:15:51.209057'),(32,'cars','0003_alter_brand_id_alter_cardata_id_and_more','2025-05-25 01:48:05.216258');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-27 13:02:14
