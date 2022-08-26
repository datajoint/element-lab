import datajoint as dj

schema = dj.Schema()


def activate(schema_name, create_schema=True, create_tables=True, linking_module=None):
    """
    activate(schema_name, create_schema=True, create_tables=True, linking_module=None)
        :param schema_name: schema name on the database server to activate the
                            `lab` element
        :param create_schema: when True (default), create schema in the
                              database if it does not yet exist.
        :param create_tables: when True (default), create tables in the
                              database if they do not yet exist.
        :param linking_module: a module (or name) containing the required
                            dependencies to activate the `event` element:
        Upstream tables:
            + User: table defining user/personnel/experimenter to be associated with Project.
    """
    schema.activate(
        schema_name, create_schema=create_schema, create_tables=create_tables
    )


@schema
class Project(dj.Lookup):
    definition = """
    project                 : varchar(32)
    ---
    project_description=''  : varchar(1024)
    """


@schema
class ProjectKeywords(dj.Manual):
    definition = """
    # Project keywords, exported dataset meta info
    -> Project
    keyword: varchar(32)
    """


@schema
class ProjectPublication(dj.Manual):
    definition = """
    # Project's resulting publications
    -> Project
    publication: varchar(256)
    """


@schema
class ProjectSourceCode(dj.Manual):
    definition = """
    # URL to source code for replication
    -> Project
    repository_url     : varchar(256)
    ---
    repository_name='' : varchar(32)
    """


@schema
class ProjectUser(dj.Manual):
    definition = """
    -> Project
    -> User
    """
