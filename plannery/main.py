from users.users import register, login

from projects.projects import (
    is_project_owner,
    is_project_member,
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
    view_task_detail,
    create_task,
    view_my_tasks,
    edit_task,
    delete_task,
    mark_task_done
)


def task_menu_owner(project_id, current_user):
    """
    Menampilkan menu manajemen tugas untuk pemilik proyek.
    Pemilik dapat melihat, membuat, mengedit, dan menghapus tugas.
    """
    while True:
        print("\n============ Menu Tugas (Pemilik) ============")
        view_tasks(project_id)  # Menampilkan semua tugas dalam proyek
        print("==============================================")
        print("1. Lihat Detail Tugas")
        print("2. Buat Tugas")
        print("3. Edit Tugas")
        print("4. Hapus Tugas")
        print("5. Kembali")
        print("==============================================")

        choice = input("Pilih menu: ")

        if choice == "1":
            view_task_detail(project_id)
        elif choice == "2":
            create_task(project_id, current_user)
        elif choice == "3":
            edit_task(project_id, current_user)
        elif choice == "4":
            delete_task(project_id, current_user)
        elif choice == "5":
            break
        else:
            print("Pilihan tidak valid.")


def task_menu_member(project_id, current_user):
    """
    Menampilkan menu tugas untuk anggota proyek.
    Anggota hanya dapat melihat tugasnya dan menandai tugas selesai.
    """
    while True:
        print("\n============ Menu Tugas (Anggota) ============")
        view_my_tasks(project_id, current_user)  # Menampilkan tugas milik anggota

        print("==============================================")
        print("1. Lihat detail tugas")
        print("2. Tandai selesai")
        print("3. Kembali")

        choice = input("Pilih menu: ")

        if choice == "1":
            view_task_detail(project_id)
        elif choice == "2":
            mark_task_done(project_id, current_user)
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid.")


def project_menu(current_user):
    """
    Menu utama proyek setelah pengguna berhasil login.
    Pengguna dapat mengelola proyek sebagai pemilik atau anggota.
    """
    while True:
        print("\n=========== Menu Proyek ===========")
        print("1. Daftar Proyek (status: Pemilik)")
        print("2. Daftar Proyek (status: Anggota)")
        print("3. Logout")
        print("===================================")

        choice = input("Pilih menu: ")

        # Menu proyek sebagai pemilik
        if choice == "1":
            while True:
                print("\n=== Daftar Proyek (status: Pemilik) ===")
                view_owned_projects(current_user)

                print("=======================================")
                print("1. Buka Proyek")
                print("2. Buat Proyek")
                print("3. Edit Proyek")
                print("4. Hapus Proyek")
                print("5. Kembali")
                print("=======================================")

                sub_choice = input("Pilih menu: ")

                if sub_choice == "1":
                    try:
                        project_id = int(input("\nMasukkan ID proyek: "))

                        # Mengecek apakah pengguna adalah pemilik proyek
                        project = is_project_owner(project_id, current_user)
                        if project is False:
                            print("\nProyek tidak ditemukan atau Anda bukan pemiliknya.")
                        else:
                            task_menu_owner(project_id, current_user)
                    except ValueError:
                        print("\nID proyek harus berupa angka.")

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

        # Menu proyek sebagai anggota
        elif choice == "2":
            while True:
                print("\n=== Daftar Proyek (status: Anggota) ===")
                view_joined_projects(current_user)

                print("=======================================")
                print("1. Buka Proyek")
                print("2. Gabung Proyek")
                print("3. Keluar dari Proyek")
                print("4. Kembali")
                print("=======================================")

                sub_choice = input("Pilih menu: ")

                if sub_choice == "1":
                    try:
                        project_id = int(input("\nMasukkan ID proyek: "))

                        # Mengecek apakah pengguna adalah anggota proyek
                        project = is_project_member(project_id, current_user)
                        if project is False:
                            print("\nProyek tidak ditemukan atau Anda bukan anggotanya.")
                        else:
                            task_menu_member(project_id, current_user)
                    except ValueError:
                        print("\nID proyek harus berupa angka.")

                elif sub_choice == "2":
                    join_project(current_user)

                elif sub_choice == "3":
                    leave_project(current_user)

                elif sub_choice == "4":
                    break

                else:
                    print("\nPilihan tidak valid.")

        # Logout
        elif choice == "3":
            print("\nLogout berhasil.")
            break

        else:
            print("\nPilihan tidak valid.")


def main_menu():
    """
    Menu utama aplikasi Plannery.
    Menyediakan fitur registrasi, login, dan keluar aplikasi.
    """
    while True:
        print("\n=== Plannery ===")
        print("1. Registrasi")
        print("2. Login")
        print("3. Keluar")
        print("================")

        choice = input("Pilih menu: ")

        if choice == "1":
            register()

        elif choice == "2":
            user = login()
            if user is not None:
                project_menu(user)

        elif choice == "3":
            print("\nTerima kasih telah menggunakan Plannery.")
            break

        else:
            print("Pilihan tidak valid.")


# Menjalankan aplikasi
main_menu()