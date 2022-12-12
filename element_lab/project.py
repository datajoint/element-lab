import importlib
import inspect

import datajoint as dj

schema = dj.Schema()

_linking_module = None


def activate(
    schema_name,
    *,
    create_schema=True,
    create_tables=True,
    linking_module=None,
):
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
            + Lab: table defining general lab information
            + User: table defining user/personnel/experimenter associated with Project.
            + Protocol: table defining a protocol (e.g., protocol number and title)
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), (
        "The argument 'linking_module' must" + " be a module or module name"
    )

    global _linking_module
    _linking_module = linking_module

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=_linking_module.__dict__,
    )


@schema
class Project(dj.Manual):
    """Top-level grouping of studies and experiments to investigate a scientific question

    Attributes:
        project ( varchar(24) ): Abbreviated project name
        project_title ( varchar(1024) ): Full project title and/or description
        project_start_date (date): The start of the project
        project_end_date (date, nullable): The end date of the project
        project_comment ( varchar(1024), optional): additional notes on the project
    """

    definition = """# Top-level grouping of studies and experiments
    ---
    project               : varchar(24)   # abbreviated project name
    project_title         : varchar(1024) # full project title and/or description
    project_start_date    : date          # the start of the project
    project_end_date=NULL : date          # the end date of the project
    project_comment=''    : varchar(1024) # additional notes on the project
    """


@schema
class ProjectPersonnel(dj.Manual):
    """List of individuals involved in a project

    Attributes:
        Project (foreign key): Project key
        User (foreign key): User key
    """

    definition = """# List of individuals involved in a project
    -> Project
    -> User
    """


@schema
class ProjectKeywords(dj.Manual):
    """Project keywords, exported dataset meta info

    Attributes:
        Project (foreign key): Project key
        keyword ( varchar(32) ): Project keyword
    """

    definition = """
    # Project keywords, exported dataset meta info
    -> Project
    keyword: varchar(32)
    """


@schema
class ProjectPublication(dj.Manual):
    """Project's resulting publications

    Attributes:
        Project (foreign key): Project key
        publication ( varchar(255) ): Publication name or citation
    """

    definition = """
    # Project's resulting publications
    -> Project
    publication: varchar(255)

    """


@schema
class ProjectSourceCode(dj.Manual):
    """URL to source code for replication

    Attributes:
        Project (foreign key): Project key
        repository_url ( varchar(255) ): Link to code repository
        repository_name ( varchar(32), optional): Name of code repository
    """

    definition = """
    # URL to source code for replication
    -> Project
    repository_url     : varchar(255)

    ---
    repository_name='' : varchar(32)
    """


@schema
class Study(dj.Manual):
    """A set of experiments designed to address a specific aim

    Attributes:
        Project (foreign key): Project key
        study ( varchar(24) ): Abbreviated study name, e.g., 'Aim 1'
        study_name ( varchar(128) ): Full study name, e.g., 'perceptual response tasks',
            or 'Aim 1'
        study_description ( varchar(1024), optional): Description of study goals,
            objectives, and/or methods
    """

    definition = """# A set of experiments designed to address a specific aim
    -> Project
    study                : varchar(24)    # abbreviated study name, e.g., 'Aim 1'
    ---
    study_name           : varchar(128)   # full name, e.g., 'perceptual response tasks'
    study_description='' : varchar(1024)  # goals, objectives, and/or methods
    """

    class Protocol(dj.Part):
        """Info about institutional approval (e.g., IACUC, IRB, etc.)

        Attributes:
            Study (foreign key): Study key
            Protocol (foreign key): Protocol key
        """

        definition = """# Info about institutional approval (e.g., IACUC, IRB, etc.)
        -> master
        -> Protocol
        """


@schema
class Experiment(dj.Manual):
    """Experimental tasks/protocols and their associated lab and study

    Attributes:
        experiment ( varchar(24) ): abbreviated experiment name
        experiment_name ( varchar(128), optional): Experiment full name or identifier
        experiment_description ( varchar(1024), optional): Experiment's focus
        Study (foreign key): Study key
        Lab (foreign key): Lab key
        Protocol (foreign key, optional): Protocol key
    """

    definition = """# Experimental tasks/protocols and their associated lab and study
    experiment                : varchar(24)   # abbreviated experiment name
    ---
    experiment_name=''        : varchar(128)  # experiment full name or identifier
    experiment_description='' : varchar(1024) # description of the experiment's focus
    -> Study
    -> Lab
    -> [nullable] Protocol
    """
