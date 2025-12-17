def tampilkan_tugas_pribadi():
    while True:
        with open("task.txt", "r") as file:
            task = file.readlines()

        print("DAFTAR TUGAS: ")
        if len(task) == 0:
            print("Belum ada tugas.")
        else:
            for i in range(len(task)):
                print(str(i + 1) + "." + task[i].strip())

        print("\nMenu \n")
        print("1. Lihat Detail Tugas")
        print("2. Buat Tugas")
        print("3. Edit Tugas")
        print("4. Hapus Tugas")
        print("5. Keluar")

        pilihan = int(input("Pilih dalah satu menu (1-5): "))

        if pilihan == 1:
            nomor = int(input("pilih  nomor tugas: "))
            if nomor >= 1 and nomor <= len(task):
                print("Detail tugas: ", task[nomor - 1])
            else:
                print("Tugas dengan nomor tersebut tidak tersedia.")

        elif pilihan == 2:
            tugas_baru = input("Masukkan nama tugas: ")
            with open("task.txt", "a") as file:
                file.write(tugas_baru + "\n")

        elif pilihan == 3:
            nomor = int(input("pilih  nomor tugas: "))
            if nomor >= 1 and nomor <= len(task):
                edit_tugas = input("Masukkan nama tuggas baru: ")
                task[nomor - 1] = edit_tugas
                with open ("task.txt", "w") as file:
                    file.writelines(task)
            else:
                print("Tugas dengan nomor tersebut tidak tersedia.")

        elif pilihan == 4:
            nomor = int(input("Pilih nomor tugas: "))
            if nomor >= 1 and nomor <= len(task):
                task.pop(nomor-1)
                with open ("task.txt", "w") as file:
                    file.writelines(task)
            else:
                print("Tugas dengan nomor tersebut tidak tersedia: ")

        elif pilihan == 5:
            print("kembali ke menu sebelumnya.")
            break

        else:
            print("Pilihan anda tidak valid.")

tampilkan_tugas_pribadi()