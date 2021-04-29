-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: 98.212.157.222    Database: locker
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

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
-- Table structure for table `locker`
--

DROP TABLE IF EXISTS `locker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `locker` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(32) NOT NULL,
  `pwd` varchar(128) NOT NULL,
  `customer_name` varchar(64) NOT NULL,
  `pickup_code` int NOT NULL,
  `deposit_code` int NOT NULL,
  `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin` tinyint NOT NULL,
  `admin_password` int DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `username` (`email`),
  UNIQUE KEY `pickup_code` (`pickup_code`),
  UNIQUE KEY `deposit_code` (`deposit_code`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locker`
--

LOCK TABLES `locker` WRITE;
/*!40000 ALTER TABLE `locker` DISABLE KEYS */;
INSERT INTO `locker` VALUES (24,'jpu3@illinois.edu','123456','Jake Pu',0,0,'2021-04-27 00:33:27',0,0),(26,'johnhd4@illinois.edu','12345','Jack Davis',557431,794796,'2021-04-26 22:20:26',0,0),(27,'jtnolan2@illinois.edu','illini','Josh Nolan',558289,682995,'2021-04-28 21:17:54',1,0),(28,'ece445lockeremail1@gmail.com','JoshN445','Mark Cuban',397075,702016,'2021-04-26 22:22:33',0,0),(29,'ece445lockeremail2@gmail.com','JoshN445','Selena Gomez',947330,417627,'2021-04-26 22:22:51',0,0),(30,'ece445lockeremail3@gmail.com','JoshN445','Ron Howard',425938,265874,'2021-04-26 22:23:38',0,0),(32,'ece445lockeremail5@gmail.com','JoshN445','Kevin Hart',444172,736284,'2021-04-26 22:29:02',0,0),(33,'bigjoe@fatones.com','12345','Big Joe',549490,141138,'2021-04-26 23:36:18',0,0),(35,'ben2','ben','ben',521549,454543,'2021-04-27 14:01:47',0,0),(38,'schu4@illinois.edu','password','Ali',306535,148139,'2021-04-27 14:20:59',0,0);
/*!40000 ALTER TABLE `locker` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-28 23:37:26
