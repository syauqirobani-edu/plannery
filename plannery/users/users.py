USERS_FILE = "data/users.txt"

def read_users():
    users = []

    with open(USERS_FILE, "r") as file:
        lines = file.readlines()

        if len(lines) <= 1:
            return users
        
        headers = lines[0].strip().split("|")

        for line in lines[1:]:
            values = line.strip().split("|")
            user = {}

            for i in range(len(headers)):
                if headers[i] == "user_id":
                    user[headers[i]] = int(values[i])
                else:
                    user[headers[i]] = values[i]


            users.append(user)

    return users

def get_next_user_id(users):
    if len(users) == 0:
        return 1
    
    max_id = 0
    for user in users:
        user_id = int(user["user_id"])
        if user_id > max_id:
            max_id = user_id

    return max_id + 1

def username_exists(username):
    users = read_users()
    for user in users:
        if user["username"] == username:
            return True
    return False

def check_password(password, confirm_password):
    return password == confirm_password

"""D"""

def register():
    users = read_users()
    symbol = "!@#$%^&*().?\":{}|<>,"

    username = input("\nNama Pengguna: ")

    if not username: 
        print("\nNama pengguna tidak boleh kosong!")
        return
    
    username = username.strip()

    for char in username:
        if char in symbol:
            print("\nNama pengguna tidak boleh mengandung simbol!")
            return

    if username_exists(username):
        print("\nNama pengguna sudah dipakai.")
        return
    
    password = input("Kata Sandi: ")

    if not password:
        print("\nKata sandi tidak boleh kosong!")
        return

    if len (password) < 8 :
        print("\nKata sandi minimal 8 karakter!")
        return

    for char in password:
        if char in symbol:
            print("\nKata sandi tidak boleh mengandung simbol!")
            return

    confirm_password = input ("Konfirmasi kata sandi: ")

    if not check_password(password, confirm_password):
        print("\nKata sandi tidak sama!")
        return

    new_id = get_next_user_id(users)

    users.append({
        "user_id": new_id,
        "username": username,
        "password": password
    })

    with open(USERS_FILE, "w") as file:
        file.write("user_id|username|password\n")
        for user in users:
            line = f"{user['user_id']}|{user['username']}|{user['password']}\n"
            file.write(line)

    
    print("\nPengguna berhasil teregistrasi!")
    print("ID pengguna Anda adalah:", new_id)

def login():
    users = read_users()

    username = input("\nNama Pengguna: ").strip()
    password = input("Kata Sandi: ")

    for user in users:
        if user["username"].lower() == username.lower() and user["password"] == password:
            print("\nLogin berhasil!")
            return user

    print("\nNama pengguna dan/atau kata sandi salah!")
    return None