-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-05-2026 a las 02:25:37
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
(4, 2, 'pipote', 50, 50, 0, '2026-05-14 22:47:56');

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
(3, 'Laboratorio de Física', 'mantenimiento', '2026-05-13 23:10:09');

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
(2, 2, 4, 4, 25, '2026-05-17 00:23:27', '2026-05-17 00:24:49', 'devuelto');

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
(1, 2, 4, '2026-05-13', '07:00:00', '07:45:00', 'cancelada', '2026-05-13 23:21:45'),
(2, 2, 4, '2026-05-13', '11:05:00', '11:50:00', 'cancelada', '2026-05-13 23:21:48'),
(3, 2, 5, '2026-05-13', '08:30:00', '09:15:00', 'cancelada', '2026-05-13 23:22:38'),
(4, 2, 5, '2026-05-13', '10:20:00', '11:05:00', 'cancelada', '2026-05-13 23:22:42'),
(5, 2, 5, '2026-05-14', '07:45:00', '08:30:00', 'cancelada', '2026-05-14 22:34:21'),
(6, 2, 5, '2026-05-14', '11:05:00', '11:50:00', 'cancelada', '2026-05-14 22:34:25');

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
(1, 5, 4, 25, 'aprobada', '2026-05-14 23:59:53', '2026-05-15 00:00:25', 1, NULL),
(2, 4, 4, 25, 'aprobada', '2026-05-17 00:22:39', '2026-05-17 00:23:27', 1, NULL);

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
(2, 'admin', 'admin123', 'admin', '2026-05-13 23:10:09'),
(3, 'maestro1', 'maestro123', 'maestro', '2026-05-13 23:10:09'),
(4, 'lucho', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'maestro', '2026-05-13 23:16:14'),
(5, 'lucha', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'maestro', '2026-05-13 23:22:13');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `laboratorios`
--
ALTER TABLE `laboratorios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `prestamos_activos`
--
ALTER TABLE `prestamos_activos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `solicitudes_prestamo`
--
ALTER TABLE `solicitudes_prestamo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
