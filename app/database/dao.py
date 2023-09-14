from app.entity.contract import Contract
from app.entity.project import Project
from app.database.database import Database
import datetime


class Dao:
    database = Database()

    def display_data(self):
        data = ''
        self.database.execute("SELECT * FROM contracts")
        contracts = self.database.cur.fetchall()
        data += "\nContracts:"
        for contract in contracts:
            contract_id, contract_name, creation_date, signing_date, status, project_id = contract
            data += f"\n{contract_name} - Status: {status} - Project ID: {project_id}"

        self.database.execute("SELECT * FROM projects")
        projects = self.database.cur.fetchall()
        data += "\nProjects:"
        for project in projects:
            project_id, project_name, creation_date = project
            data += f"\n{project_name} - Project ID: {project_id}"
        return data

    def create_project(self, project_name):
        self.database.execute("INSERT INTO projects (project_name, creation_date) VALUES (%s, %s)",
                              (project_name, datetime.datetime.now()))
        self.database.commit()

    def get_draft_contracts(self):
        return self.get_contracts(" WHERE status = 'draft'")

    def link_project_with_contract(self, project_id, contract_id):
        self.database.execute("UPDATE contracts SET project_id = %s WHERE id = %s",
                              (project_id, contract_id))
        self.database.commit()

    def get_project_contracts(self, project_id):
        return self.get_contracts(" WHERE project_id = " + project_id)

    def get_active_contracts(self):
        return self.get_contracts(" WHERE status = 'active'")

    def get_active_contracts_without_project(self):
        return self.get_contracts(" WHERE status = 'active' AND project_id IS NULL")

    def get_contracts(self, additional_cause=''):
        contracts = []
        self.database.execute("SELECT * FROM contracts" + additional_cause)
        data = self.database.cur.fetchall()

        for row in data:
            contract = Contract(*row)
            contracts.append(contract)

        return contracts

    def confirm_contracts(self, contract_id):
        self.database.execute("UPDATE contracts SET status = %s, signing_date = %s WHERE id = %s",
                              ("active", datetime.datetime.now(), contract_id))
        self.database.commit()

    def get_contractless_projects(self):
        projects = []
        self.database.execute("""SELECT projects.id, project_name, projects.creation_date
                                        FROM public.projects
                                        LEFT JOIN contracts ON projects.id = contracts.project_id
                                        WHERE contracts.project_id IS NULL;""")
        data = self.database.cur.fetchall()

        for row in data:
            project = Project(*row)
            projects.append(project)

        return projects

    def get_projects_with_unfinished_contracts(self):
        projects = []
        self.database.execute("""SELECT projects.id, project_name, projects.creation_date
                                        FROM public.projects
                                        LEFT JOIN contracts ON projects.id = contracts.project_id
                                        WHERE contracts.project_id IS NOT NULL;""")
        data = self.database.cur.fetchall()

        for row in data:
            project = Project(*row)
            projects.append(project)

        return projects

    def create_contract(self, contract_name):
        self.database.execute("INSERT INTO contracts (contract_name, creation_date, status) VALUES (%s, %s, %s)",
                              (contract_name, datetime.datetime.now(), "draft"))
        self.database.commit()

    def complete_contract(self, contract_id):
        self.database.execute("UPDATE contracts SET project_id = NULL, status = %s WHERE id = %s",
                              ("completed", contract_id))
        self.database.commit()

    def close_db(self):
        self.database.close()
