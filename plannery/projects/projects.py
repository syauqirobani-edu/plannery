PROJECTS_FILE = "data/projects.txt"
MEMBERS_FILE = "data/project_members.txt"

def read_projects():
    projects = []

    with open(PROJECTS_FILE, "r") as file:
        lines = file.readlines()

        if len(lines) <= 1:
            return projects

        headers = lines[0].strip().split(",")

        for line in lines[1:]:
            values = line.strip().split(",")
            project = {}

            for i in range(len(headers)):
                project[headers[i]] = values[i]

            project["project_id"] = int(project["project_id"])
            project["created_by"] = int(project["created_by"])

            projects.append(project)

    return projects

def read_members():
    members = []

    with open(MEMBERS_FILE, "r") as file:
        lines = file.readlines()

        if len(lines) <= 1:
            return members

        headers = lines[0].strip().split(",")

        for line in lines[1:]:
            values = line.strip().split(",")
            member = {}

            for i in range(len(headers)):
                member[headers[i]] = values[i]

            member["project_id"] = int(member["project_id"])
            member["user_id"] = int(member["user_id"])

            members.append(member)

    return members

def get_next_project_id(projects):
    if len(projects) == 0:
        return 1

    max_id = 0
    for project in projects:
        if project["project_id"] > max_id:
            max_id = project["project_id"]

    return max_id + 1

def generate_project_code(project_id):
    return "PRJ" + str(project_id)

def view_owned_projects(current_user):
    projects = read_projects()

    print("\n=== Proyek yang Anda Miliki ===")
    found = False

    for p in projects:
        if p["created_by"] == current_user["user_id"]:
            print(f"- ID: {p['project_id']} | Nama: {p['project_name']} | Kode: {p['project_code']}")
            found = True

    if not found:
        print("Anda belum memiliki proyek.")

def create_project(current_user):
    projects = read_projects()
    members = read_members()

    project_name = input("Nama proyek: ")

    # TODO: Hapus whitespace tidak perlu dari variabel "project_name" inputan pengguna.
    # TODO: Tolak apabila variabel "project_name" kosong.
    # TODO: Tolak apabila variabel "project_name" hanya terdiri dari whitespace.
    # TODO: Tolak apabila variabel "project_name" mempunyai simbol.

    project_id = get_next_project_id(projects)
    project_code = generate_project_code(project_id)

    projects.append({
        "project_id": project_id,
        "project_name": project_name,
        "project_code": project_code,
        "created_by": current_user["user_id"]
    })

    with open(PROJECTS_FILE, "w") as file:
        file.write("project_id,project_name,project_code,created_by\n")
        for p in projects:
            file.write(f"{p['project_id']},{p['project_name']},{p['project_code']},{p['created_by']}\n")

    members.append({
        "project_id": project_id,
        "user_id": current_user["user_id"],
        "role": "owner"
    })

    with open(MEMBERS_FILE, "w") as file:
        file.write("project_id,user_id,role\n")
        for m in members:
            file.write(f"{m['project_id']},{m['user_id']},{m['role']}\n")

    print("Proyek berhasil dibuat!")
    print("Kode proyek:", project_code)

def edit_project(current_user):
    
    projects = read_projects()

    project_id = int(input("Masukkan ID proyek yang ingin diedit: "))

    for p in projects:
        if p["project_id"] == project_id and p["created_by"] == current_user["user_id"]:
            new_name = input("Nama proyek baru: ")

            # TODO: Hapus whitespace tidak perlu dari variabel "new_name" inputan pengguna.
            # TODO: Tolak apabila variabel "new_name" kosong.
            # TODO: Tolak apabila variabel "new_name" hanya terdiri dari whitespace.
            # TODO: Tolak apabila variabel "new_name" mempunyai simbol.
            p["project_name"] = new_name

            with open(PROJECTS_FILE, "w") as file:
                file.write("project_id,project_name,project_code,created_by\n")
                for proj in projects:
                    file.write(
                        f"{proj['project_id']},{proj['project_name']},{proj['project_code']},{proj['created_by']}\n"
                    )

            print("Proyek berhasil diperbarui.")
            return

    print("Proyek tidak ditemukan atau Anda bukan pemiliknya.")

def delete_project(current_user):
    projects = read_projects()
    members = read_members()

    project_id = int(input("Masukkan ID proyek yang ingin dihapus: "))

    project_found = False
    new_projects = []

    for p in projects:
        if p["project_id"] == project_id and p["created_by"] == current_user["user_id"]:
            project_found = True
        else:
            new_projects.append(p)

    if not project_found:
        print("Proyek tidak ditemukan atau Anda bukan pemiliknya.")
        return

    new_members = []
    for m in members:
        if m["project_id"] != project_id:
            new_members.append(m)

    with open(PROJECTS_FILE, "w") as file:
        file.write("project_id,project_name,project_code,created_by\n")
        for p in new_projects:
            file.write(f"{p['project_id']},{p['project_name']},{p['project_code']},{p['created_by']}\n")

    with open(MEMBERS_FILE, "w") as file:
        file.write("project_id,user_id,role\n")
        for m in new_members:
            file.write(f"{m['project_id']},{m['user_id']},{m['role']}\n")

    print("Proyek berhasil dihapus.")

def view_joined_projects(current_user):
    projects = read_projects()
    members = read_members()

    print("\n=== Proyek yang Anda Ikuti ===")
    found = False

    for m in members:
        if m["user_id"] == current_user["user_id"] and m["role"] == "member":
            for p in projects:
                if p["project_id"] == m["project_id"]:
                    print(f"- ID: {p['project_id']} | Nama: {p['project_name']}")
                    found = True

    if not found:
        print("Anda belum bergabung ke proyek manapun.")

def join_project(current_user):
    projects = read_projects()
    members = read_members()

    code = input("Masukkan kode proyek: ")

    project = None
    for p in projects:
        if p["project_code"] == code:
            project = p
            break

    if project is None:
        print("Kode proyek tidak ditemukan.")
        return

    for m in members:
        if m["project_id"] == project["project_id"] and m["user_id"] == current_user["user_id"]:
            print("Anda sudah menjadi anggota proyek ini.")
            return

    members.append({
        "project_id": project["project_id"],
        "user_id": current_user["user_id"],
        "role": "member"
    })

    with open(MEMBERS_FILE, "w") as file:
        file.write("project_id,user_id,role\n")
        for m in members:
            file.write(f"{m['project_id']},{m['user_id']},{m['role']}\n")

    print("Berhasil bergabung ke proyek:", project["project_name"])

def leave_project(current_user):
    members = read_members()

    project_id = int(input("Masukkan ID proyek yang ingin ditinggalkan: "))

    new_members = []
    left = False

    for m in members:
        if m["project_id"] == project_id and m["user_id"] == current_user["user_id"] and m["role"] == "member":
            left = True
        else:
            new_members.append(m)

    if not left:
        print("Anda bukan anggota proyek ini atau proyek tidak ditemukan.")
        return

    with open(MEMBERS_FILE, "w") as file:
        file.write("project_id,user_id,role\n")
        for m in new_members:
            file.write(f"{m['project_id']},{m['user_id']},{m['role']}\n")

    print("Anda telah keluar dari proyek.")