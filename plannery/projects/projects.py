PROJECTS_FILE = "data/projects.txt"      # Lokasi file data proyek
MEMBERS_FILE = "data/project_members.txt"  # Lokasi file data anggota proyek

def read_projects():
    """
    Membaca data proyek dari file dan mengembalikannya
    dalam bentuk list berisi dictionary.
    """
    projects = []  # Menyimpan daftar proyek

    # Membuka file proyek dalam mode baca
    with open(PROJECTS_FILE, "r") as file:
        lines = file.readlines()  # Membaca seluruh baris file

        # Jika file kosong atau hanya berisi header
        if len(lines) <= 1:
            return projects

        headers = lines[0].strip().split("|")  # Mengambil header

        # Memproses setiap baris data proyek
        for line in lines[1:]:
            values = line.strip().split("|")
            project = {}

            # Memetakan nilai ke header
            for i in range(len(headers)):
                project[headers[i]] = values[i]

            # Konversi field tertentu ke integer
            project["project_id"] = int(project["project_id"])
            project["created_by"] = int(project["created_by"])

            projects.append(project)  # Menambahkan proyek ke list

    return projects  # Mengembalikan daftar proyek

def read_members():
    """
    Membaca data anggota proyek dari file dan
    mengembalikannya dalam bentuk list dictionary.
    """
    members = []  # Menyimpan daftar anggota proyek

    # Membuka file anggota proyek
    with open(MEMBERS_FILE, "r") as file:
        lines = file.readlines()

        # Jika file kosong atau hanya header
        if len(lines) <= 1:
            return members

        headers = lines[0].strip().split("|")  # Mengambil header

        # Memproses setiap baris anggota proyek
        for line in lines[1:]:
            values = line.strip().split("|")
            member = {}

            # Memetakan nilai ke header
            for i in range(len(headers)):
                member[headers[i]] = values[i]

            # Konversi ID ke integer
            member["project_id"] = int(member["project_id"])
            member["user_id"] = int(member["user_id"])

            members.append(member)  # Menambahkan anggota ke list

    return members  # Mengembalikan daftar anggota proyek

def get_next_project_id(projects):
    """
    Menentukan ID proyek berikutnya berdasarkan
    proyek yang sudah ada.
    """
    # Jika belum ada proyek
    if len(projects) == 0:
        return 1

    max_id = 0  # Menyimpan ID proyek terbesar

    # Mencari ID terbesar
    for project in projects:
        if project["project_id"] > max_id:
            max_id = project["project_id"]

    return max_id + 1  # Mengembalikan ID berikutnya

def is_project_owner(project_id, current_user):
    """
    Mengecek apakah pengguna saat ini adalah owner
    dari proyek tertentu.
    """
    members = read_members()  # Membaca data anggota proyek

    # Mengecek peran pengguna pada proyek
    for m in members:
        if (
            m["project_id"] == project_id and
            m["user_id"] == current_user["user_id"] and
            m["role"] == "owner"
        ):
            return True

    return False  # Bukan owner proyek

def generate_project_code(project_id):
    """
    Menghasilkan kode proyek berdasarkan ID proyek.
    """
    return "PRJ" + str(project_id)

def view_owned_projects(current_user):
    """
    Menampilkan daftar proyek yang dimiliki
    oleh pengguna saat ini.
    """
    projects = read_projects()  # Membaca data proyek
    found = False  # Penanda apakah proyek ditemukan

    # Menampilkan proyek yang dibuat oleh pengguna
    for p in projects:
        if p["created_by"] == current_user["user_id"]:
            print(
                f"- ID: {p['project_id']} | "
                f"Nama: {p['project_name']} | "
                f"Kode: {p['project_code']}"
            )
            found = True

    # Jika tidak ada proyek yang dimiliki
    if not found:
        print("Anda belum memiliki proyek.")

