from users.users import register, login

from projects.projects import (
    create_project,
    join_project,
    view_owned_projects,
    edit_project,
    delete_project,
    view_joined_projects,
    leave_project
)

from tasks.tasks import (
    view_tasks,
    create_task,
    view_my_tasks,
    submit_task
)

def task_menu_owner(project_id, current_user):
    while True:
        print("\n=== Menu Tugas (Pemilik) ===")
        view_tasks(project_id)

        print("\nMenu:")
        print("1. Buat Tugas")
        print("2. Edit Tugas")
        print("3. Hapus Tugas")
        print("4. Kembali")

        choice = input("Pilih menu: ")

        if choice == "1":
            create_task(project_id, current_user)

        elif choice == "2":
            print("Edit tugas masih dalam pengembangan (WIP).")

        elif choice == "3":
            print("Hapus tugas masih dalam pengembangan (WIP).")

        elif choice == "4":
            break

        else:
            print("Pilihan tidak valid.")


def task_menu_member(project_id, current_user):
    while True:
        print("\n=== Menu Tugas (Anggota) ===")
        view_my_tasks(project_id, current_user)

        print("\nMenu:")
        print("1. Submit Tugas")
        print("2. Kembali")

        choice = input("Pilih menu: ")

        if choice == "1":
            submit_task()

        elif choice == "2":
            break

        else:
            print("Pilihan tidak valid.")

def project_menu(current_user):
    while True:
        print("\n=== Menu Proyek ===")
        print("1. Daftar Proyek (status: Pemilik)")
        print("2. Daftar Proyek (status: Anggota)")
        print("3. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            while True:
                print("\n--- Daftar Proyek (status: Pemilik) ---")
                view_owned_projects(current_user)

                print("\nMenu:")
                print("1. Buka Proyek")
                print("2. Buat Proyek")
                print("3. Edit Proyek")
                print("4. Hapus Proyek")
                print("5. Kembali")

                sub_choice = input("Pilih menu: ")

                if sub_choice == "1":
                    try:
                        project_id = int(input("Masukkan ID proyek: "))
                        task_menu_owner(project_id, current_user)
                    except ValueError:
                        print("ID proyek harus berupa angka.")

                elif sub_choice == "2":
                    create_project(current_user)

                elif sub_choice == "3":
                    edit_project(current_user)

                elif sub_choice == "4":
                    delete_project(current_user)

                elif sub_choice == "5":
                    break

                else:
                    print("Pilihan tidak valid.")

        elif choice == "2":
            while True:
                print("\n--- Daftar Proyek (status: Anggota) ---")
                view_joined_projects(current_user)

                print("\nMenu:")
                print("1. Buka Proyek")
                print("2. Gabung Proyek")
                print("3. Keluar dari Proyek")
                print("4. Kembali")

                sub_choice = input("Pilih menu: ")

                if sub_choice == "1":
                    try:
                        project_id = int(input("Masukkan ID proyek: "))
                        task_menu_member(project_id, current_user)
                    except ValueError:
                        print("ID proyek harus berupa angka.")

                elif sub_choice == "2":
                    join_project(current_user)

                elif sub_choice == "3":
                    leave_project(current_user)

                elif sub_choice == "4":
                    break

                else:
                    print("Pilihan tidak valid.")

        elif choice == "3":
            print("Logout berhasil.")
            break

        else:
            print("Pilihan tidak valid.")

def main_menu():
    while True:
        print("\n=== Plannery ===")
        print("1. Registrasi")
        print("2. Login")
        print("3. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            register()

        elif choice == "2":
            user = login()
            if user is not None:
                project_menu(user)

        elif choice == "3":
            print("Terima kasih telah menggunakan Plannery.")
            break

        else:
            print("Pilihan tidak valid.")

main_menu()