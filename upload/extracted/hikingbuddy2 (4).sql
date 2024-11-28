-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Waktu pembuatan: 20 Nov 2024 pada 05.58
-- Versi server: 10.4.21-MariaDB
-- Versi PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hikingbuddy2`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `Article`
--

CREATE TABLE `Article` (
  `ArticleId` char(36) NOT NULL,
  `ArticleTitle` longtext DEFAULT NULL,
  `ArticleData` longtext DEFAULT NULL,
  `ArticleDateRelease` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `articleconnect`
--

CREATE TABLE `articleconnect` (
  `ArticleId` char(36) NOT NULL,
  `UserId` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `Thread`
--

CREATE TABLE `Thread` (
  `ThreadId` char(36) NOT NULL,
  `ThreadDescription` varchar(255) DEFAULT NULL,
  `ThreadDateRelease` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `Thread`
--

INSERT INTO `Thread` (`ThreadId`, `ThreadDescription`, `ThreadDateRelease`) VALUES
('03266c91-6d77-4fd2-b9b2-cca2697389c8', 'testes', '2023-01-01'),
('36cae73e-e471-4af0-8ad8-961b07e83a4b', 'budi123', '2023-01-11'),
('5d613dc1-6d80-46c4-b7e4-30af40b37415', 'budi123', '2023-01-11'),
('d28f4427-4bd1-4b4c-bde3-99dea7f1d9d6', 'budi123', '2023-01-02'),
('d2cf2f05-3c1b-43e1-a095-91075d05ff3b', 'budi123', '2023-01-11');

-- --------------------------------------------------------

--
-- Struktur dari tabel `ThreadComment`
--

CREATE TABLE `ThreadComment` (
  `ThreadId` char(36) NOT NULL,
  `UserId` char(36) NOT NULL,
  `CommentData` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `ThreadLike`
--

CREATE TABLE `ThreadLike` (
  `ThreadId` char(36) NOT NULL,
  `UserId` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `ThreadPostHeader`
--

CREATE TABLE `ThreadPostHeader` (
  `ThreadId` char(36) NOT NULL,
  `UserId` char(36) NOT NULL,
  `TotalLike` int(10) DEFAULT NULL,
  `TotalComment` int(10) DEFAULT NULL,
  `TotalShare` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `ThreadPostHeader`
--

INSERT INTO `ThreadPostHeader` (`ThreadId`, `UserId`, `TotalLike`, `TotalComment`, `TotalShare`) VALUES
('03266c91-6d77-4fd2-b9b2-cca2697389c8', '9eff7896-d390-43bc-9ce3-573e106620f2', 0, 0, 0),
('36cae73e-e471-4af0-8ad8-961b07e83a4b', '9eff7896-d390-43bc-9ce3-573e106620f2', 0, 0, 0),
('5d613dc1-6d80-46c4-b7e4-30af40b37415', '9eff7896-d390-43bc-9ce3-573e106620f2', 0, 0, 0),
('d28f4427-4bd1-4b4c-bde3-99dea7f1d9d6', '9eff7896-d390-43bc-9ce3-573e106620f2', 0, 0, 0),
('d2cf2f05-3c1b-43e1-a095-91075d05ff3b', '9eff7896-d390-43bc-9ce3-573e106620f2', 0, 0, 0);

-- --------------------------------------------------------

--
-- Struktur dari tabel `ThreadShare`
--

CREATE TABLE `ThreadShare` (
  `ThreadId` char(36) NOT NULL,
  `UserId` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `Ticket`
--

CREATE TABLE `Ticket` (
  `TicketId` char(36) NOT NULL,
  `TicketName` text NOT NULL,
  `TicketCity` text NOT NULL,
  `TicketProvince` text NOT NULL,
  `DistanceToPeak` int(11) NOT NULL,
  `TicketPrice` int(11) NOT NULL,
  `Longitude` decimal(10,6) DEFAULT NULL,
  `Latitude` decimal(10,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `Ticket`
--

INSERT INTO `Ticket` (`TicketId`, `TicketName`, `TicketCity`, `TicketProvince`, `DistanceToPeak`, `TicketPrice`, `Longitude`, `Latitude`) VALUES
('0fcc6a2e-94af-4c5d-97b1-bef602f604de', 'Gunung Andong Magelang', 'Magelang', 'Jawa Tengah', 20, 62000, '7.388730', '110.371390'),
('42071a34-a88a-4eed-952e-b94302b6dd67', 'Gunung Merapi Boyolali', 'Boyolali', 'Jawa Tengah', 35, 100000, '-7.540718', '110.445724'),
('b3b6f01a-5795-4deb-bd71-329ef1ab571f', 'Gunung Lawu Tawangmangu', 'Tawangmangu', 'Jawa Tengah', 25, 50000, '-7.627188', '111.194007');

-- --------------------------------------------------------

--
-- Struktur dari tabel `TicketTransactionDetail`
--

CREATE TABLE `TicketTransactionDetail` (
  `TransactionId` char(36) NOT NULL,
  `TicketId` char(36) NOT NULL,
  `Quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `TicketTransactionDetail`
