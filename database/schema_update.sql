-- Mise à jour du schéma pour la messagerie avancée
USE mentorlink;

-- Ajouter colonnes pour fichiers/images dans les messages
ALTER TABLE message 
ADD COLUMN type_message ENUM('text', 'image', 'file') DEFAULT 'text' AFTER contenu,
ADD COLUMN fichier_url VARCHAR(255) AFTER type_message,
ADD COLUMN fichier_nom VARCHAR(255) AFTER fichier_url,
ADD COLUMN modifie BOOLEAN DEFAULT FALSE AFTER lu,
ADD COLUMN date_modification TIMESTAMP NULL AFTER modifie,
ADD COLUMN supprime BOOLEAN DEFAULT FALSE AFTER date_modification;

-- Index pour améliorer les performances
CREATE INDEX idx_conversation_messages ON message(conversation_id, created_at);
CREATE INDEX idx_message_expediteur ON message(expediteur_id);
CREATE INDEX idx_message_lu ON message(lu);

-- Made with Bob
