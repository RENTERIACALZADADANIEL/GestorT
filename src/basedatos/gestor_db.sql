-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-06-2026 a las 01:48:15
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestor_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bloques_horario`
--

CREATE TABLE `bloques_horario` (
  `id` int(11) NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `es_receso` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `bloques_horario`
--

INSERT INTO `bloques_horario` (`id`, `hora_inicio`, `hora_fin`, `es_receso`) VALUES
(1, '07:00:00', '07:45:00', 0),
(2, '07:45:00', '08:30:00', 0),
(3, '08:30:00', '09:15:00', 0),
(4, '09:15:00', '10:00:00', 0),
(5, '10:20:00', '11:05:00', 0),
(6, '11:05:00', '11:50:00', 0),
(7, '11:50:00', '12:35:00', 0),
(8, '12:35:00', '13:20:00', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id` int(11) NOT NULL,
  `laboratorio_id` int(11) NOT NULL,
  `item_nombre` varchar(150) NOT NULL,
  `cantidad_total` int(11) NOT NULL,
  `cantidad_disponible` int(11) NOT NULL DEFAULT 0,
  `cantidad_prestada` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id`, `laboratorio_id`, `item_nombre`, `cantidad_total`, `cantidad_disponible`, `cantidad_prestada`, `created_at`) VALUES
(3, 2, 'computadoras', 45, 45, 0, '2026-05-14 22:33:20'),
(4, 2, 'pipote', 50, 50, 0, '2026-05-14 22:47:56'),
(5, 6, 'Hoja de corte', 4, 4, 0, '2026-05-24 03:12:27'),
(6, 7, 'cable ethernet', 15, 15, 0, '2026-06-04 00:38:53'),
(7, 6, 'serrucho', 3, 3, 0, '2026-06-04 23:19:11'),
(8, 9, 'proyector', 7, 7, 0, '2026-06-04 23:33:15'),
(9, 10, 'controol', 1, 1, 0, '2026-06-04 23:47:03');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `laboratorios`
--

CREATE TABLE `laboratorios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `estado` enum('disponible','mantenimiento') DEFAULT 'disponible',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `laboratorios`
--

