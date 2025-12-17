
                #Lihat projek sendiri
def view_project_details(user, project_number):
    print(f"Detail project {project_number} milik {user}")

def create_project(user):
    print(f"Project baru dibuat oleh {user}")

def edit_project(user, project_number):
    print(f"Project {project_number} milik {user} diedit")

def delete_project(user, project_number):
    print(f"Project {project_number} milik {user} dihapus")

def view_own_projects(user):
    while True:
        print("List project milik user")
        print("Choose an option:")
        print("1. View Project Details")
        print("2. Create Project")
        print("3. Edit Project")
        print("4. Delete Project")
        print("5. Exit")

        option = input("Pilihan: ")

        if option == "1":
            project_number = input("Masukkan nomor project: ")
            view_project_details(user, project_number)

        elif option == "2":
            create_project(user)

        elif option == "3":
            project_number = input("Masukkan nomor project: ")
            edit_project(user, project_number)

        elif option == "4":
            project_number = input("Masukkan nomor project: ")
            delete_project(user, project_number)

        elif option == "5":
            return

        else:
            print("Invalid choice")

view_own_projects("User1")


            #buat proyek

def create_project():
    print("Enter project name:")
    project_name = input()

    if project_name == "":
        print("Project name cannot be empty")
        return

    file = open("projects.txt", "a")
    file.write(project_name + "\n")
    file.close()

    print("Project created successfully")
    return

create_project()

                    #sunting projek

def edit_project():
    try:
        file = open("projects.txt", "r")
        projects = file.readlines()
        file.close()
    except FileNotFoundError:
        print("No projects found")
        return

    if len(projects) == 0:
        print("No projects found")
        return

    for i in range(len(projects)):
        print(f"{i + 1}. {projects[i].strip()}")

    print("Select project number to edit:")
    choice = input()

    if not choice.isdigit():
        print("Invalid choice")
        return

    choice = int(choice)

    if choice < 1 or choice > len(projects):
        print("Invalid choice")
        return

    print("Enter new project name:")
    new_name = input()

    if new_name == "":
        print("Project name cannot be empty")
        return

    projects[choice - 1] = new_name + "\n"

    file = open("projects.txt", "w")
    file.writelines(projects)
    file.close()

    print("Project updated successfully")
    return

edit_project()


