TASKS_FILE = "data/tasks.txt"
ASSIGNED_FILE = "data/assigned_members.txt"

def read_tasks():
    tasks = []
    with open(TASKS_FILE, "r") as file:
        lines = file.readlines()
        if len(lines) <= 1:
            return tasks

        headers = lines[0].strip().split(",")

        for line in lines[1:]:
            values = line.strip().split(",")
            task = {}

            for i in range(len(headers)):
                if headers[i] in ["task_id", "project_id", "created_by"]:
                    task[headers[i]] = int(values[i])
                else:
                    task[headers[i]] = values[i]

            tasks.append(task)
    return tasks

def read_assigned_members():
    assigns = []
    with open(ASSIGNED_FILE, "r") as file:
        lines = file.readlines()
        if len(lines) <= 1:
            return assigns

        headers = lines[0].strip().split(",")

        for line in lines[1:]:
            values = line.strip().split(",")
            assigns.append({
                "task_id": int(values[0]),
                "user_id": int(values[1])
            })
    return assigns

def view_tasks(project_id):
    tasks = read_tasks()
    found = False

    print("\n=== Daftar Tugas ===")
    for t in tasks:
        if t["project_id"] == project_id:
            print(
                f"ID: {t['task_id']} | {t['task_name']} | "
                f"Status: {t['status']} | Deadline: {t['due_date']}"
            )
            found = True

    if not found:
        print("Belum ada tugas.")

def view_task_detail(project_id):
    tasks = read_tasks()
    assigns = read_assigned_members()

    task_id = input("Masukkan ID tugas: ")

    if not task_id.isdigit():
        print("ID tugas harus berupa angka.")
        return

    task_id = int(task_id)

    task = None
    for t in tasks:
        if t["task_id"] == task_id and t["project_id"] == project_id:
            task = t
            break

    if task is None:
        print("Tugas tidak ditemukan.")
        return

    assigned_users = [
        a["user_id"] for a in assigns if a["task_id"] == task_id
    ]

    print("\n=== Detail Tugas ===")
    print(f"ID           : {task['task_id']}")
    print(f"Nama         : {task['task_name']}")
    print(f"Deskripsi    : {task['task_description']}")
    print(f"Status       : {task['status']}")
    print(f"Deadline     : {task['due_date']}")
    print(f"Dibuat oleh  : User ID {task['created_by']}")

    if assigned_users:
        print(f"Ditugaskan ke: User ID {assigned_users[0]}")
    else:
        print("Ditugaskan ke: (tidak ada)")

def create_task(project_id, current_user):
    tasks = read_tasks()
    assigns = read_assigned_members()

    task_name = input("Nama tugas: ")
    if not task_name.strip():
        print("Nama tugas tidak boleh kosong.")
        return
    if any(not c.isalnum() and not c.isspace() for c in task_name):
        print("Nama tugas tidak boleh berisi simbol.")
        return

    desc = input("Deskripsi tugas: ")
    if not desc.strip():
        print("Deskripsi tugas tidak boleh kosong.")
        return
    if any(not c.isalnum() and not c.isspace() for c in desc):
        print("Deskripsi tugas tidak boleh berisi simbol.")
        return

    due_date = input("Deadline (YYYY-MM-DD): ")
    
    task_name = task_name.strip()
    desc = desc.strip()
    due_date = due_date.strip()

    if not due_date:
        print("Deadline tidak valid.")
        return

    task_id = len(tasks) + 1

    tasks.append({
        "task_id": task_id,
        "project_id": project_id,
        "task_name": task_name,
        "task_description": desc,
        "status": "todo",
        "due_date": due_date,
        "created_by": current_user["user_id"]
    })

    assigned_user = input("Masukkan ID anggota yang ditugaskan: ")
    if not assigned_user.isdigit():
        print("ID anggota harus berupa angka.")
        return

    assigns.append({
        "task_id": task_id,
        "user_id": int(assigned_user)
    })

    with open(TASKS_FILE, "w") as f:
        f.write("task_id,project_id,task_name,task_description,status,due_date,created_by\n")
        for t in tasks:
            f.write(
                f"{t['task_id']},{t['project_id']},{t['task_name']},"
                f"{t['task_description']},{t['status']},"
                f"{t['due_date']},{t['created_by']}\n"
            )

    with open(ASSIGNED_FILE, "w") as f:
        f.write("task_id,user_id\n")
        for a in assigns:
            f.write(f"{a['task_id']},{a['user_id']}\n")

    print("Tugas berhasil dibuat.")

    task_id = len(tasks) + 1

    tasks.append({
        "task_id": task_id,
        "project_id": project_id,
        "task_name": task_name,
        "task_description": desc,
        "status": "todo",
        "due_date": due_date,
        "created_by": current_user["user_id"]
    })

    assigned_user = input("Masukkan ID anggota yang ditugaskan: ")

    if not assigned_user.isdigit():
        print("ID anggota harus berupa angka.")
        return

    assigns.append({
        "task_id": task_id,
        "user_id": int(assigned_user)
    })

    with open(TASKS_FILE, "w") as f:
        f.write("task_id,project_id,task_name,task_description,status,due_date,created_by\n")
        for t in tasks:
            f.write(
                f"{t['task_id']},{t['project_id']},{t['task_name']},"
                f"{t['task_description']},{t['status']},{t['due_date']},{t['created_by']}\n"
            )

    with open(ASSIGNED_FILE, "w") as f:
        f.write("task_id,user_id\n")
        for a in assigns:
            f.write(f"{a['task_id']},{a['user_id']}\n")

    print("Tugas berhasil dibuat.")


