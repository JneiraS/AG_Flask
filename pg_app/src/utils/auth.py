import hashlib
from pg_app.src.dao.membre_jury_dao import MembresJuryDAO


class Authentication:
    def __init__(self, password: str):
        self.password = password

    def hash_password(self) -> str:
        """
        Retourne le mot de passe haché avec la fonction de hachage SHA-256.
        """
        return hashlib.sha256(self.password.encode()).hexdigest()

    def check_password(self, hash_password: str) -> dict:  # type: ignore
        """
        Vérifie si le mot de passe enregistré correspond celui donné.
        :return: True si le mot de passe est correct, False sinon.
        """
        dao_membre: MembresJuryDAO = MembresJuryDAO()
        membre_jury_passwords: list[dict] | None = dao_membre.gethash(hash_password)

        for password in membre_jury_passwords:
            if password["mot_de_passe"] == self.hash_password():
                return password

    def delete_auth(self):
        """
        Supprime l'objet Authentication.
        """
        del self
