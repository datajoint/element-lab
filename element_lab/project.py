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
            + Lab: table defining 
            + User: table defining user/personnel/experimenter to be associated with Project.
            + Protocol: 
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), (
        "The argument 'dependency' must" + " be a module or module name"
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
    definition = """# Top-level grouping of studies and experiments to investigate a scientific question
    project                                  : VARCHAR(24)                 # abbreviated project name
    ---
    project_title                            : VARCHAR(1024)               # full project title and/or description
    project_start_date                       : DATE                        # the start of the project
    project_end_date=NULL                    : DATE                        # the end date of the project
    project_comment=''                       : VARCHAR(1024)               # additional notes on the project
    """


@schema
class ProjectPersonnel(dj.Manual):
    definition = """# List of individuals involved in a project
    -> Project
    -> lab.User
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
class Study(dj.Manual):
    definition = """# A set of experiments designed to address a specific aim
    -> Project
    study                                    : VARCHAR(24)    # abbreviated study name, e.g., 'Aim 1'
    ---
    study_name                               : VARCHAR(128)   # full study name, e.g., 'perceptual response tasks', or 'Aim 1'
    study_description=''                     : VARCHAR(1024)  # description of study goals, objectives, and/or methods
    """

    class Protocol(dj.Part):
        definition = """# Information about the experiment(s) approved by some institutions like IACUC, IRB, etc.
        -> master
        -> Protocol
        """


@schema
class Experiment(dj.Manual):
    definition = """# Experimental tasks and protocols and their associated lab and study
    experiment                      : VARCHAR(24)     # abbreviated experiment name
    ---
    experiment_name=''              : VARCHAR(128)    # experiment full name or identifier
    experiment_description=''       : VARCHAR(1024)   # description of the focus of the experiment
    -> Study
    -> Lab
    -> [nullable] Protocol
    """
