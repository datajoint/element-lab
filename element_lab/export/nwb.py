from element_lab import lab


def lab_to_nwb_dict(lab_key=None):
    """
    Generate a dictionary containing all relevant lab and institution info
    :param lab_key: Key specifying one entry in element_lab.lab.Lab
    :return: dictionary with NWB parameters
    """
    if lab_key is not None:
        lab_info = (lab.Lab & lab_key).fetch1()
        return dict(
            institution=lab_info.get('institution', ''),
            lab=lab_info.get('lab_name', '')
        )
    else:
        return {}


def project_to_nwb_dict(project_key=None):
    """
    Generate a dictionary object containing relevant project information
        (e.g., experimental description, related publications, etc.).
    :param project_key: Key specifying one entry in element_lab.lab.Project
    :return: dictionary with NWB parameters
    """
    if project_key is not None:
        proj_info = (lab.Project & project_key).fetch1()
        proj_keyw = (lab.Project.Keywords() & project_key
                     ).fetch('keyword').tolist()
        proj_pubs = (lab.Project.Publication() & project_key
                     ).fetch('publication').tolist()
        return dict(
            experiment_description=(proj_info.get('project_description', '')),
            keywords=proj_keyw,
            related_publications=proj_pubs
        )
    else:
        return {}


def protocol_to_nwb_dict(protocol_key=None):
    """
    Generate a dictionary object containing all protocol title and notes.
    :param protocol_key: Key specifying one entry in element_lab.lab.Protocol
    :return: dictionary with NWB parameters
    """
    if protocol_key is not None:
        prot_info = (lab.Protocol & protocol_key).fetch1()
        return dict(
            # data_collection='',
            protocol=(prot_info['protocol']
                      if 'protocol' in prot_info else ''),
            notes=(prot_info['protocol_description']
                   if 'project_description' in prot_info else '')
        )
    else:
        return {}


def elementlab_nwb_dict(lab_key=None, project_key=None, protocol_key=None):
    """
    Generate a dictionary object containing all relevant lab information used
        when generating an NWB file at the session level.
        All parameters optional, but should only specify one of respective type
    Use: mynwbfile = NWBfile(identifier="your identifier",
                             session_description="your description",
                             session_start_time=session_datetime,
                             elementlab_nwb_dict(lab_key=key1,project_key=key2,
                                                 protocol_key=key3))

    :param lab_key: Key specifying one entry in element_lab.lab.Lab
    :param project_key: Key specifying one entry in element_lab.lab.Project
    :param protocol_key: Key specifying one entry in element_lab.lab.PRotocol
    :return: dictionary with NWB parameters
    """
    # Validate input
    if lab_key is not None: 
        assert len(lab.Lab & lab_key
                   ) == 1, ('Multiple labs error! The lab_key should specify '
                            + 'only one lab.')
    if project_key is not None:
        assert len(lab.Project & project_key
                   ) == 1, ('Multiple projects error! The project_key should'
                            + ' specify only one project.')
    if protocol_key is not None:
        assert len(lab.Protocol & protocol_key
                   ) == 1, ('Multiple protocols error! The protocol_key should'
                            + ' specify only one protocol.')

    elem_info = dict(
        lab_to_nwb_dict(lab_key),
        **project_to_nwb_dict(project_key),
        **protocol_to_nwb_dict(protocol_key)
        )

    # Drop blank entries
    for k in list(elem_info):
        if len(elem_info[k]) == 0:
            elem_info.pop(k)

    return elem_info