INSERT INTO `laboratorios` (`id`, `nombre`, `estado`, `created_at`) VALUES
(1, 'Laboratorio de Computación', 'disponible', '2026-05-13 23:10:09'),
(2, 'Laboratorio de Química', 'disponible', '2026-05-13 23:10:09'),
(3, 'Laboratorio de Física', 'mantenimiento', '2026-05-13 23:10:09'),
(4, 'gimna', 'disponible', '2026-05-19 22:47:22'),
(5, 'sala5', 'disponible', '2026-05-19 22:58:41'),
(6, 'Laboratorio de carpinteria', 'disponible', '2026-05-24 03:11:26'),
(7, 'p1', 'disponible', '2026-06-04 00:38:28'),
(8, 'p2', 'disponible', '2026-06-04 23:19:23'),
(9, 'sala1', 'disponible', '2026-06-04 23:32:25'),
(10, 'lab22', 'disponible', '2026-06-04 23:46:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos_activos`
--

CREATE TABLE `prestamos_activos` (
  `id` int(11) NOT NULL,
  `solicitud_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `inventario_id` int(11) NOT NULL,
  `cantidad_prestada` int(11) NOT NULL,
  `fecha_prestamo` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_devolucion` timestamp NULL DEFAULT NULL,
  `estado` enum('prestado','devuelto') DEFAULT 'prestado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `prestamos_activos`
--

INSERT INTO `prestamos_activos` (`id`, `solicitud_id`, `usuario_id`, `inventario_id`, `cantidad_prestada`, `fecha_prestamo`, `fecha_devolucion`, `estado`) VALUES
(6, 7, 7, 7, 2, '2026-06-04 23:21:34', '2026-06-04 23:22:40', 'devuelto'),
(7, 8, 7, 4, 5, '2026-06-04 23:23:59', '2026-06-04 23:33:35', 'devuelto'),
(8, 9, 7, 6, 4, '2026-06-04 23:31:51', '2026-06-04 23:33:29', 'devuelto'),
(9, 11, 7, 6, 2, '2026-06-04 23:47:11', '2026-06-04 23:47:21', 'devuelto');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `laboratorio_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `estado` enum('activa','cancelada') DEFAULT 'activa',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id`, `laboratorio_id`, `usuario_id`, `fecha`, `hora_inicio`, `hora_fin`, `estado`, `created_at`) VALUES
(13, 7, 7, '2026-06-04', '07:00:00', '07:45:00', 'activa', '2026-06-04 23:34:05'),
(14, 7, 7, '2026-06-04', '12:35:00', '13:20:00', 'activa', '2026-06-04 23:34:10'),
(15, 4, 7, '2026-06-04', '07:00:00', '07:45:00', 'cancelada', '2026-06-04 23:45:19'),
(16, 4, 7, '2026-06-04', '10:20:00', '11:05:00', 'activa', '2026-06-04 23:45:24'),
(17, 4, 9, '2026-06-04', '07:00:00', '07:45:00', 'activa', '2026-06-04 23:47:56');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitudes_prestamo`
--

CREATE TABLE `solicitudes_prestamo` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `inventario_id` int(11) NOT NULL,
  `cantidad_solicitada` int(11) NOT NULL,
  `estado` enum('pendiente','aprobada','rechazada') DEFAULT 'pendiente',
  `fecha_solicitud` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_respuesta` timestamp NULL DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `comentario` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `solicitudes_prestamo`
--

INSERT INTO `solicitudes_prestamo` (`id`, `usuario_id`, `inventario_id`, `cantidad_solicitada`, `estado`, `fecha_solicitud`, `fecha_respuesta`, `admin_id`, `comentario`) VALUES
(7, 7, 7, 2, 'aprobada', '2026-06-04 23:21:09', '2026-06-04 23:21:34', 1, NULL),
(8, 7, 4, 5, 'aprobada', '2026-06-04 23:23:09', '2026-06-04 23:23:59', 1, NULL),
(9, 7, 6, 4, 'aprobada', '2026-06-04 23:31:16', '2026-06-04 23:31:51', 1, NULL),
(10, 7, 6, 8, 'rechazada', '2026-06-04 23:34:28', '2026-06-04 23:35:10', 1, 'Rechazada por administrador'),
(11, 7, 6, 2, 'aprobada', '2026-06-04 23:45:11', '2026-06-04 23:47:11', 1, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('admin','maestro') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `password`, `rol`, `created_at`) VALUES
(1, 'tester', '88fa0d759f845b47c044c2cd44e29082cf6fea665c30c146374ec7c8f3d699e3', 'admin', '2026-05-13 23:10:09'),
(7, 'maestro', '17756315ebd47b7110359fc7b168179bf6f2df3646fcc888bc8aa05c78b38ac1', 'maestro', '2026-06-04 23:20:37'),
(8, 'maestro1', '0449fd49186e15e1a167d543897e4a0f3f43c7aea17222d4a6db104481ce6c15', 'maestro', '2026-06-04 23:32:58'),
(9, 'maestro22', '65fe9217a22aee14bad28de8bdafb98a09c341b0be8656510415cdbb6a49c25b', 'maestro', '2026-06-04 23:46:43');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `bloques_horario`
--
ALTER TABLE `bloques_horario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `laboratorio_id` (`laboratorio_id`);

--
-- Indices de la tabla `laboratorios`
--
ALTER TABLE `laboratorios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `prestamos_activos`
--
ALTER TABLE `prestamos_activos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `solicitud_id` (`solicitud_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `inventario_id` (`inventario_id`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `laboratorio_id` (`laboratorio_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `solicitudes_prestamo`
--
ALTER TABLE `solicitudes_prestamo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `inventario_id` (`inventario_id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bloques_horario`
--
ALTER TABLE `bloques_horario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `laboratorios`
--
ALTER TABLE `laboratorios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `prestamos_activos`
--
ALTER TABLE `prestamos_activos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `solicitudes_prestamo`
--
ALTER TABLE `solicitudes_prestamo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`laboratorio_id`) REFERENCES `laboratorios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `prestamos_activos`
--
ALTER TABLE `prestamos_activos`
  ADD CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`solicitud_id`) REFERENCES `solicitudes_prestamo` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prestamos_ibfk_3` FOREIGN KEY (`inventario_id`) REFERENCES `inventario` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`laboratorio_id`) REFERENCES `laboratorios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `solicitudes_prestamo`
--
ALTER TABLE `solicitudes_prestamo`
  ADD CONSTRAINT `solicitudes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `solicitudes_ibfk_2` FOREIGN KEY (`inventario_id`) REFERENCES `inventario` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `solicitudes_ibfk_3` FOREIGN KEY (`admin_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
