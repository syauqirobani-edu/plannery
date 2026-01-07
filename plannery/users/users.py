USERS_FILE = "data/users.txt"

def read_users():
    users = []

    with open(USERS_FILE, "r") as file:
        lines = file.readlines()

        if len(lines) <= 1:
            return users
        
        headers = lines[0].strip().split(",")

        for line in lines[1:]:
            values = line.strip().split(",")
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

def register():
    users = read_users()
    simbol = "!@#$%^&*(),.?\":{}|<>"

    username = input("Nama Pengguna: ")

    if not username: 
        print("Nama pengguna tidak boleh kosong!")
        return
    
    username = username.strip()

    for char in username:
        if char in simbol:
            print("Nama pengguna tidak boleh mengandung simbol!")
            return

    if username_exists(username):
        print("Nama pengguna sudah dipakai.")
        return
    
    password = input("Kata Sandi: ")

    if not password:
        print("Kata sandi tidak boleh kosong!")
        return

    if len (password) < 8 :
        print("Kata sandi minimal 8 karakter!")
        return

    if "," in password:
        print("Kata sandi tidak boleh mengandung koma")
        return

    # membuat variabel "confirm_password" di mana pengguna diharuskan untuk meng-input variabel "password" kembali

    # membuat function untuk membandingkan keduanya.

    new_id = get_next_user_id(users)

    users.append({
        "user_id": new_id,
        "username": username,
        "password": password
    })

    with open(USERS_FILE, "w") as file:
        file.write("user_id,username,password\n")
        for user in users:
            line = f"{user['user_id']},{user['username']},{user['password']}\n"
            file.write(line)

    
    print("Pengguna berhasil teregistrasi!")
    print("ID pengguna Anda alah: ", new_id)

def login():
    users = read_users()

    username = input("Nama Pengguna: ")
    password = input("Kata Sandi: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login berhasil!")
            return user

    print("Nama pengguna dan/atau kata sandi salah!")
    return None