def create_project(current_user):
    """
    Membuat proyek baru dan menetapkan pengguna saat ini
    sebagai pemilik (owner) proyek.
    """
    projects = read_projects()  # Membaca data proyek
    members = read_members()    # Membaca data anggota proyek

    # Meminta dan memvalidasi nama proyek
    while True:
        project_name = input("\nMasukkan nama proyek: ").strip()
        
        if not project_name:
            print("\nNama proyek tidak boleh kosong.")
            continue
        
        # Nama proyek hanya boleh huruf, angka, dan spasi
        if not all(c.isalnum() or c.isspace() for c in project_name):
            print("\nNama proyek tidak boleh mengandung simbol.")
            continue
        
        break

    # Menentukan ID dan kode proyek baru
    project_id = get_next_project_id(projects)
    project_code = generate_project_code(project_id)

    # Menambahkan proyek baru ke daftar proyek
    projects.append({
        "project_id": project_id,
        "project_name": project_name,
        "project_code": project_code,
        "created_by": current_user["user_id"]
    })

    # Menyimpan data proyek ke file
    with open(PROJECTS_FILE, "w") as file:
        file.write("project_id|project_name|project_code|created_by\n")
        for p in projects:
            file.write(
                f"{p['project_id']}|{p['project_name']}|{p['project_code']}|{p['created_by']}\n"
            )

    # Menambahkan pengguna sebagai owner proyek
    members.append({
        "project_id": project_id,
        "user_id": current_user["user_id"],
        "role": "owner"
    })

    # Menyimpan data anggota proyek ke file
    with open(MEMBERS_FILE, "w") as file:
        file.write("project_id|user_id|role\n")
        for m in members:
            file.write(f"{m['project_id']}|{m['user_id']}|{m['role']}\n")

    print("\nProyek berhasil dibuat!")
    print("Kode proyek:", project_code)

def edit_project(current_user):
    """
    Mengubah nama proyek yang dimiliki oleh pengguna saat ini.
    """
    projects = read_projects()  # Membaca data proyek

    # Meminta ID proyek yang ingin diubah
    project_id = int(input("\nMasukkan ID proyek: "))

    # Mencari proyek yang sesuai dan dimiliki pengguna
    for p in projects:
        if p["project_id"] == project_id and p["created_by"] == current_user["user_id"]:
            while True:
                new_name = input("\nNama proyek baru: ").strip()
                
                if not new_name:
                    print("\nNama proyek tidak boleh kosong.")
                    continue
                
                # Validasi nama proyek baru
                if not all(c.isalnum() or c.isspace() for c in new_name):
                    print("\nNama proyek tidak boleh mengandung simbol.")
                    continue
                
                break
            
            p["project_name"] = new_name  # Memperbarui nama proyek

            # Menyimpan perubahan ke file
            with open(PROJECTS_FILE, "w") as file:
                file.write("project_id|project_name|project_code|created_by\n")
                for proj in projects:
                    file.write(
                        f"{proj['project_id']}|{proj['project_name']}|{proj['project_code']}|{proj['created_by']}\n"
                    )

            print("\nProyek berhasil diperbarui.")
            return

    print("\nProyek tidak ditemukan atau Anda bukan pemiliknya.")

def delete_project(current_user):
    """
    Menghapus proyek beserta seluruh anggota proyek
    jika pengguna saat ini adalah pemiliknya.
    """
    projects = read_projects()  # Membaca data proyek
    members = read_members()    # Membaca data anggota proyek

    # Meminta ID proyek yang ingin dihapus
    project_id = int(input("\nMasukkan ID proyek yang ingin dihapus: "))

    project_found = False
    new_projects = []  # Menyimpan proyek yang tidak dihapus

    # Memfilter proyek
    for p in projects:
        if p["project_id"] == project_id and p["created_by"] == current_user["user_id"]:
            project_found = True
        else:
            new_projects.append(p)

    # Jika proyek tidak ditemukan atau bukan milik pengguna
    if not project_found:
        print("\nProyek tidak ditemukan atau Anda bukan pemiliknya.")
        return

    new_members = []  # Menyimpan anggota selain proyek yang dihapus
    for m in members:
        if m["project_id"] != project_id:
            new_members.append(m)

    # Menyimpan data proyek yang tersisa
    with open(PROJECTS_FILE, "w") as file:
        file.write("project_id|project_name|project_code|created_by\n")
        for p in new_projects:
            file.write(
                f"{p['project_id']}|{p['project_name']}|{p['project_code']}|{p['created_by']}\n"
            )

    # Menyimpan data anggota proyek yang tersisa
    with open(MEMBERS_FILE, "w") as file:
        file.write("project_id|user_id|role\n")
        for m in new_members:
            file.write(f"{m['project_id']}|{m['user_id']}|{m['role']}\n")

    print("\nProyek berhasil dihapus.")

