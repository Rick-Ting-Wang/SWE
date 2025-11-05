import bcrypt
import getpass

def generate_hash():
    username = input("Please enter username: ")
    password = getpass.getpass("Please enter password (not shown when typing): ").encode("utf-8")

    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    print("\n✅ Hash generated successfully! Please copy the following result into the database:\n")
    print(f"Username: {username}")
    print(f"Password hash: {hashed}")
    print("\nYou can execute SQL like:")
    print(f"UPDATE users SET password_hash='{hashed}' WHERE username='{username}';")

if __name__ == "__main__":
    generate_hash()
