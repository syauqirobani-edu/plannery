TASKS_FILE = "data/tasks.txt"              # Lokasi file data tugas
ASSIGNED_FILE = "data/assigned_members.txt"  # Lokasi file data penugasan anggota


def read_tasks():
    """
    Membaca data tugas dari file dan mengembalikannya
    dalam bentuk list berisi dictionary.
    """
    tasks = []  # Menyimpan daftar tugas

    # Membuka file tugas
    with open(TASKS_FILE, "r") as file:
        lines = file.readlines()

        # Jika file kosong atau hanya berisi header
        if len(lines) <= 1:
            return tasks

        headers = lines[0].strip().split("|")  # Mengambil header

        # Memproses setiap baris data tugas
        for line in lines[1:]:
            values = line.strip().split("|")
            task = {}

            # Memetakan nilai ke header dan konversi tipe data tertentu
            for i in range(len(headers)):
                if headers[i] in ["task_id", "project_id", "created_by"]:
                    task[headers[i]] = int(values[i])
                else:
                    task[headers[i]] = values[i]

            tasks.append(task)  # Menambahkan tugas ke list

    return tasks  # Mengembalikan daftar tugas


def read_assigned_members():
    """
    Membaca data penugasan anggota ke tugas
    dan mengembalikannya dalam bentuk list dictionary.
    """
    assigns = []  # Menyimpan daftar penugasan

    # Membuka file penugasan anggota
    with open(ASSIGNED_FILE, "r") as file:
        lines = file.readlines()

        # Jika file kosong atau hanya berisi header
        if len(lines) <= 1:
            return assigns

        # Memproses setiap baris penugasan
        for line in lines[1:]:
            values = line.strip().split("|")
            assigns.append({
                "task_id": int(values[0]),
                "user_id": int(values[1])
            })

    return assigns  # Mengembalikan daftar penugasan


def view_tasks(project_id):
    """
    Menampilkan daftar tugas berdasarkan ID proyek.
    """
    tasks = read_tasks()  # Membaca data tugas
    found = False         # Penanda apakah tugas ditemukan

    # Menampilkan tugas yang sesuai dengan proyek
    for t in tasks:
        if t["project_id"] == project_id:
            print(
                f"ID: {t['task_id']} | {t['task_name']} | "
                f"Status: {t['status']} | Deadline: {t['due_date']}"
            )
            found = True

    # Jika tidak ada tugas
    if not found:
        print("Belum ada tugas.")


def view_task_detail(project_id):
    """
    Menampilkan detail lengkap dari satu tugas
    berdasarkan ID tugas dan ID proyek.
    """
    tasks = read_tasks()            # Membaca data tugas
    assigns = read_assigned_members()  # Membaca data penugasan

    # Meminta ID tugas
    task_id = input("\nMasukkan ID tugas: ")

    # Validasi ID tugas harus berupa angka
    if not task_id.isdigit():
        print("\nID tugas harus berupa angka.")
        return

    task_id = int(task_id)

    task = None

    # Mencari tugas berdasarkan ID tugas dan proyek
    for t in tasks:
        if t["task_id"] == task_id and t["project_id"] == project_id:
            task = t
            break

    # Jika tugas tidak ditemukan
    if task is None:
        print("\nTugas tidak ditemukan.")
        return

    # Mengambil daftar user yang ditugaskan
    assigned_users = [
        a["user_id"] for a in assigns if a["task_id"] == task_id
    ]

    # Menampilkan detail tugas
    print("\n========== Detail Tugas ==========")
    print(f"ID           : {task['task_id']}")
    print(f"Nama         : {task['task_name']}")
    print(f"Deskripsi    : {task['task_description']}")
    print(f"Status       : {task['status']}")
    print(f"Deadline     : {task['due_date']}")
    print(f"Dibuat oleh  : User ID {task['created_by']}")

    # Menampilkan informasi penugasan
    if assigned_users:
        print(f"Ditugaskan ke: User ID {assigned_users[0]}")
    else:
        print("Ditugaskan ke: (tidak ada)")

    print("==================================")

