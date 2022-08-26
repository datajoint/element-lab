import importlib
import inspect

import datajoint as dj

from element_lab import lab

schema = dj.Schema()

_linking_module = None


def activate(
    project_schema_name,
    lab_schema_name,
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
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), (
        "The argument 'dependency' must" + " be a module or module name"
    )

    global _linking_module
    _linking_module = linking_module

    lab.activate(
        lab_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        linking_module=_linking_module,
    )

    schema.activate(
        project_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=_linking_module.__dict__,
    )


@schema
class Project(dj.Manual):
    definition = """# Top-level grouping of studies and experiments to investigate a scientific question
    project_id                               : VARCHAR(24)                 # abbreviated project name
    ---
    project_title                            : VARCHAR(1024)               # full project title and/or description
    project_start_date                       : DATE                        # the start of the project
    project_end_date=NULL                    : DATE                        # the end date of the project
    project_url=''                           : VARCHAR(512)                # URL of the project repository
    project_keywords=''                      : VARCHAR(1024)               # comma-separated list of keywords describing the project
    project_comment=''                       : VARCHAR(1024)               # additional notes on the project
    """

    class Personnel(dj.Part):
        definition = """# List of individuals involved in a project
        -> master
        -> lab.User
        """


@schema
class Study(dj.Manual):
    definition = """# A research protocol or set of experiments designed to address a specific aim
    study_name                               : VARCHAR(128)                # full study name, e.g., 'perceptual response tasks', or 'Aim 1'
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
    definition = """# Experimental tasks and protocols and their associated lab and study
    experiment_uuid                          : UUID                        # unique identifier of the experiment
    ---
    experiment_name=NULL                     : VARCHAR(32)                 # experiment name or identifier
    experiment_description=''                : VARCHAR(1024)               # short description of the focus of the experiment
    -> Study
    -> lab.Lab
    -> [nullable] lab.Protocol
    """
