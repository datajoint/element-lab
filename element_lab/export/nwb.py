import logging

from datajoint.errors import DataJointError

from .. import lab, project

logger = logging.getLogger("datajoint")


def _lab_to_nwb_dict(lab_key: dict) -> dict:
    """Generate a dictionary containing all relevant lab and institution info.

    Args:
        lab_key (dict): Key specifying one entry in element_lab.lab.Lab

    Returns:
        dict: Dictionary with NWB parameters.
    """
    lab_info = (lab.Lab * lab.Lab.Organization * lab.Organization & lab_key).fetch1()
    return dict(
        institution=lab_info.get("org_name"),
        lab=lab_info.get("lab_name"),
    )


def _project_to_nwb_dict(project_key: dict) -> dict:
    """Generate a dictionary object containing relevant project information
        (e.g., experimental description, related publications, etc.).

    Args:
        project_key (dict): Key specifying one entry in element_lab.lab.Project

    Returns:
        dict: Dictionary with NWB parameters.
    """

    try:  # if using project schema (not lab.Project), fetch1 will DataJointError
        project_info = (lab.Project & project_key).fetch1()
        return dict(
            experiment_description=project_info.get("project_description"),
            keywords=(lab.ProjectKeywords() & project_key).fetch("keyword").tolist()
            or None,
            related_publications=(lab.ProjectPublication() & project_key)
            .fetch("publication")
            .tolist()
            or None,
        )
    except DataJointError:
        return dict(
            experiment_description=(project.Project & project_key).fetch1(
                "project_title"
            ),
            keywords=(project.ProjectKeywords & project_key).fetch("keyword").tolist()
            or None,
            related_publications=(project.ProjectPublication() & project_key)
            .fetch("publication")
            .tolist()
            or None,
        )


def _protocol_to_nwb_dict(protocol_key: dict) -> dict:
    """Generate a dictionary object containing all protocol title and notes.

    Args:
        protocol_key (dict): Key specifying one entry in element_lab.lab.Protocol

    Returns:
        dict: Dictionary with NWB parameters.
    """

    protocol_info = (lab.Protocol & protocol_key).fetch1()
    return dict(
        protocol=protocol_info.get("protocol"),
        notes=protocol_info.get("protocol_description"),
    )


def element_lab_to_nwb_dict(
    lab_key: dict = None, project_key: dict = None, protocol_key: dict = None
) -> dict:
    """Generate a NWB-compliant dictionary object for lab metadata

    Generate a dictionary object containing all relevant lab information used
       when generating an NWB file at the session level.
       All parameters optional, but should only specify one of respective type.

    Args:
        lab_key (dict, optional): Key specifying one entry in element_lab.lab.Lab
        project_key (dict, optional): Key specifying one entry in element_lab.lab.Project
        protocol_key (dict, optional): Key specifying one entry in element_lab.lab.Protocol

    Returns:
        dict: Dictionary with NWB parameters.
    """
    # Validate input
    assert any([lab_key, project_key, protocol_key]), "Must specify one key."
    assert (
        lab_key is None or len(lab.Lab & lab_key) == 1
    ), "Multiple labs error! The lab_key should specify only one lab."
    assert (
        project_key is None
        or len(lab.Project & project_key) == 1
        or len(project.Project & project_key) == 1
    ), "Multiple projects error! The project_key should specify only one project."
    assert (
        protocol_key is None or len(lab.Protocol & protocol_key) == 1
    ), "Multiple protocols error! The protocol_key should specify only one protocol."

    element_info = dict()
    if lab_key:
        element_info.update(_lab_to_nwb_dict(lab_key))
    if project_key:
        element_info.update(_project_to_nwb_dict(project_key))
    if protocol_key:
        element_info.update(_protocol_to_nwb_dict(protocol_key))

    return element_info
