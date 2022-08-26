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
class Project(dj.Manual):
    definition = """# Information about the project
    project_id                               : VARCHAR(24)                 # abbreviated project name
    ---
    project_title                            : VARCHAR(1024)               # full project title and description
    project_start_date                       : DATE                        # the start of the project
    project_end_date                         : DATE                        # the end date of the project
    project_url=''                           : VARCHAR(512)                # URL of the project repository
    project_keywords=''                      : VARCHAR(1024)               # comma-separated list of keywords describing the project
    project_comment=''                       : VARCHAR(1024)               # additional notes on the project
    """

    class Personnel(dj.Part):
        definition = """# List of individuals involved in a project
        -> master
        -> User
        """


@schema
class Study(dj.Manual):
    definition = """# Collection of tasks, experiments, or aims under a single project
    study_name                               : VARCHAR(128)                # full study name, e.g., 'Navigation tasks', or 'Aim 1'
    -> Project
    ---
    study_description=''                     : VARCHAR(1024)               # description of study goals, objectives, and/or methods
    """

    class Protocol(dj.Part):
        definition = """# Information about the experiment(s) approved by some institutions like IACUC, IRB, etc.
        -> master
        -> Protocol
        """


@schema
class Experiment(dj.Manual):
    definition = """# Experimental tasks and their associated lab and study
    experiment_uuid                 : UUID                        # unique identifier of the experiment
    ---
    experiment_name=NULL            : VARCHAR(32)                 # experiment name or identifier
    experiment_description=''       : VARCHAR(1024)               # short description of the focus of the experiment
    -> Study
    -> Lab
    -> [nullable] Protocol
    """
