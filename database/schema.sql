CREATE DATABASE IF NOT EXISTS mentorlink;
USE mentorlink;

-- Table utilisateurs
CREATE TABLE utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    photo VARCHAR(255),
    filiere VARCHAR(50),
    niveau VARCHAR(20),
    bio TEXT,
    format_mentorat ENUM('presentiel', 'enligne', 'les_deux') DEFAULT 'les_deux',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table compétences
CREATE TABLE competence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    matiere VARCHAR(100) NOT NULL,
    type ENUM('fort', 'faible') NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
);

-- Table disponibilités
CREATE TABLE disponibilite (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    jour VARCHAR(20) NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
);

-- Table matching
CREATE TABLE matching (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_id INT NOT NULL,
    mentore_id INT NOT NULL,
    score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mentor_id) REFERENCES utilisateur(id),
    FOREIGN KEY (mentore_id) REFERENCES utilisateur(id)
);

-- Table conversations
CREATE TABLE conversation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur1_id INT NOT NULL,
    utilisateur2_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur1_id) REFERENCES utilisateur(id),
    FOREIGN KEY (utilisateur2_id) REFERENCES utilisateur(id)
);

-- Table messages
CREATE TABLE message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    expediteur_id INT NOT NULL,
    contenu TEXT NOT NULL,
    lu BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversation(id),
    FOREIGN KEY (expediteur_id) REFERENCES utilisateur(id)
);