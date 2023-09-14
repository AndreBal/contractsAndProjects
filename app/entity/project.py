class Project:
    def __init__(self, id, project_name, creation_date):
        self.id = id
        self.project_name = project_name
        self.creation_date = creation_date  # datetime.datetime.now()
        self.contracts = []
