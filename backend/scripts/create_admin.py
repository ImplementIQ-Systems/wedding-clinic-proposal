"""
Cria o utilizador administrador. Corre uma única vez antes do deploy.

    cd backend/
    python scripts/create_admin.py admin@weddingclinic.pt senha_forte_aqui
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python scripts/create_admin.py <email> <password>")
        sys.exit(1)

    email, password = sys.argv[1], sys.argv[2]

    if len(password) < 8:
        print("Erro: password deve ter pelo menos 8 caracteres")
        sys.exit(1)

    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            print(f"Erro: já existe um utilizador com o email '{email}'")
            sys.exit(1)
        user = User(email=email, password_hash=hash_password(password))
        db.add(user)
        db.commit()
        print(f"Admin criado: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
