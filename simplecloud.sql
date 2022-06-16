-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 16, 2022 at 06:26 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `simplecloud`
--

-- --------------------------------------------------------

--
-- Table structure for table `file`
--

CREATE TABLE `file` (
  `id` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `file`
--

INSERT INTO `file` (`id`, `id_user`, `name`, `location`) VALUES
(23, 1, 'X-Jenis-Olahraga-Menyenangkan-untuk-Anjing-Peliharaan.jpg', 'file/X-Jenis-Olahraga-Menyenangkan-untuk-Anjing-Peliharaan2022-06-16 111602.jpg'),
(24, 1, '1545111808_contoh-pdf.pdf', 'file/1545111808_contoh-pdf2022-06-16 111610.pdf'),
(25, 2, 'Cat03.jpg', 'file/Cat032022-06-16 111623.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `share`
--

CREATE TABLE `share` (
  `id` int(11) NOT NULL,
  `id_user_origin` int(11) NOT NULL,
  `id_user_destination` int(11) NOT NULL,
  `id_file` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `share`
--

INSERT INTO `share` (`id`, `id_user_origin`, `id_user_destination`, `id_file`) VALUES
(2, 2, 1, 25);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`) VALUES
(1, 'han', 'han123'),
(2, 'han1', 'han123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `file`
--
ALTER TABLE `file`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `share`
--
ALTER TABLE `share`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user_origin` (`id_user_origin`),
  ADD KEY `id_user_destination` (`id_user_destination`),
  ADD KEY `id_file` (`id_file`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `file`
--
ALTER TABLE `file`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `share`
--
ALTER TABLE `share`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `file`
--
ALTER TABLE `file`
  ADD CONSTRAINT `file_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`);

--
-- Constraints for table `share`
--
ALTER TABLE `share`
  ADD CONSTRAINT `share_ibfk_1` FOREIGN KEY (`id_user_origin`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `share_ibfk_2` FOREIGN KEY (`id_user_destination`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `share_ibfk_3` FOREIGN KEY (`id_file`) REFERENCES `file` (`id`);
COMMIT;