import datajoint as dj

schema = dj.Schema()


def activate(schema_name: str, create_schema: bool = True, create_tables: bool = True):
    """Activate this schema

    Args:
        schema_name (str): schema name on the database server to activate the `lab` element
        create_schema (bool, optional): when True (default), create schema in the database if it
                            does not yet exist.
        create_tables (bool, optional): when True (default), create schema tables in the database
                             if they do not yet exist.
    """
    schema.activate(
        schema_name, create_schema=create_schema, create_tables=create_tables
    )


@schema
class Lab(dj.Lookup):
    """Table for storing general lab info.

    Attributes:
        lab ( varchar(24) ): Abbreviated lab name.
        lab_name ( varchar(255) ): Full lab name.
        institution ( varchar(255) ): Name of the affiliation institution.
        address ( varchar(255) ): Physical lab address.
        time_zone ( varchar(64) ): 'UTC±X' format for NWB export.
    """

    definition = """
    lab             : varchar(24)    # abbreviated lab name
    ---
    lab_name        : varchar(255)   # full lab name
    institution     : varchar(255)
    address         : varchar(255)
    time_zone       : varchar(64)    # 'UTC±X' format for NWB export
    """


@schema
class Location(dj.Lookup):
    """Location of animal housing or experimental rigs.

    Attributes:
        Lab (foreign key): Lab key.
        location ( varchar(32) ): Location of the lab.
        location_description ( varchar(255) ): Optional. Description of the lab location.
    """

    definition = """
    -> Lab
    location                   : varchar(32)
    ---
    location_description=''    : varchar(255)
    """


@schema
class UserRole(dj.Lookup):
    """Roles assigned to a user or a job title.

    Attributes:
        user_role ( varchar(16) ): (e.g., "PI", "Postdoc", "Surgeon", etc.)
    """

    definition = """
    user_role           : varchar(16)
    """


@schema
class User(dj.Lookup):
    """Table for storing user information.

    Attributes:
        user ( varchar(32) ): User name.
        user_email ( varchar(128) ): User email address.
        user_cellphone ( varchar(32) ): User cellphone number.
    """

    definition = """
    user                : varchar(32)
    ---
    user_email=''       : varchar(128)
    user_cellphone=''   : varchar(32)
    """


@schema
class LabMembership(dj.Lookup):
    """Store lab membership information using three lookup tables.

    Attributes:
        Lab (foreign key): Lab key.
        User (foreign key): User key.
        UserRole (foreign key): Optional. UserRole primary key.
    """

    definition = """
    -> Lab
    -> User
    ---
    -> [nullable] UserRole
    """


@schema
class ProtocolType(dj.Lookup):
    """Store protocol types.

    Attributes:
        protocol_type ( varchar(32) ): Protocol types (e.g., IACUC, IRB, etc.).
    """

    definition = """
    protocol_type           : varchar(32)
    """


@schema
class Protocol(dj.Lookup):
    """Store information about protocols approved by institutions like IACUC, IRB.

    Attributes:
        protocol ( varchar(16) ): Protocol identifier.
        ProtocolType (foreign key): ProtocolType key.
        protocol_description( varchar(255) ): Optional. Description of the protocol.
    """

    definition = """
    protocol                : varchar(16)
    ---
    -> ProtocolType
    protocol_description='' : varchar(255)
    """


@schema
class Project(dj.Lookup):
    """Projects undergoing in the lab.

    Attributes:
        project ( varchar(32) ): Project identifier.
        project_description ( varchar(1024) ): Description about the project.
    """

    definition = """
    project                 : varchar(32)
    ---
    project_description=''  : varchar(1024)
    """


@schema
class ProjectKeywords(dj.Manual):
    """Project keywords or exported dataset meta info.

    Attributes:
        Project (foreign key): Project key.
        keyword ( varchar(32) ): Description about the project.
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
        contact_details ( varchar(255) ): Optional. Phone number or email.
        source_description ( varchar(255) ): Optional. Description of the source.
    """

    definition = """
    source                : varchar(32)  # abbreviated source name
    ---
    source_name           : varchar(255)
    contact_details=''    : varchar(255)
    source_description='' : varchar(255)
    """
