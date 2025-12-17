import os

FILENAME = "projects.txt"

# --- FUNGSI BANTUAN (HELPER) ---

def get_all_projects():
    """Membaca semua project dari file dengan aman."""
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as file:
        return file.readlines()

def save_all_projects(projects):
    """Menyimpan list project kembali ke file."""
    with open(FILENAME, "w") as file:
        file.writelines(projects)

def show_project_list(projects):
    """Menampilkan daftar project agar user mudah memilih."""
    if not projects:
        print("   (Tidak ada project)")
        return False
    
    print("\n--- Daftar Project ---")
    for i, p in enumerate(projects):
        print(f"{i + 1}. {p.strip()}")
    return True

# --- FITUR UTAMA ---

def create_project(user):
    print("\n--- Buat Project Baru ---")
    print("Masukkan nama project:")
    project_name = input()

    if project_name.strip() == "":
        print("Error: Nama project tidak boleh kosong.")
        return

    with open(FILENAME, "a") as file:
        file.write(project_name + "\n")

    print(f"Sukses: Project '{project_name}' berhasil dibuat oleh {user}.")

def view_project_details(user):
    print("\n--- Lihat Detail Project ---")
    projects = get_all_projects()
    
    if not show_project_list(projects):
        return

    idx_input = input("Masukkan nomor project untuk dilihat: ")
    
    if not idx_input.isdigit():
        print("Error: Pilihan harus angka.")
        return

    idx = int(idx_input) - 1

    if 0 <= idx < len(projects):
        nama_projek = projects[idx].strip()
        print(f"\nDETAIL:")
        print(f"Pemilik : {user}")
        print(f"ID      : {idx + 1}")
        print(f"Nama    : {nama_projek}")
    else:
        print("Error: Project tidak ditemukan.")

def edit_project(user):
    print("\n--- Edit Project ---")
    projects = get_all_projects()

    if not show_project_list(projects):
        return

    idx_input = input("Pilih nomor project yang akan diedit: ")

    if not idx_input.isdigit():
        print("Error: Pilihan harus angka.")
        return

    idx = int(idx_input) - 1

    if 0 <= idx < len(projects):
        print(f"Mengedit: {projects[idx].strip()}")
        new_name = input("Masukkan nama baru: ")

        if new_name.strip() == "":
            print("Error: Nama tidak boleh kosong.")
            return

        projects[idx] = new_name + "\n"
        save_all_projects(projects)
        print("Sukses: Project berhasil diupdate.")
    else:
        print("Error: Nomor project tidak valid.")

def delete_project(user):
    print("\n--- Hapus Project ---")
    projects = get_all_projects()

    if not show_project_list(projects):
        return

    idx_input = input("Pilih nomor project yang akan DIHAPUS: ")

    if not idx_input.isdigit():
        print("Error: Pilihan harus angka.")
        return

    idx = int(idx_input) - 1

    if 0 <= idx < len(projects):
        deleted_name = projects.pop(idx).strip()
        save_all_projects(projects)
        print(f"Sukses: Project '{deleted_name}' telah dihapus.")
    else:
        print("Error: Nomor project tidak valid.")

# --- MENU UTAMA ---

def view_own_projects(user):
    while True:
        print("\n" + "="*25)
        print(f" LOGGED IN AS: {user}")
        print("="*25)
        print("1. View Project Details")
        print("2. Create Project")
        print("3. Edit Project")
        print("4. Delete Project")
        print("5. Exit")
        
        option = input("Pilihan Anda: ")

        if option == "1":
            view_project_details(user)
        elif option == "2":
            create_project(user)
        elif option == "3":
            edit_project(user)
        elif option == "4":
            delete_project(user)
        elif option == "5":
            print("Keluar program... Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

# --- EKSEKUSI ---
if __name__ == "__main__":
    # Pastikan file ada agar tidak error saat pertama kali baca
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f: 
            pass 
            
    view_own_projects("User1")
