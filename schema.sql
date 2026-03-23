CREATE DATABASE IF NOT EXISTS military_citizen_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE military_citizen_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS citizens (
    cccd VARCHAR(20) NOT NULL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) DEFAULT '',
    phone VARCHAR(20) DEFAULT '',
    ward VARCHAR(100) DEFAULT '',
    address VARCHAR(255) DEFAULT '',
    neighborhood VARCHAR(255) DEFAULT '',
    education_level VARCHAR(100) DEFAULT '',
    occupation VARCHAR(255) DEFAULT '',
    religion VARCHAR(100) DEFAULT '',
    ethnicity VARCHAR(100) DEFAULT '',
    photo_path VARCHAR(500) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS citizen_backgrounds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    citizen_cccd VARCHAR(20) NOT NULL UNIQUE,
    father_name VARCHAR(255) DEFAULT '',
    father_birth_date VARCHAR(20) DEFAULT '',
    father_status VARCHAR(20) DEFAULT '',
    father_occupation VARCHAR(255) DEFAULT '',
    father_phone VARCHAR(20) DEFAULT '',
    father_history_before_1975 LONGTEXT NULL,
    father_history_after_1975 LONGTEXT NULL,
    mother_name VARCHAR(255) DEFAULT '',
    mother_birth_date VARCHAR(20) DEFAULT '',
    mother_status VARCHAR(20) DEFAULT '',
    mother_occupation VARCHAR(255) DEFAULT '',
    mother_phone VARCHAR(20) DEFAULT '',
    mother_history_before_1975 LONGTEXT NULL,
    mother_history_after_1975 LONGTEXT NULL,
    siblings_json LONGTEXT NULL,
    family_status VARCHAR(255) DEFAULT '',
    criminal_record VARCHAR(255) DEFAULT '',
    party_union_status VARCHAR(255) DEFAULT '',
    notes LONGTEXT NULL,
    birth_registration_place VARCHAR(255) DEFAULT '',
    hometown VARCHAR(255) DEFAULT '',
    nationality VARCHAR(100) DEFAULT '',
    family_permanent_residence VARCHAR(255) DEFAULT '',
    current_residence VARCHAR(255) DEFAULT '',
    family_component VARCHAR(255) DEFAULT '',
    general_education_level VARCHAR(100) DEFAULT '',
    training_level VARCHAR(100) DEFAULT '',
    training_major VARCHAR(255) DEFAULT '',
    party_join_date VARCHAR(20) DEFAULT '',
    union_join_date VARCHAR(20) DEFAULT '',
    workplace_or_school VARCHAR(255) DEFAULT '',
    personal_situation LONGTEXT NULL,
    spouse_info VARCHAR(255) DEFAULT '',
    children_info VARCHAR(255) DEFAULT '',
    total_male_children INT NULL,
    total_female_children INT NULL,
    birth_order VARCHAR(20) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_background_citizen
        FOREIGN KEY (citizen_cccd) REFERENCES citizens (cccd)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS citizen_health (
    id INT AUTO_INCREMENT PRIMARY KEY,
    citizen_cccd VARCHAR(20) NOT NULL UNIQUE,
    height VARCHAR(20) DEFAULT '',
    weight VARCHAR(20) DEFAULT '',
    vision VARCHAR(50) DEFAULT '',
    blood_pressure VARCHAR(50) DEFAULT '',
    health_type VARCHAR(100) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_health_citizen
        FOREIGN KEY (citizen_cccd) REFERENCES citizens (cccd)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS military_service (
    id INT AUTO_INCREMENT PRIMARY KEY,
    citizen_cccd VARCHAR(20) NOT NULL UNIQUE,
    service_status VARCHAR(50) NOT NULL DEFAULT 'CHUA_GOI',
    health_check_date DATE NULL,
    health_result VARCHAR(255) DEFAULT '',
    enlistment_date DATE NULL,
    unit_name VARCHAR(255) DEFAULT '',
    position_name VARCHAR(255) DEFAULT '',
    note TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_military_citizen
        FOREIGN KEY (citizen_cccd) REFERENCES citizens (cccd)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_citizens_full_name ON citizens (full_name);
CREATE INDEX idx_citizens_phone ON citizens (phone);
CREATE INDEX idx_citizens_ward ON citizens (ward);
CREATE INDEX idx_military_status ON military_service (service_status);

-- Create application users and grant permissions in environment-specific
-- deployment scripts instead of storing credentials in version control.