--

INSERT INTO `TicketTransactionDetail` (`TransactionId`, `TicketId`, `Quantity`) VALUES
('4fcc0a57-f2eb-4171-94dc-88667a821514', '0fcc6a2e-94af-4c5d-97b1-bef602f604de', 1),
('4fcc0a57-f2eb-4171-94dc-88667a821514', '42071a34-a88a-4eed-952e-b94302b6dd67', 2),
('87ba0a28-08a2-4d9d-942c-9957c93fd220', '0fcc6a2e-94af-4c5d-97b1-bef602f604de', 1),
('87ba0a28-08a2-4d9d-942c-9957c93fd220', '42071a34-a88a-4eed-952e-b94302b6dd67', 2);

-- --------------------------------------------------------

--
-- Struktur dari tabel `TicketTransactionHeader`
--

CREATE TABLE `TicketTransactionHeader` (
  `TransactionId` char(36) NOT NULL,
  `UserId` char(36) NOT NULL,
  `TotalAmount` int(11) NOT NULL,
  `PaymentMethod` text NOT NULL,
  `TicketPaymentDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `TicketTransactionHeader`
--

INSERT INTO `TicketTransactionHeader` (`TransactionId`, `UserId`, `TotalAmount`, `PaymentMethod`, `TicketPaymentDate`) VALUES
('4fcc0a57-f2eb-4171-94dc-88667a821514', '9eff7896-d390-43bc-9ce3-573e106620f2', 262000, 'Transfer', '2024-05-21'),
('87ba0a28-08a2-4d9d-942c-9957c93fd220', '9eff7896-d390-43bc-9ce3-573e106620f2', 262000, 'Transfer', '2024-05-22');

-- --------------------------------------------------------

--
-- Struktur dari tabel `Users`
--

CREATE TABLE `Users` (
  `UserId` char(36) NOT NULL,
  `UserFullname` varchar(255) DEFAULT NULL,
  `UserEmail` varchar(30) DEFAULT NULL,
  `UserPhone` varchar(10) DEFAULT NULL,
  `UserRole` varchar(20) NOT NULL,
  `UserPassword` varchar(30) DEFAULT NULL,
  `Username` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `Users`
--

INSERT INTO `Users` (`UserId`, `UserFullname`, `UserEmail`, `UserPhone`, `UserRole`, `UserPassword`, `Username`) VALUES
('9eff7896-d390-43bc-9ce3-573e106620f2', 'francis', 'francis@gmail.com', '082143121', 'Member', 'francis123', 'francis');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `Article`
--
ALTER TABLE `Article`
  ADD PRIMARY KEY (`ArticleId`);

--
-- Indeks untuk tabel `articleconnect`
--
ALTER TABLE `articleconnect`
  ADD PRIMARY KEY (`ArticleId`,`UserId`),
  ADD KEY `articleconnect_ibfk_2` (`UserId`);

--
-- Indeks untuk tabel `Thread`
--
ALTER TABLE `Thread`
  ADD PRIMARY KEY (`ThreadId`);

--
-- Indeks untuk tabel `ThreadComment`
--
ALTER TABLE `ThreadComment`
  ADD PRIMARY KEY (`ThreadId`,`UserId`),
  ADD KEY `threadcomment_ibfk_2` (`UserId`);

--
-- Indeks untuk tabel `ThreadLike`
--
ALTER TABLE `ThreadLike`
  ADD PRIMARY KEY (`ThreadId`,`UserId`),
  ADD KEY `threadlike_ibfk_2` (`UserId`);

--
-- Indeks untuk tabel `ThreadPostHeader`
--
ALTER TABLE `ThreadPostHeader`
  ADD PRIMARY KEY (`ThreadId`,`UserId`),
  ADD KEY `threadpostheader_ibfk_2` (`UserId`);

--
-- Indeks untuk tabel `ThreadShare`
--
ALTER TABLE `ThreadShare`
  ADD PRIMARY KEY (`ThreadId`,`UserId`),
  ADD KEY `threadshare_ibfk_2` (`UserId`);

--
-- Indeks untuk tabel `Ticket`
--
ALTER TABLE `Ticket`
  ADD PRIMARY KEY (`TicketId`);

--
-- Indeks untuk tabel `TicketTransactionDetail`
--
ALTER TABLE `TicketTransactionDetail`
  ADD PRIMARY KEY (`TransactionId`,`TicketId`),
  ADD KEY `TicketId` (`TicketId`);

--
-- Indeks untuk tabel `TicketTransactionHeader`
--
ALTER TABLE `TicketTransactionHeader`
  ADD PRIMARY KEY (`TransactionId`),
  ADD KEY `UserId` (`UserId`);

--
-- Indeks untuk tabel `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`UserId`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `articleconnect`
--
ALTER TABLE `articleconnect`
  ADD CONSTRAINT `articleconnect_ibfk_1` FOREIGN KEY (`ArticleId`) REFERENCES `Article` (`ArticleId`),
  ADD CONSTRAINT `articleconnect_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`);

