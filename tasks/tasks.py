tugas = []
detail = {}

with open("tugas_lain.txt", "r") as file:
    for line in file:
        data = line.strip().split("|")
        tugas.append(data[0])
        detail[data[0]] = data[1]

while True:
    print("\n----------Daftar Tugas----------\n")
    for i in range(len(tugas)):
        print(f"{i+1}. {tugas[i]}")

    print("Menu")   
    print("1. Lihat detail tugas.")
    print("2. Lihat tugas.")
    print("3. Keluar dari tugas.")
    print("4. Keluar dari Menu.")

    pilihan = input("Silahkan pilih opsi: ")

    if pilihan == "1":
        no = int(input("Masukkan nomor tugas yang akan dipilih: "))
        if 1 <= no <= len(tugas):
            nama = tugas[no - 1]
            print("\n--- Detail Tugas ---")
            print("Nama Tugas :", nama)
            print("Deskripsi  :", detail[nama])
        else:
            print("Nomor tugas tidak valid!")

    elif pilihan == "2":
        print("Fitur Masuk Tugas belum diimplementasikan.")

    elif pilihan == "3":
        print("Fitur Masuk Tugas belum diimplementasikan.")

    elif pilihan == "4":
        print("Kembali ke Menu Proyek.")
        break

    else:
        print("Pilihan tidak valid!")