def create_task(project_id, current_user):
    """
    Membuat tugas baru pada proyek tertentu dan
    menetapkan anggota proyek sebagai penanggung jawab tugas.
    """
    tasks = read_tasks()                 # Membaca data tugas
    assigns = read_assigned_members()    # Membaca data penugasan anggota

    # Meminta nama tugas
    task_name = input("\nNama tugas: ")
    if not task_name.strip():
        print("\nNama tugas tidak boleh kosong.")
        return

    # Validasi nama tugas tidak mengandung simbol
    if any(not c.isalnum() and not c.isspace() for c in task_name):
        print("\nNama tugas tidak boleh berisi simbol.")
        return

    # Meminta deskripsi tugas
    desc = input("Deskripsi tugas: ")
    if not desc.strip():
        print("\nDeskripsi tugas tidak boleh kosong.")
        return

    # Karakter '|' tidak diperbolehkan karena digunakan sebagai pemisah file
    if "|" in desc:
        print("\nDeskripsi tugas tidak boleh mengandung karakter '|'.")
        return

    # Meminta deadline tugas
    due_date = input("Deadline (Hari-Bulan-Tahun): ")

    # Membersihkan input
    task_name = task_name.strip()
    desc = desc.strip()
    due_date = due_date.strip()

    # Validasi deadline
    if not due_date:
        print("\nDeadline tidak valid.")
        return

    # Menentukan ID tugas baru
    task_id = len(tasks) + 1

    # Menambahkan tugas ke daftar tugas
    tasks.append({
        "task_id": task_id,
        "project_id": project_id,
        "task_name": task_name,
        "task_description": desc,
        "status": "todo",
        "due_date": due_date,
        "created_by": current_user["user_id"]
    })

    # Meminta ID anggota yang ditugaskan
    assigned_user = input("\nMasukkan ID anggota yang ditugaskan: ")
    if not assigned_user.isdigit():
        print("\nID anggota harus berupa angka.")
        return

    # Menyimpan data penugasan
    assigns.append({
        "task_id": task_id,
        "user_id": int(assigned_user)
    })

    # Menyimpan data tugas ke file
    with open(TASKS_FILE, "w") as f:
        f.write("task_id|project_id|task_name|task_description|status|due_date|created_by\n")
        for t in tasks:
            f.write(
                f"{t['task_id']}|{t['project_id']}|{t['task_name']}|"
                f"{t['task_description']}|{t['status']}|"
                f"{t['due_date']}|{t['created_by']}\n"
            )

    # Menyimpan data penugasan anggota
    with open(ASSIGNED_FILE, "w") as f:
        f.write("task_id|user_id\n")
        for a in assigns:
            f.write(f"{a['task_id']}|{a['user_id']}\n")

    print("\nTugas berhasil dibuat.")


def view_my_tasks(project_id, current_user):
    """
    Menampilkan daftar tugas yang ditugaskan
    kepada pengguna saat ini pada proyek tertentu.
    """
    tasks = read_tasks()              # Membaca data tugas
    assigns = read_assigned_members() # Membaca data penugasan

    # Mengambil ID tugas yang ditugaskan ke pengguna
    my_task_ids = [
        a["task_id"] for a in assigns
        if a["user_id"] == current_user["user_id"]
    ]

    found = False

    # Menampilkan tugas pengguna
    for t in tasks:
        if t["task_id"] in my_task_ids and t["project_id"] == project_id:
            print(
                f"ID: {t['task_id']} | {t['task_name']} | "
                f"Status: {t['status']} | Deadline: {t['due_date']}"
            )
            found = True

    # Jika tidak ada tugas
    if not found:
        print("Anda belum memiliki tugas.")


def edit_task(project_id, current_user):
    """
    Mengedit tugas dalam proyek tertentu.
    Hanya pembuat tugas yang memiliki izin untuk mengedit.
    """
    tasks = read_tasks()  # Membaca data tugas

    # Meminta ID tugas
    task_id = input("\nMasukkan ID tugas yang ingin diedit: ")

    # Validasi ID tugas
    if not task_id.isdigit():
        print("\nID tugas harus berupa angka.")
        return

    task_id = int(task_id)

    # Mencari tugas
    for t in tasks:
        if t["task_id"] == task_id and t["project_id"] == project_id:
            # Mengecek izin pengguna
            if t["created_by"] != current_user["user_id"]:
                print("\nAnda tidak memiliki izin untuk mengedit tugas ini.")
                return

            print("\nBiarkan kosong jika tidak ingin mengubah.")

            # Meminta data baru
            new_name = input("\nNama tugas: ")
            new_desc = input("Deskripsi: ")
            new_due = input("Deadline: ")
            new_status = input("Status: ")

            # Validasi deskripsi
            if new_desc.strip() == "":
                print("\nDeskripsi tugas tidak boleh kosong.")

            if "|" in new_desc:
                print("\nDeskripsi tugas tidak boleh mengandung karakter '|'.")

            # Memperbarui data tugas jika diisi
            if new_name.strip():
                t["task_name"] = new_name
            if new_desc.strip():
                t["task_description"] = new_desc
            if new_due.strip():
                t["due_date"] = new_due
            if new_status.strip():
                t["status"] = new_status

            # Menyimpan perubahan ke file
            with open(TASKS_FILE, "w") as f:
                f.write("task_id|project_id|task_name|task_description|status|due_date|created_by\n")
                for task in tasks:
                    f.write(
                        f"{task['task_id']}|{task['project_id']}|{task['task_name']}|"
                        f"{task['task_description']}|{task['status']}|"
                        f"{task['due_date']}|{task['created_by']}\n"
                    )

            print("\nTugas berhasil diperbarui.")
            return

    print("\nTugas tidak ditemukan.")

