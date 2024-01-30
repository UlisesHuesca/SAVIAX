-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: UlisesHuesca$default
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.22.04.1

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
-- Table structure for table `compras_proveedor_direcciones`
--

DROP TABLE IF EXISTS `compras_proveedor_direcciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras_proveedor_direcciones` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `domicilio` varchar(200) DEFAULT NULL,
  `contacto` varchar(50) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `clabe` varchar(20) DEFAULT NULL,
  `cuenta` varchar(20) DEFAULT NULL,
  `financiamiento` tinyint(1) DEFAULT NULL,
  `dias_credito` int unsigned DEFAULT NULL,
  `banco_id` bigint DEFAULT NULL,
  `distrito_id` bigint DEFAULT NULL,
  `estatus_id` bigint DEFAULT NULL,
  `nombre_id` bigint DEFAULT NULL,
  `estado_id` bigint DEFAULT NULL,
  `completo` tinyint(1) NOT NULL,
  `creado_por_id` bigint DEFAULT NULL,
  `email2` varchar(100) DEFAULT NULL,
  `email_2` varchar(100) DEFAULT NULL,
  `modified` date NOT NULL,
  `email_opt` varchar(100) DEFAULT NULL,
  `actualizado_por_id` bigint DEFAULT NULL,
  `modificado_fecha` date DEFAULT NULL,
  `telefono` varchar(31) DEFAULT NULL,
  `enviado_fecha` date DEFAULT NULL,
  `swift` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `compras_proveedor_completo_banco_id_05e0d3a3_fk_user_banco_id` (`banco_id`),
  KEY `compras_proveedor_co_distrito_id_82429f83_fk_user_dist` (`distrito_id`),
  KEY `compras_proveedor_co_estatus_id_1e82dd08_fk_compras_e` (`estatus_id`),
  KEY `compras_proveedor_co_nombre_id_cd0972a2_fk_compras_p` (`nombre_id`),
  KEY `compras_proveedor_direcciones_estado_id_8801c63f` (`estado_id`),
  KEY `compras_proveedor_di_creado_por_id_d97cad62_fk_user_prof` (`creado_por_id`),
  KEY `compras_proveedor_di_actualizado_por_id_609c6ba3_fk_user_prof` (`actualizado_por_id`),
  CONSTRAINT `compras_proveedor_co_distrito_id_82429f83_fk_user_dist` FOREIGN KEY (`distrito_id`) REFERENCES `user_distrito` (`id`),
  CONSTRAINT `compras_proveedor_co_estatus_id_1e82dd08_fk_compras_e` FOREIGN KEY (`estatus_id`) REFERENCES `compras_estatus_proveedor` (`id`),
  CONSTRAINT `compras_proveedor_co_nombre_id_cd0972a2_fk_compras_p` FOREIGN KEY (`nombre_id`) REFERENCES `compras_proveedor` (`id`),
  CONSTRAINT `compras_proveedor_completo_banco_id_05e0d3a3_fk_user_banco_id` FOREIGN KEY (`banco_id`) REFERENCES `user_banco` (`id`),
  CONSTRAINT `compras_proveedor_di_actualizado_por_id_609c6ba3_fk_user_prof` FOREIGN KEY (`actualizado_por_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `compras_proveedor_di_creado_por_id_d97cad62_fk_user_prof` FOREIGN KEY (`creado_por_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `compras_proveedor_di_estado_id_8801c63f_fk_compras_e` FOREIGN KEY (`estado_id`) REFERENCES `compras_estado` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=422 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras_proveedor_direcciones`
--
-- WHERE:  =telefono IS NOT NULL