def is_project_member(project_id, current_user):
    """
    Mengecek apakah pengguna saat ini merupakan anggota (member)
    dari proyek tertentu.
    """
    members = read_members()  # Membaca data anggota proyek

    # Mengecek keanggotaan pengguna pada proyek
    for m in members:
        if (
            m["project_id"] == project_id and
            m["user_id"] == current_user["user_id"] and
            m["role"] == "member"
        ):
            return True

    return False  # Bukan anggota proyek

def view_joined_projects(current_user):
    """
    Menampilkan daftar proyek yang diikuti
    oleh pengguna saat ini sebagai anggota.
    """
    projects = read_projects()  # Membaca data proyek
    members = read_members()    # Membaca data anggota proyek

    found = False  # Penanda apakah ada proyek ditemukan

    # Mencari proyek yang diikuti pengguna
    for m in members:
        if m["user_id"] == current_user["user_id"] and m["role"] == "member":
            for p in projects:
                if p["project_id"] == m["project_id"]:
                    print(f"- ID: {p['project_id']} | Nama: {p['project_name']}")
                    found = True

    # Jika tidak ada proyek yang diikuti
    if not found:
        print("Anda belum bergabung ke proyek manapun.")

def join_project(current_user):
    """
    Menambahkan pengguna saat ini sebagai anggota
    ke dalam proyek berdasarkan kode proyek.
    """
    projects = read_projects()  # Membaca data proyek
    members = read_members()    # Membaca data anggota proyek

    # Meminta kode proyek dari pengguna
    code = input("\nMasukkan kode proyek: ")

    project = None

    # Mencari proyek berdasarkan kode
    for p in projects:
        if p["project_code"] == code:
            project = p
            break

    # Jika proyek tidak ditemukan
    if project is None:
        print("\nKode proyek tidak ditemukan.")
        return

    # Mengecek apakah pengguna sudah menjadi anggota
    for m in members:
        if (
            m["project_id"] == project["project_id"] and
            m["user_id"] == current_user["user_id"]
        ):
            print("\nAnda sudah menjadi anggota proyek ini.")
            return

    # Menambahkan pengguna sebagai anggota proyek
    members.append({
        "project_id": project["project_id"],
        "user_id": current_user["user_id"],
        "role": "member"
    })

    # Menyimpan perubahan data anggota proyek
    with open(MEMBERS_FILE, "w") as file:
        file.write("project_id|user_id|role\n")
        for m in members:
            file.write(f"{m['project_id']}|{m['user_id']}|{m['role']}\n")

    print("\nBerhasil bergabung ke proyek:", project["project_name"])

def leave_project(current_user):
    """
    Mengeluarkan pengguna dari proyek yang diikuti
    sebagai anggota (member).
    """
    members = read_members()  # Membaca data anggota proyek

    # Meminta ID proyek
    project_id = input("\nMasukkan ID proyek: ")

    # Validasi ID proyek harus berupa angka
    if not project_id.isdigit():
        print("\nID proyek harus berupa angka.")
        return
    
    project_id = int(project_id)

    new_members = []  # Menyimpan anggota yang tersisa
    left = False      # Penanda apakah pengguna berhasil keluar

    # Memfilter data anggota
    for m in members:
        if (
            m["project_id"] == project_id and
            m["user_id"] == current_user["user_id"] and
            m["role"] == "member"
        ):
            left = True
        else:
            new_members.append(m)

    # Jika pengguna bukan anggota proyek
    if not left:
        print("\nAnda bukan anggota proyek ini atau proyek tidak ditemukan.")
        return

    # Menyimpan data anggota proyek yang telah diperbarui
    with open(MEMBERS_FILE, "w") as file:
        file.write("project_id|user_id|role\n")
        for m in new_members:
            file.write(f"{m['project_id']}|{m['user_id']}|{m['role']}\n")

    print("\nAnda telah keluar dari proyek.")