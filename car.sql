-- phpMyAdmin SQL Dump
-- version 3.2.5
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 26, 2023 at 06:11 PM
-- Server version: 5.1.43
-- PHP Version: 5.3.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `testcase1`
--

-- --------------------------------------------------------

--
-- Table structure for table `testcase`
--

CREATE TABLE IF NOT EXISTS `car` (
  `id` bigint(10) unsigned NOT NULL AUTO_INCREMENT,
  `plate_number` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `date_in` date NOT NULL,
  `date_out` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf COLLATE=utf8_unicode_ci;


--
-- Dumping data for table `testcase`
--

