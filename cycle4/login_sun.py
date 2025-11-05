import mysql.connector

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="komodo"
)

cursor = db.cursor(dictionary=True)  # Return as dictionary, convenient for printing


def login():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    # Query user info
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if not user:
        print("Incorrect username or password!")
        return

    print("Login successful!")
    print_user_info(user)


def print_user_info(user):
    user_id = user['username']

    print("\n=== User Basic Information ===")
    for key, value in user.items():
        print(f"{key}: {value}")

    # Query user profile
    cursor.execute("SELECT * FROM user_profiles WHERE user_id = %s", (user_id,))
    profile = cursor.fetchone()
    if profile:
        print("\n=== User Profile Information ===")
        for key, value in profile.items():
            print(f"{key}: {value}")

    # Query user's organizations
    cursor.execute("""
                   SELECT o.org_name, o.org_type, om.role
                   FROM organization_members om
                            JOIN organizations o ON om.org_id = o.id
                   WHERE om.user_id = %s
                   """, (user_id,))
    orgs = cursor.fetchall()
    if orgs:
        print("\n=== User Organization Information ===")
        for org in orgs:
            print(f"{org['org_type']} - {org['org_name']} ({org['role']})")


if __name__ == "__main__":
    login()
    cursor.close()
    db.close()