--
-- Ketidakleluasaan untuk tabel `ThreadComment`
--
ALTER TABLE `ThreadComment`
  ADD CONSTRAINT `threadcomment_ibfk_1` FOREIGN KEY (`ThreadId`) REFERENCES `Thread` (`ThreadId`),
  ADD CONSTRAINT `threadcomment_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`);

--
-- Ketidakleluasaan untuk tabel `ThreadLike`
--
ALTER TABLE `ThreadLike`
  ADD CONSTRAINT `threadlike_ibfk_1` FOREIGN KEY (`ThreadId`) REFERENCES `Thread` (`ThreadId`),
  ADD CONSTRAINT `threadlike_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`);

--
-- Ketidakleluasaan untuk tabel `ThreadPostHeader`
--
ALTER TABLE `ThreadPostHeader`
  ADD CONSTRAINT `threadpostheader_ibfk_1` FOREIGN KEY (`ThreadId`) REFERENCES `Thread` (`ThreadId`),
  ADD CONSTRAINT `threadpostheader_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`);

--
-- Ketidakleluasaan untuk tabel `ThreadShare`
--
ALTER TABLE `ThreadShare`
  ADD CONSTRAINT `threadshare_ibfk_1` FOREIGN KEY (`ThreadId`) REFERENCES `Thread` (`ThreadId`),
  ADD CONSTRAINT `threadshare_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`);

--
-- Ketidakleluasaan untuk tabel `TicketTransactionDetail`
--
ALTER TABLE `TicketTransactionDetail`
  ADD CONSTRAINT `tickettransactiondetail_ibfk_1` FOREIGN KEY (`TransactionId`) REFERENCES `TicketTransactionHeader` (`TransactionId`),
  ADD CONSTRAINT `tickettransactiondetail_ibfk_2` FOREIGN KEY (`TicketId`) REFERENCES `Ticket` (`TicketId`);

--
-- Ketidakleluasaan untuk tabel `TicketTransactionHeader`
--
ALTER TABLE `TicketTransactionHeader`
  ADD CONSTRAINT `tickettransactionheader_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