def delete_task(project_id, current_user):
    """
    Menghapus tugas dari proyek tertentu.
    Hanya pembuat tugas yang memiliki izin untuk menghapus.
    """
    tasks = read_tasks()                 # Membaca data tugas
    assigns = read_assigned_members()    # Membaca data penugasan anggota

    # Meminta ID tugas yang akan dihapus
    task_id = input("\nMasukkan ID tugas yang ingin dihapus: ")

    # Validasi ID tugas
    if not task_id.isdigit():
        print("\nID tugas harus berupa angka.")
        return

    task_id = int(task_id)

    task_found = False
    new_tasks = []  # Menyimpan daftar tugas selain yang dihapus

    # Memfilter tugas
    for t in tasks:
        if t["task_id"] == task_id and t["project_id"] == project_id:
            # Mengecek izin penghapusan
            if t["created_by"] != current_user["user_id"]:
                print("\nAnda tidak memiliki izin untuk menghapus tugas ini.")
                return
            task_found = True
            continue
        new_tasks.append(t)

    # Jika tugas tidak ditemukan
    if not task_found:
        print("\nTugas tidak ditemukan.")
        return

    # Menghapus data penugasan terkait tugas
    new_assigns = [
        a for a in assigns if a["task_id"] != task_id
    ]

    # Menyimpan data tugas terbaru
    with open(TASKS_FILE, "w") as f:
        f.write("task_id|project_id|task_name|task_description|status|due_date|created_by\n")
        for t in new_tasks:
            f.write(
                f"{t['task_id']}|{t['project_id']}|{t['task_name']}|"
                f"{t['task_description']}|{t['status']}|"
                f"{t['due_date']}|{t['created_by']}\n"
            )

    # Menyimpan data penugasan terbaru
    with open(ASSIGNED_FILE, "w") as f:
        f.write("task_id|user_id\n")
        for a in new_assigns:
            f.write(f"{a['task_id']}|{a['user_id']}\n")

    print("\nTugas berhasil dihapus.")


def mark_task_done(project_id, current_user):
    """
    Menandai tugas sebagai selesai (done).
    Hanya pengguna yang ditugaskan yang dapat menandai tugas selesai.
    """
    tasks = read_tasks()                 # Membaca data tugas
    assigns = read_assigned_members()    # Membaca data penugasan anggota

    # Meminta ID tugas
    task_id = input("\nMasukkan ID tugas yang ingin ditandai selesai: ")

    # Validasi ID tugas
    if not task_id.isdigit():
        print("\nID tugas harus berupa angka.")
        return

    task_id = int(task_id)

    # Mengecek apakah pengguna ditugaskan pada tugas ini
    is_assigned = False
    for a in assigns:
        if a["task_id"] == task_id and a["user_id"] == current_user["user_id"]:
            is_assigned = True
            break

    if not is_assigned:
        print("\nAnda tidak ditugaskan pada tugas ini.")
        return

    task_found = False

    # Mencari dan memperbarui status tugas
    for t in tasks:
        if t["task_id"] == task_id and t["project_id"] == project_id:
            task_found = True

            # Jika tugas sudah selesai
            if t["status"] == "done":
                print("\nTugas ini sudah ditandai selesai.")
                return

            t["status"] = "done"
            break

    # Jika tugas tidak ditemukan
    if not task_found:
        print("\nTugas tidak ditemukan.")
        return

    # Menyimpan perubahan status tugas
    with open(TASKS_FILE, "w") as f:
        f.write("task_id|project_id|task_name|task_description|status|due_date|created_by\n")
        for t in tasks:
            f.write(
                f"{t['task_id']}|{t['project_id']}|{t['task_name']}|"
                f"{t['task_description']}|{t['status']}|"
                f"{t['due_date']}|{t['created_by']}\n"
            )

    print("\nTugas berhasil ditandai sebagai SELESAI.")