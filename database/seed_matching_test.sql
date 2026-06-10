-- Données de test pour le module matching (à exécuter après schema.sql)
USE mentorlink;

DELETE FROM matching;
DELETE FROM disponibilite;
DELETE FROM competence;
DELETE FROM utilisateur;

INSERT INTO utilisateur (id, nom, prenom, email, telephone, mot_de_passe, filiere, niveau, bio) VALUES
(1, 'Koffi', 'Aline', 'aline@test.bj', '90000001', 'hash', 'GL', 'L2', 'Étudiante en GL, besoin d''aide en algo.'),
(2, 'Dossou', 'Marc', 'marc@test.bj', '90000002', 'hash', 'GL', 'L3', 'Bon niveau en algorithmique et Python.'),
(3, 'Agbessi', 'Sarah', 'sarah@test.bj', '90000003', 'hash', 'IA', 'L2', 'Spécialiste machine learning.');

INSERT INTO competence (utilisateur_id, matiere, type) VALUES
(1, 'Algorithmes', 'faible'),
(1, 'Python', 'faible'),
(1, 'HTML', 'fort'),
(2, 'Algorithmes', 'fort'),
(2, 'Python', 'fort'),
(2, 'Base de données', 'fort'),
(3, 'Python', 'fort'),
(3, 'Machine Learning', 'fort');

INSERT INTO disponibilite (utilisateur_id, jour, heure_debut, heure_fin) VALUES
(1, 'Lundi', '14:00:00', '16:00:00'),
(1, 'Mercredi', '10:00:00', '12:00:00'),
(2, 'Lundi', '14:00:00', '17:00:00'),
(2, 'Vendredi', '09:00:00', '11:00:00'),
(3, 'Mardi', '15:00:00', '17:00:00');
