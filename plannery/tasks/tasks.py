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

def create_task(project_id, current_user):
    tasks = read_tasks()
    assigns = read_assigned_members()

    task_name = input("Nama tugas: ")
    desc = input("Deskripsi tugas: ")
    due_date = input("Deadline (YYYY-MM-DD): ")

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

    print("Masukkan ID anggota (pisahkan dengan koma):")
    ids = input("> ").split(",")

    for uid in ids:
        assigns.append({
            "task_id": task_id,
            "user_id": int(uid.strip())
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

def submit_task():
    print("Fitur pengumpulan tugas masih dalam pengembangan (WIP).")