def view_my_tasks(project_id, current_user):
    tasks = read_tasks()
    assigns = read_assigned_members()

    my_task_ids = [
        a["task_id"] for a in assigns
        if a["user_id"] == current_user["user_id"]
    ]

    print("\n=== Tugas Saya ===")
    found = False
    for t in tasks:
        if t["task_id"] in my_task_ids and t["project_id"] == project_id:
            print(
                f"ID: {t['task_id']} | {t['task_name']} | "
                f"Status: {t['status']} | Deadline: {t['due_date']}"
            )
            found = True

    if not found:
        print("Anda belum memiliki tugas.")

def edit_task(project_id, current_user):
    tasks = read_tasks()

    task_id = input("Masukkan ID tugas yang ingin diedit: ")

    if not task_id.isdigit():
        print("ID tugas harus berupa angka.")
        return

    task_id = int(task_id)

    for t in tasks:
        if t["task_id"] == task_id and t["project_id"] == project_id:
            if t["created_by"] != current_user["user_id"]:
                print("Anda tidak memiliki izin untuk mengedit tugas ini.")
                return

            print("\nBiarkan kosong jika tidak ingin mengubah.")
            new_name = input(f"Nama tugas [{t['task_name']}]: ")
            new_desc = input(f"Deskripsi [{t['task_description']}]: ")
            new_due = input(f"Deadline [{t['due_date']}]: ")
            new_status = input(f"Status [{t['status']}]: ")

            if new_name.strip():
                t["task_name"] = new_name
            if new_desc.strip():
                t["task_description"] = new_desc
            if new_due.strip():
                t["due_date"] = new_due
            if new_status.strip():
                t["status"] = new_status

            with open(TASKS_FILE, "w") as f:
                f.write("task_id,project_id,task_name,task_description,status,due_date,created_by\n")
                for task in tasks:
                    f.write(
                        f"{task['task_id']},{task['project_id']},{task['task_name']},"
                        f"{task['task_description']},{task['status']},"
                        f"{task['due_date']},{task['created_by']}\n"
                    )

            print("Tugas berhasil diperbarui.")
            return

    print("Tugas tidak ditemukan.")

def delete_task(project_id, current_user):
    tasks = read_tasks()
    assigns = read_assigned_members()

    task_id = input("Masukkan ID tugas yang ingin dihapus: ")

    if not task_id.isdigit():
        print("ID tugas harus berupa angka.")
        return

    task_id = int(task_id)

    task_found = False
    new_tasks = []

    for t in tasks:
        if t["task_id"] == task_id and t["project_id"] == project_id:
            if t["created_by"] != current_user["user_id"]:
                print("Anda tidak memiliki izin untuk menghapus tugas ini.")
                return
            task_found = True
            continue
        new_tasks.append(t)

    if not task_found:
        print("Tugas tidak ditemukan.")
        return

    new_assigns = [
        a for a in assigns if a["task_id"] != task_id
    ]

    with open(TASKS_FILE, "w") as f:
        f.write("task_id,project_id,task_name,task_description,status,due_date,created_by\n")
        for t in new_tasks:
            f.write(
                f"{t['task_id']},{t['project_id']},{t['task_name']},"
                f"{t['task_description']},{t['status']},"
                f"{t['due_date']},{t['created_by']}\n"
            )

    with open(ASSIGNED_FILE, "w") as f:
        f.write("task_id,user_id\n")
        for a in new_assigns:
            f.write(f"{a['task_id']},{a['user_id']}\n")

    print("Tugas berhasil dihapus.")

def mark_task_done(project_id, current_user):
    tasks = read_tasks()
    assigns = read_assigned_members()

    task_id = input("Masukkan ID tugas yang ingin ditandai selesai: ")

    if not task_id.isdigit():
        print("ID tugas harus berupa angka.")
        return

    task_id = int(task_id)

    is_assigned = False
    for a in assigns:
        if a["task_id"] == task_id and a["user_id"] == current_user["user_id"]:
            is_assigned = True
            break

    if not is_assigned:
        print("Anda tidak ditugaskan pada tugas ini.")
        return

    task_found = False
    for t in tasks:
        if t["task_id"] == task_id and t["project_id"] == project_id:
            task_found = True

            if t["status"] == "done":
                print("Tugas ini sudah ditandai selesai.")
                return

            t["status"] = "done"
            break

    if not task_found:
        print("Tugas tidak ditemukan.")
        return

    with open(TASKS_FILE, "w") as f:
        f.write("task_id,project_id,task_name,task_description,status,due_date,created_by\n")
        for t in tasks:
            f.write(
                f"{t['task_id']},{t['project_id']},{t['task_name']},"
                f"{t['task_description']},{t['status']},{t['due_date']},{t['created_by']}\n"
            )

    print("Tugas berhasil ditandai sebagai SELESAI.")