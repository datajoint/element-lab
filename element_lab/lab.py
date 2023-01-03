import logging

import datajoint as dj

logger = logging.getLogger("datajoint")

schema = dj.Schema()


def activate(schema_name: str, create_schema: bool = True, create_tables: bool = True):
    """Activate this schema

    Args:
        schema_name (str): schema name on the database server to activate the `lab` element
        create_schema (bool): when True (default), create schema in the database if it
                            does not yet exist.
        create_tables (bool): when True (default), create schema tables in the database
                             if they do not yet exist.
    """

    schema.activate(
        schema_name, create_schema=create_schema, create_tables=create_tables
    )


@schema
class Organization(dj.Manual):
    """Top-level list of all organizations involved in any of the projects.

    Attributes:
        organization ( varchar(24) ): Abbreviated organization name.
        org_name ( varchar(255) ): Full organization name.
        org_address ( varchar(512), optional ): Address of the organization.
        org_comment ( varchar(1024), optional ): Additional notes on the organization.
    """

    definition = """# Top-level list of all organizations involved in any of the projects
    organization      : varchar(24)   # Abbreviated organization name
    ---
    org_name          : varchar(255)  # Full organization name
    org_address=''    : varchar(512)  # Address of the organization
    org_comment=''    : varchar(1024) # Additional notes on the organization
    """


@schema
class Lab(dj.Lookup):
    """Table for storing general lab info.

    Attributes:
        lab ( varchar(24) ): Abbreviated lab name.
        lab_name ( varchar(255) ): Full lab name.
        address ( varchar(255) ): Physical lab address.
        time_zone ( varchar(64) ): 'UTC±X' format or timezone, e.g., America/New_York.
            If using NWB export, use 'UTC±X' format.
    """

    definition = """# Table for storing general lab info.
    lab             : varchar(24)    # Abbreviated lab name
    ---
    lab_name        : varchar(255)   # Full lab name
    address         : varchar(255)    # Physical lab address
    time_zone       : varchar(64)    # 'UTC±X' format or timezone, e.g., America/New_York
    """

    class Organization(dj.Part):
        definition = """
        -> master
        -> Organization
        """


@schema
class Location(dj.Lookup):
    """Location of research (e.g., animal housing or experimental rigs).

    Attributes:
        Lab (foreign key): Lab key.
        location ( varchar(32) ): Location of a space related to the lab.
        location_description ( varchar(255), optional ): Description of the location.
    """

    definition = """# location of research (e.g., animal housing or experimental rigs)
    -> Lab
    location                   : varchar(32)   # Location of a space related to the lab
    ---
    location_description=''    : varchar(255)  # Description of the location
    """


@schema
class UserRole(dj.Lookup):
    """Roles assigned to a user or a job title.

    Attributes:
        user_role ( varchar(24) ): Role within the lab (e.g., PI, Postdoc, etc.).
    """

    definition = """# Roles assigned to a user or a job title.
    user_role           : varchar(24) # Role within the lab (e.g., PI, Postdoc, etc.)
    """


@schema
class User(dj.Lookup):
    """Table for storing user information.

    Attributes:
        user ( varchar(32) ): User name.
        user_email ( varchar(128), optional ): User email address.
        user_cellphone ( varchar(32), optional ): User cellphone number.
        user_fullname ( varchar(64), optional ): User full name
    """

    definition = """# Table for storing user information.
    user                : varchar(32)  # username, short identifier
    ---
    user_email=''       : varchar(128)
    user_cellphone=''   : varchar(32)
    user_fullname=''    : varchar(64)  # Full name used to uniquely identify an individual
    """


@schema
class LabMembership(dj.Lookup):
    """Store lab membership information using three lookup tables.

    Attributes:
        Lab (foreign key): Lab key.
        User (foreign key): User key.
        UserRole (foreign key): Optional. UserRole primary key.
    """

    definition = """# Store lab membership information using three lookup tables.
    -> Lab
    -> User
    ---
    -> [nullable] UserRole
    """


@schema
class ProtocolType(dj.Lookup):
    """Type of protocol or issuing agency.

    Attributes:
        protocol_type ( varchar(32) ): Protocol types (e.g., IACUC, IRB, etc.).
    """

    definition = """# Type of protocol or issuing agency
    protocol_type           : varchar(32)  # Protocol types (e.g., IACUC, IRB, etc.)
    """


@schema
class Protocol(dj.Lookup):
    """Protocol approved by institutions (e.g. IACUC, IRB), or experimental protocol.

    Attributes:
        protocol ( varchar(36) ): Protocol identifier.
        ProtocolType (foreign key): ProtocolType key.
        protocol_description( varchar(255), optional ): Description of the protocol.
    """

    definition = """# Protocol approved by institutions (e.g. IACUC, IRB), or experimental protocol.
    protocol                : varchar(36)   # Protocol identifier.
    ---
    -> ProtocolType
    protocol_description='' : varchar(255)  # Description of the protocol
    """


@schema
class Project(dj.Lookup):
    """Projects within a lab.

    Attributes:
        project ( varchar(32) ): Project identifier.
        project_description ( varchar(1024) ): Description about the project.
    """

    logger.warning(
        "lab.Project and related tables will be removed in a future version of"
        + " Element Lab. Please use the project schema."
    )

    definition = """
    project                 : varchar(32)
    ---
    project_description=''  : varchar(1024)
    """


@schema
class ProjectKeywords(dj.Manual):
    """Project keywords or meta-information.

    Attributes:
        Project (foreign key): Project key.
        keyword ( varchar(32) ): Descriptive keyword about the project.
    """

    definition = """
    -> Project
    keyword:    varchar(32)
    """


@schema
class ProjectPublication(dj.Manual):
    """Project's resulting publications.

    Attributes:
        Project (foreign key): Project key.
        publication ( varchar(256) ): Name of the published paper.
    """

    definition = """
    -> Project
    publication:    varchar(256)
    """


@schema
class ProjectSourceCode(dj.Manual):
    """URL to source code for replication.

    Attributes:
        Project (foreign key): Project key.
        repository_url ( varchar(256) ): URL to the code repository.
        repository_name ( varchar(32) ): Name of the repository.
    """

    definition = """
    -> Project
    repository_url     : varchar(256)
    ---
    repository_name='' : varchar(32)
    """


@schema
class ProjectUser(dj.Manual):
    """Users participating in the project.

    Attributes:
        Project (foreign key): Project key.
        User (foreign key): User key.
    """

    definition = """
    -> Project
    -> User
    """


@schema
class Source(dj.Lookup):
    """Source or supplier of subject animals.

    Attributes:
        source ( varchar(32) ): Abbreviated source name.
        source_name ( varchar(255) ): Source name.
        contact_details ( varchar(255) ): Optional. Phone number and/or email.
        source_description ( varchar(255) ): Optional. Description of the source.
    """

    definition = """
    source                : varchar(32)  # abbreviated source name
    ---
    source_name           : varchar(255)
    contact_details=''    : varchar(255)
    source_description='' : varchar(255)
    """
