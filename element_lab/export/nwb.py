from datetime import datetime
from element_lab import lab

'''
Broz 120121: packages lab, project and protocol data as dicts
    Updated session nwb export function then reads items
    if they exist, populates. If not, blank - not best practice.
    How to populate only NWB items for which we have user entries?
'''

def lab_to_nwb_dict(lab_key=None):
    if lab_key is not None:
        lab_info = (lab.Lab & lab_key).fetch1()
        return dict(
            institution=(lab_info['institution']
                if 'institution' in lab_info else ''),
            lab=(lab_info['lab_name']
                if 'lab_name' in lab_info else '')
        )
    else: return {}


def proj_to_nwb_dict(project_key=None):
    if project_key is not None:
        proj_info = (lab.Project & project_key).fetch1()
        proj_keyw = (lab.Project.Keywords() & project_key).fetch('keyword').tolist()
        proj_pubs = (lab.Project.Publication() & project_key).fetch('publication').tolist()
        return dict(
            experiment_description=(proj_info['project_description']
                if 'project_description' in proj_info else ''),
            keywords=proj_keyw,
            pharmacology=(proj_info['pharmacology']
                if 'pharmacology' in proj_info else ''),
            related_publications=proj_pubs,
            slices=(proj_info['slices']
                if 'slices' in proj_info else ''),
            source_script=(proj_info['repositoryurl']
                if 'repositoryurl' in proj_info else ''),
            stimulus=(list(proj_info['stimulus'])
                if 'stimulus' in proj_info else []),
            surgery=(proj_info['surgery']
                if 'surgery' in proj_info else ''),
            virus=(proj_info['virus']
                if 'virus' in proj_info else '')
        )
    else: return {}


def prot_to_nwb_dict(protocol_key=None):
    if protocol_key is not None:
        prot_info = (lab.Protocol & protocol_key).fetch1()
        return dict(
            # data_collection='',
            protocol=(prot_info['protocol']
                if 'protocol' in prot_info else ''),
            notes=(prot_info['protocol_description']
                if 'project_description' in prot_info else '')
        )
    else: return {}

def elemlab_to_nwb_dict(lab_key=None,project_key=None,protocol_key=None):
    return dict(
        lab_to_nwb_dict(lab_key),
        **proj_to_nwb_dict(project_key),
        **prot_to_nwb_dict(protocol_key)
        )


