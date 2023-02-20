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
    """Activate this schema

    Args:
        schema_name (str): schema name on the database server to activate the Element
        create_schema (bool): when True (default), create schema in the database if it
            does not yet exist.
        create_tables (bool): when True (default), create schema tables in the database
            if they do not yet exist.
        linking_module (str): A string containing the module name or module containing
            the required dependencies to activate the schema.

    Dependencies:
    Upstream tables:
        Lab: table defining general lab information
        User: table defining user/personnel/experimenter associated with Project.
        Protocol: table defining a protocol (e.g., protocol number and title)
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(
        linking_module
    ), "The argument 'linking_module' must be a module or module name"

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
        project_end_date (date, optional): The end date of the project
        project_comment ( varchar(1024), optional): additional notes on the project
    """

    definition = """# Top-level grouping of studies and experiments
    project               : varchar(24)   # abbreviated project name
    ---
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
    """Project keywords. If the dataset is exported, this metadata is saved within the NWB file.

    Attributes:
        Project (foreign key): Project key
        keyword ( varchar(32) ): Keywords describing the project
    """

    definition = """
    # Project keywords. If the dataset is exported, this metadata is saved within the NWB file.
    -> Project
    keyword: varchar(32) # Keywords describing the project
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
    publication: varchar(255)  # Publication name or citation
    """


@schema
class ProjectSourceCode(dj.Manual):
    """Web address of source code

    Attributes:
        Project (foreign key): Project key
        repository_url ( varchar(255) ): Link to code repository
        repository_name ( varchar(32), optional): Name of code repository
    """

    definition = """# Web address of source code
    -> Project
    repository_url     : varchar(255)  # Link to code repository

    ---
    repository_name='' : varchar(32)   # Name of code repository
    """


@schema
class Study(dj.Manual):
    """A set of experiments designed to address a specific aim

    Attributes:
        Project (foreign key): Project key
        study ( varchar(24) ): Abbreviated study name, e.g., 'Aim 1'
        study_name ( varchar(128) ): Full study name, e.g., 'perceptual response tasks'
        study_description ( varchar(1024), optional ): Description of study goals,
            objectives, and/or methods
    """

    definition = """# A set of experiments designed to address a specific aim
    -> Project
    study                : varchar(24)    # Abbreviated study name, e.g., 'Aim 1'
    ---
    study_name           : varchar(128)   # Full name, e.g., 'perceptual response tasks'
    study_description='' : varchar(1024)  # Description of study goals, objectives, and/or methods
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
    """Experimental tasks and their associated lab, study, and protocol

    Attributes:
        experiment ( varchar(24) ): Abbreviated experiment name
        experiment_name ( varchar(128), optional): Experiment full name or identifier
        experiment_description ( varchar(1024), optional): Description of the
            experiment's focus
        Study (foreign key): Study key
        Lab (foreign key): Lab key
        Protocol (foreign key, optional): Protocol key
    """

    definition = """# Experimental tasks and their associated lab, study, and protocol
    experiment                : varchar(24)   # Abbreviated experiment name
    ---
    experiment_name=''        : varchar(128)  # Experiment full name or identifier
    experiment_description='' : varchar(1024) # Description of the experiment's focus
    -> Study
    -> Lab
    -> [nullable] Protocol
    """
