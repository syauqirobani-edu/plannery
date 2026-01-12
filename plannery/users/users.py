USERS_FILE = "data/users.txt"  # Lokasi file data pengguna

def read_users():
    """
    Membaca data pengguna dari file teks dan mengembalikannya
    dalam bentuk list berisi dictionary.

    Setiap baris merepresentasikan satu pengguna, dengan header
    sebagai kunci dictionary.
    """
    users = []  # Menyimpan daftar pengguna

    # Membuka file pengguna dalam mode baca
    with open(USERS_FILE, "r") as file:
        lines = file.readlines()  # Membaca seluruh baris dalam file

        # Jika file hanya berisi header atau kosong, kembalikan list kosong
        if len(lines) <= 1:
            return users
        
        # Mengambil header dari baris pertama
        headers = lines[0].strip().split("|")

        # Memproses setiap baris data pengguna
        for line in lines[1:]:
            values = line.strip().split("|")
            user = {}  # Dictionary untuk satu pengguna

            # Memetakan nilai ke header masing-masing
            for i in range(len(headers)):
                if headers[i] == "user_id":
                    user[headers[i]] = int(values[i])  # user_id disimpan sebagai integer
                else:
                    user[headers[i]] = values[i]  # Field lain disimpan sebagai string

            users.append(user)  # Menambahkan pengguna ke list

    return users  # Mengembalikan daftar pengguna


def get_next_user_id(users):
    """
    Menentukan ID pengguna berikutnya berdasarkan data pengguna yang ada.

    Jika belum ada pengguna, ID dimulai dari 1.
    """
    # Jika daftar pengguna kosong, kembalikan ID awal
    if len(users) == 0:
        return 1
    
    max_id = 0  # Menyimpan ID terbesar yang ditemukan

    # Mencari ID pengguna terbesar
    for user in users:
        user_id = int(user["user_id"])
        if user_id > max_id:
            max_id = user_id

    # Mengembalikan ID berikutnya
    return max_id + 1


def username_exists(username):
    """
    Mengecek apakah username sudah ada di data pengguna.

    Mengembalikan True jika username ditemukan, jika tidak False.
    """
    users = read_users()  # Membaca data pengguna dari file

    # Mengecek setiap pengguna
    for user in users:
        if user["username"] == username:
            return True

    return False  # Username tidak ditemukan


def check_password(password, confirm_password):
    """
    Memeriksa apakah password dan konfirmasi password sama.

    Mengembalikan True jika sama, jika tidak False.
    """
    return password == confirm_password

def register():
    """
    Melakukan proses pendaftaran pengguna baru.

    Fungsi ini akan memvalidasi nama pengguna dan kata sandi,
    lalu menyimpan data pengguna ke dalam file jika valid.
    """
    users = read_users()  # Membaca data pengguna yang sudah ada
    symbol = "!@#$%^&*().?\":{}|<>,"  # Daftar simbol yang tidak diperbolehkan

    # Meminta input nama pengguna
    username = input("\nNama Pengguna: ")

    # Validasi nama pengguna tidak boleh kosong
    if not username:
        print("\nNama pengguna tidak boleh kosong!")
        return
    
    username = username.strip()  # Menghapus spasi di awal dan akhir

    # Mengecek apakah nama pengguna mengandung simbol
    for char in username:
        if char in symbol:
            print("\nNama pengguna tidak boleh mengandung simbol!")
            return

    # Mengecek apakah nama pengguna sudah digunakan
    if username_exists(username):
        print("\nNama pengguna sudah dipakai.")
        return
    
    # Meminta input kata sandi
    password = input("Kata Sandi: ")

    # Validasi kata sandi tidak boleh kosong
    if not password:
        print("\nKata sandi tidak boleh kosong!")
        return

    # Validasi panjang kata sandi minimal 8 karakter
    if len(password) < 8:
        print("\nKata sandi minimal 8 karakter!")
        return

    # Mengecek apakah kata sandi mengandung simbol
    for char in password:
        if char in symbol:
            print("\nKata sandi tidak boleh mengandung simbol!")
            return

    # Meminta konfirmasi kata sandi
    confirm_password = input("Konfirmasi kata sandi: ")

    # Mengecek apakah kata sandi dan konfirmasi sama
    if not check_password(password, confirm_password):
        print("\nKata sandi tidak sama!")
        return

    # Menentukan ID pengguna baru
    new_id = get_next_user_id(users)

    # Menambahkan pengguna baru ke daftar pengguna
    users.append({
        "user_id": new_id,
        "username": username,
        "password": password
    })

    # Menyimpan seluruh data pengguna ke file
    with open(USERS_FILE, "w") as file:
        file.write("user_id|username|password\n")
        for user in users:
            line = f"{user['user_id']}|{user['username']}|{user['password']}\n"
            file.write(line)

    print("\nPengguna berhasil teregistrasi!")
    print("ID pengguna Anda adalah:", new_id)


def login():
    """
    Melakukan proses login pengguna.

    Fungsi ini akan mencocokkan nama pengguna dan kata sandi
    dengan data yang tersimpan.
    """
    users = read_users()  # Membaca data pengguna

    # Meminta input login
    username = input("\nNama Pengguna: ").strip()
    password = input("Kata Sandi: ")

    # Mencari kecocokan username dan password
    for user in users:
        if user["username"].lower() == username.lower() and user["password"] == password:
            print("\nLogin berhasil!")
            return user  # Mengembalikan data pengguna yang login

    # Jika tidak ditemukan kecocokan
    print("\nNama pengguna dan/atau kata sandi salah!")
    return None