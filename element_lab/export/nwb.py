import numpy as np
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile

from element_lab import lab

def lab_to_nwb(lab_key):
    lab_query = lab.Lab & lab_key
    lab_query = lab_query.join(lab.Lab.Protocol, left=True)
    lab_query = lab_query.join(lab.Lab.Project, left=True)
    lab_info = lab.query.fetch1()

    return NWBFile(
    data_collection='',
    experiment_description=lab_info.pop('project_description'),
    institution=lab_info.pop('institution'),
    keywords=list(lab.Project.keywords.fetch()),
    lab=lab_info.pop('lab_name'),
    notes=lab_info.pop('protocol_description'),
    pharmacology=lab_info.pop('pharmacology'),
    protocol=lab_info.pop('protocol'),
    related_publications=list(lab.Project.publication.fetch()),
    session_id='', # why is NWB asking for this at this level?
    slices=lab_info.pop('slices'),
    souce_script=lab_info.pop('repositoryurl'),
    file_name=lab_info.pop('repositoryname'),
    stimulus=lab_info.pop('stimulus'),
    surgery=lab_info.pop('surgery'),
    virus=lab_info.pop('virus')
    )
