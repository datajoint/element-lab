from element_lab import lab


def lab_to_nwb_dict(lab_key):
    """
    Generate a dictionary containing all relevant lab and institution info
    :param lab_key: Key specifying one entry in element_lab.lab.Lab
    :return: dictionary with NWB parameters
    """
    lab_info = (lab.Lab & lab_key).fetch1()
    return dict(
        institution=lab_info.get("institution"),
        lab=lab_info.get("lab_name"),
    )


def project_to_nwb_dict(project_key):
    """
    Generate a dictionary object containing relevant project information
        (e.g., experimental description, related publications, etc.).
    :param project_key: Key specifying one entry in element_lab.lab.Project
    :return: dictionary with NWB parameters
    """
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


def protocol_to_nwb_dict(protocol_key):
    """
    Generate a dictionary object containing all protocol title and notes.
    :param protocol_key: Key specifying one entry in element_lab.lab.Protocol
    :return: dictionary with NWB parameters
    """
    protocol_info = (lab.Protocol & protocol_key).fetch1()
    return dict(
        protocol=protocol_info.get("protocol"),
        notes=protocol_info.get("protocol_description"),
    )


def element_lab_to_nwb_dict(lab_key=None, project_key=None, protocol_key=None):
    """
    Generate a dictionary object containing all relevant lab information used
        when generating an NWB file at the session level.
        All parameters optional, but should only specify one of respective type
    Use: mynwbfile = pynwb.NWBFile(identifier="your identifier",
                             session_description="your description",
                             session_start_time=session_datetime,
                             **element_lab_to_nwb_dict(
                                lab_key=key1,
                                project_key=key2,
                                protocol_key=key3))

    :param lab_key: Key specifying one entry in element_lab.lab.Lab
    :param project_key: Key specifying one entry in element_lab.lab.Project
    :param protocol_key: Key specifying one entry in element_lab.lab.Protocol
    :return: dictionary with NWB parameters
    """
    # Validate input
    assert any([lab_key, project_key, protocol_key]), "Must specify one key."
    assert (
        lab_key is None or len(lab.Lab & lab_key) == 1
    ), "Multiple labs error! The lab_key should specify only one lab."
    assert project_key is None or len(lab.Project & project_key) == 1, (
        "Multiple projects error! The project_key should specify only one " "project."
    )
    assert protocol_key is None or len(lab.Protocol & protocol_key) == 1, (
        "Multiple protocols error! The protocol_key should specify only one "
        "protocol."
    )

    element_info = dict()
    if lab_key:
        element_info.update(lab_to_nwb_dict(lab_key))
    if project_key:
        element_info.update(project_to_nwb_dict(project_key))
    if protocol_key:
        element_info.update(protocol_to_nwb_dict(protocol_key))

    return element_info
