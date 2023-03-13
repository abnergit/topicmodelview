-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: Discursos
-- ------------------------------------------------------
-- Server version	8.0.26-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `doc_doc`
--

DROP TABLE IF EXISTS `doc_doc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doc_doc` (
  `id` int NOT NULL,
  `doc_a` int NOT NULL,
  `doc_b` int NOT NULL,
  `score` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `doc_doc_idx1` (`doc_a`),
  KEY `doc_doc_idx2` (`doc_b`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doc_doc`
--

LOCK TABLES `doc_doc` WRITE;
/*!40000 ALTER TABLE `doc_doc` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_doc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doc_term`
--

DROP TABLE IF EXISTS `doc_term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doc_term` (
  `id` int NOT NULL,
  `doc` int NOT NULL,
  `term` int NOT NULL,
  `score` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `doc_term_idx1` (`doc`),
  KEY `doc_term_idx2` (`term`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doc_term`
--

LOCK TABLES `doc_term` WRITE;
/*!40000 ALTER TABLE `doc_term` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_term` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doc_topic`
--

DROP TABLE IF EXISTS `doc_topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doc_topic` (
  `id` int NOT NULL AUTO_INCREMENT,
  `doc` int NOT NULL,
  `topic` int NOT NULL,
  `score` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `doc_topic_idx1` (`doc`),
  KEY `doc_topic_idx2` (`topic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doc_topic`
--

LOCK TABLES `doc_topic` WRITE;
/*!40000 ALTER TABLE `doc_topic` DISABLE KEYS */;
/*!40000 ALTER TABLE `doc_topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `docs`
--

DROP TABLE IF EXISTS `docs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `docs` (
  `id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `docs`
--

LOCK TABLES `docs` WRITE;
/*!40000 ALTER TABLE `docs` DISABLE KEYS */;
/*!40000 ALTER TABLE `docs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `term_term`
--

DROP TABLE IF EXISTS `term_term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `term_term` (
  `id` int NOT NULL,
  `term_a` int NOT NULL,
  `term_b` int NOT NULL,
  `score` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `term_term_idx1` (`term_a`),
  KEY `term_term_idx2` (`term_b`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `term_term`
--

LOCK TABLES `term_term` WRITE;
/*!40000 ALTER TABLE `term_term` DISABLE KEYS */;
/*!40000 ALTER TABLE `term_term` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `terms`
--

DROP TABLE IF EXISTS `terms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `terms` (
  `id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `terms`
--

LOCK TABLES `terms` WRITE;
/*!40000 ALTER TABLE `terms` DISABLE KEYS */;
/*!40000 ALTER TABLE `terms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic_term`
--

DROP TABLE IF EXISTS `topic_term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic_term` (
  `id` int NOT NULL,
  `topic` int NOT NULL,
  `term` int NOT NULL,
  `score` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topic_term_idx1` (`topic`),
  KEY `topic_term_idx2` (`term`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_term`
--

LOCK TABLES `topic_term` WRITE;
/*!40000 ALTER TABLE `topic_term` DISABLE KEYS */;
/*!40000 ALTER TABLE `topic_term` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic_topic`
--

DROP TABLE IF EXISTS `topic_topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic_topic` (
  `id` int NOT NULL,
  `topic_a` int NOT NULL,
  `topic_b` int NOT NULL,
  `score` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topic_topic_idx1` (`topic_a`),
  KEY `topic_topic_idx2` (`topic_b`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_topic`
--

LOCK TABLES `topic_topic` WRITE;
/*!40000 ALTER TABLE `topic_topic` DISABLE KEYS */;
/*!40000 ALTER TABLE `topic_topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topics` (
  `id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */;
/*!40000 ALTER TABLE `topics` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-01  1:11:26
