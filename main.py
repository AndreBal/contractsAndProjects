from app.database.dao import Dao

def main():
    dao = Dao()

    while True:
        print("\nMenu:")
        print("1. Project")
        print("2. Contract")
        print("3. View Projects and Contracts")
        print("4. Quit")
        choice = input("Select an option: ")
        if choice == "1":
            print("\nProject Menu:")
            print("1. Start a Project")
            print("2. Add Contract to Project")
            print("3. Terminate Contract from Project")
            print("4. Back to Main Menu")
            print("5. View Projects and Contracts")
            sub_choice = input("Select an option: ")
            if sub_choice == "1":
                contracts = dao.get_contracts()
                if not any(c.status == "active" for c in contracts):
                    print("You cannot start a project without at least one active contract.")
                    continue

                project_name = input("Enter project name: ")
                dao.create_project(project_name)
                print(f"Project '{project_name}' created.")
            elif sub_choice == "2":
                print("\nSelect a contract to add to the project:")
                contracts = dao.get_active_contracts_without_project()
                for i, contract in enumerate(contracts):
                    print(f"{i + 1}. {contract.contract_name}")
                selection = int(input("Enter the contract number: ")) - 1
                if 0 <= selection < len(contracts):
                    contract_id = contracts[selection].id
                    print("\nSelect a project to add the contract to:")
                    projects = dao.get_contractless_projects()
                    for i, project in enumerate(projects):
                        print(f"{i + 1}. {project.project_name}")
                    project_selection = int(input("Enter the project number: ")) - 1
                    if 0 <= project_selection < len(projects):
                        project_id = projects[project_selection].id
                        dao.link_project_with_contract(project_id, contract_id)
                        print("Contract added to the project.")
                    else:
                        print("Invalid project number.")
                else:
                    print("Invalid contract number.")
            elif sub_choice == "3":
                print("\nSelect a project to terminate a contract from:")
                projects = dao.get_projects_with_unfinished_contracts()
                if projects:
                    for i, project in enumerate(projects):
                        print(f"{i + 1}. {project.project_name}")
                    project_selection = int(input("Enter the project number: ")) - 1
                    if 0 <= project_selection < len(projects):
                        project_id = projects[project_selection].id
                        print("\nSelect a contract to terminate:")
                        contracts = dao.get_project_contracts(project_id)
                        for i, contract in enumerate(contracts):
                            print(f"{i + 1}. {contract.contract_name}")
                        contract_selection = int(input("Enter the contract number: ")) - 1
                        if 0 <= contract_selection < len(contracts):
                            contract_id = contracts[contract_selection].id
                            dao.complete_contract(contract_id)
                            print("Contract terminated from the project.")
                        else:
                            print("Invalid contract number.")
                    else:
                        print("Invalid project number.")
                else:
                    print("There are no projects with active contracts.")
            elif sub_choice == "4":
                break
            elif choice == "5":
                print(dao.display_data())
        elif choice == "2":
            print("\n1. Create Contract")
            print("2. Confirm Contract")
            print("3. Complete Contract")
            print("4. Back to Main Menu")
            print("5. View Projects and Contracts")
            sub_choice = input("Select an option: ")
            if sub_choice == "1":
                contract_name = input("Enter contract name: ")
                dao.create_contract(contract_name)
                print(f"Contract '{contract_name}' created.")
            elif sub_choice == "2":
                print("\nSelect a contract to confirm:")
                contracts = dao.get_draft_contracts()
                for i, contract in enumerate(contracts):
                    print(f"{i + 1}. {contract.contract_name}")
                selection = int(input("Enter the contract number: ")) - 1
                if 0 <= selection < len(contracts):
                    contract_id = contracts[selection].id
                    dao.confirm_contracts(contract_id)
                    print("Contract confirmed.")
                else:
                    print("Invalid contract number.")
            elif sub_choice == "3":
                print("\nSelect a contract to complete:")
                contracts = dao.get_active_contracts()
                for i, contract in enumerate(contracts):
                    print(f"{i + 1}. {contract.contract_name}")
                selection = int(input("Enter the contract number: ")) - 1
                if 0 <= selection < len(contracts):
                    contract_id = contracts[selection].id
                    dao.complete_contract(contract_id)
                    print("Contract completed.")
                else:
                    print("Invalid contract number.")
            elif sub_choice == "4":
                break
            elif choice == "5":
                print(dao.display_data())
        elif choice == "3":
            print(dao.display_data())
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select a valid option.")

    dao.close_db()


if __name__ == "__main__":
    main()
