USERS_FILE = "data/users.txt"

def load_users():
    users = {}
    
    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, password = line.split("|")
                users[username] = password
    except FileNotFoundError:
        pass
    
    return users

def save_user(username, password):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}|{password}\n") # TODO: Tambah enkripsi kalau bisa/sempet.

def register():
    users = load_users()

    print("\n=== Registrasi ===")
    username = input("Nama Pengguna: ").strip()

    if username in users:
        print("Nama pengguna sudah ada!")
        return None

    password = input("Kata Sandi: ").strip() # TODO: Tambah sensor kata sandi kalau bisa/sempet.

    save_user(username, password)
    print("Registrasi berhasil!")
    return username

def login():
    users = load_users()

    print("\n=== Login ===")
    username = input("Nama Pengguna: ").strip()
    password = input("Kata Sandi: ").strip()

    if username in users and users[username] == password:
        print("Login berhasil!")
        return username

    print("Nama pengguna dan/atau kata sandi tidak valid!")
    return None
