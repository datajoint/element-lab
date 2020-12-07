import datajoint as dj

schema = dj.Schema()


def activate(schema_name, create_schema=True, create_tables=True):
    """
    activate(schema_name, create_schema=True, create_tables=True)
        :param schema_name: schema name to activate the `lab` element
        :param create_schema: create the schema if not yet existed (default = True)
        :param create_tables: create the tables if not yet existed (default = True)
    """
    schema.activate(schema_name, create_schema=create_schema, create_tables=create_tables)


@schema
class Lab(dj.Lookup):
    definition = """
    lab             : varchar(24)  #  Abbreviated lab name 
    ---
    lab_name        : varchar(255)   # full lab name
    institution     : varchar(255)
    address         : varchar(255)
    time_zone       : varchar(64)
    """


@schema
class Location(dj.Lookup):
    definition = """
    # location of animal housing or experimental rigs
    -> Lab
    location            : varchar(32)
    ---
    location_description=''    : varchar(255)
    """


@schema
class UserRole(dj.Lookup):
    definition = """
    user_role       : varchar(16)
    """


@schema
class User(dj.Lookup):
    definition = """
    user                : varchar(32)
    ---
    user_email=''       : varchar(128)
    user_cellphone=''   : varchar(32)
    """


@schema
class LabMembership(dj.Lookup):
    definition = """
    -> Lab
    -> User
    ---
    -> [nullable] UserRole
    """


@schema
class ProtocolType(dj.Lookup):
    definition = """
    protocol_type           : varchar(32)
    """


@schema
class Protocol(dj.Lookup):
    definition = """
    # protocol approved by some institutions like IACUC, IRB
    protocol                : varchar(16)
    ---
    -> ProtocolType
    protocol_description=''        : varchar(255)
    """


@schema
class Project(dj.Lookup):
    definition = """
    project                 : varchar(32)
    ---
    project_description=''         : varchar(1024)
    """


@schema
class ProjectUser(dj.Manual):
    definition = """
    -> Project
    -> User
    """


@schema
class Source(dj.Lookup):
    definition = """
    # source or supplier of animals
    source             : varchar(32)    # abbreviated source name
    ---
    source_name        : varchar(255)
    contact_details='' : varchar(255)
    source_description=''     : varchar(255)
    """
