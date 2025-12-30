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


def project_menu(current_user):
    while True:
        print("\n=== Menu Proyek ===")
        print("1. Lihat Daftar Proyek (Status: Pemilik)")
        print("2. Lihat Daftar Proyek (Status: Anggota)")
        print("3. Logout")

        choice = input("Pilih menu: ")

        if choice == "1":
            while True:
                print("\n--- Proyek sebagai Pemilik ---")
                print("1. Lihat Daftar Proyek")
                print("2. Buat Proyek")
                print("3. Edit Proyek")
                print("4. Hapus Proyek")
                print("5. Kembali")

                sub_choice = input("Pilih menu: ")

                if sub_choice == "1":
                    view_owned_projects(current_user)

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
                print("\n--- Proyek sebagai Anggota ---")
                print("1. Lihat Daftar Proyek")
                print("2. Gabung Proyek (Kode Proyek)")
                print("3. Keluar dari Proyek")
                print("4. Kembali")

                sub_choice = input("Pilih menu: ")

                if sub_choice == "1":
                    view_joined_projects(current_user)

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
