import getpass

from auth_app.db.session import SessionLocal
from auth_app.repositories.users import UserRepository
from auth_app.security.passwords import hash_password

def main():
    username = input("Admin username: ").strip()
    if not username:
        print("Username is required")
        return

    password = getpass.getpass("Admin password: ").strip()
    if not password:
        print("Password is required")
        return

    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.get_by_username(username)

        if user is None:
            repo.create(
                username=username,
                password_hash=hash_password(password),
                is_admin=True,
            )
            print(f"Created admin: {username}")
        else:
            user.password_hash = hash_password(password)
            user.is_admin = True
            db.add(user)
            db.commit()
            print(f"Updated user to admin: {username}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
