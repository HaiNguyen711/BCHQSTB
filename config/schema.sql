CREATE DATABASE IF NOT EXISTS `military_citizen_db`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `military_citizen_db`;

CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(100) NOT NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `role` VARCHAR(50) NOT NULL DEFAULT 'staff',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_users_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `citizens` (
    `cccd` VARCHAR(32) NOT NULL,
    `full_name` VARCHAR(255) NOT NULL,
    `date_of_birth` DATE NULL,
    `gender` VARCHAR(20) NULL,
    `phone` VARCHAR(30) NULL,
    `ward` VARCHAR(255) NULL,
    `address` VARCHAR(255) NULL,
    `neighborhood` VARCHAR(255) NULL,
    `education_level` VARCHAR(255) NULL,
    `occupation` VARCHAR(255) NULL,
    `religion` VARCHAR(255) NULL,
    `ethnicity` VARCHAR(255) NULL,
    `photo_path` VARCHAR(500) NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`cccd`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `citizen_backgrounds` (
    `citizen_cccd` VARCHAR(32) NOT NULL,
    `father_name` VARCHAR(255) NULL,
    `father_occupation` VARCHAR(255) NULL,
    `father_phone` VARCHAR(30) NULL,
    `mother_name` VARCHAR(255) NULL,
    `mother_occupation` VARCHAR(255) NULL,
    `mother_phone` VARCHAR(30) NULL,
    `family_status` TEXT NULL,
    `criminal_record` TEXT NULL,
    `party_union_status` TEXT NULL,
    `notes` LONGTEXT NULL,
    `birth_registration_place` VARCHAR(255) NULL,
    `hometown` VARCHAR(255) NULL,
    `nationality` VARCHAR(255) NULL,
    `family_permanent_residence` VARCHAR(255) NULL,
    `current_residence` VARCHAR(255) NULL,
    `family_component` VARCHAR(255) NULL,
    `general_education_level` VARCHAR(255) NULL,
    `training_level` VARCHAR(255) NULL,
    `training_major` VARCHAR(255) NULL,
    `party_join_date` VARCHAR(50) NULL,
    `union_join_date` VARCHAR(50) NULL,
    `workplace_or_school` VARCHAR(255) NULL,
    `personal_situation` LONGTEXT NULL,
    `father_birth_date` VARCHAR(50) NULL,
    `father_status` VARCHAR(255) NULL,
    `mother_birth_date` VARCHAR(50) NULL,
    `mother_status` VARCHAR(255) NULL,
    `father_history_before_1975` LONGTEXT NULL,
    `father_history_after_1975` LONGTEXT NULL,
    `mother_history_before_1975` LONGTEXT NULL,
    `mother_history_after_1975` LONGTEXT NULL,
    `siblings_json` LONGTEXT NULL,
    `spouse_info` LONGTEXT NULL,
    `children_info` LONGTEXT NULL,
    `total_male_children` INT NULL,
    `total_female_children` INT NULL,
    `birth_order` VARCHAR(50) NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`citizen_cccd`),
    CONSTRAINT `fk_backgrounds_citizen`
        FOREIGN KEY (`citizen_cccd`) REFERENCES `citizens` (`cccd`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `citizen_health` (
    `citizen_cccd` VARCHAR(32) NOT NULL,
    `height` VARCHAR(50) NULL,
    `weight` VARCHAR(50) NULL,
    `vision` VARCHAR(100) NULL,
    `blood_pressure` VARCHAR(100) NULL,
    `health_type` VARCHAR(100) NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`citizen_cccd`),
    CONSTRAINT `fk_health_citizen`
        FOREIGN KEY (`citizen_cccd`) REFERENCES `citizens` (`cccd`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `military_service` (
    `citizen_cccd` VARCHAR(32) NOT NULL,
    `service_status` VARCHAR(50) NOT NULL DEFAULT 'CHUA_GOI',
    `health_check_date` DATE NULL,
    `health_result` VARCHAR(255) NULL,
    `enlistment_date` DATE NULL,
    `unit_name` VARCHAR(255) NULL,
    `position_name` VARCHAR(255) NULL,
    `note` LONGTEXT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`citizen_cccd`),
    KEY `idx_military_service_status` (`service_status`),
    CONSTRAINT `fk_military_citizen`
        FOREIGN KEY (`citizen_cccd`) REFERENCES `citizens` (`cccd`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
