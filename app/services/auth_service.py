import hashlib

def hash_password(mot_de_passe):
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()

def verify_password(mot_de_passe, mot_de_passe_hash):
    return hash_password(mot_de_passe) == mot_de_passe_hash