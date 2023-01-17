# Concepts

## Storage of high-level information about a laboratory 

Most pipelines track some information about the lab, including the facilities,
experiment rigs, and users. This can help track which users lab members are associated
with which projects or who is responsible for equipment.

Through our interviews and direct collaboration on the precursor projects, we identified
the common motifs in the lab schemas. This Element works for diverse downstream
pipelines and is always used in combination with other Elements for specific
experiments. As such, it is validated jointly with the acquisition Elements such as
[Extracellular Array
Electrophysiology](https://datajoint.com/docs/elements/element-array-ephys) and [Calcium
Imaging](https://datajoint.com/docs/elements/element-calcium-imaging).

## Key Partnerships

Over the several years, many labs have developed DataJoint-based pipelines for lab
management. The DataJoint team collaborated with several and interviewed these teams to
understand their experiment workflow, associated tools, and interfaces. These teams
include: 

- International Brain Laboratory
- BrainCoGs (Princeton Neuroscience Institute), Python pipeline, MATLAB pipeline 
- MoC3 (Columbia Zuckerman Institute) 
- Churchland Lab 
- Costa Lab (private repository) 
- Hillman Lab

## Element architecture

![element lab diagram](https://raw.githubusercontent.com/datajoint/element-lab/d222f673e590979a92ff815adb880f474eed338e/images/lab_diagram.svg)

### `lab` schema ([API docs](https://datajoint.com/docs/elements/element-lab/api/element_lab))

| Table              | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| Lab                | Table for storing general lab info.                              |
| Location           | Location of research (e.g., animal housing or experimental rigs) |
| UserRole           | Roles assigned to a user or a job title.                         |
| User               | Table for storing user information.                              |
| LabMembership      | Store lab membership information using three lookup tables.      |
| ProtocolType       | Type of protocol or issuing agency.                              |
| Protocol           | Protocol specifics (e.g., protocol number and title).            |
| Project            | Projects within a lab.                                           |
| ProjectKeywords    | Project keywords or meta-information.                            |
| ProjectPublication | Project's resulting publications.                                |
| ProjectSourceCode  | URL to source code for replication.                              |
| ProjectUser        | Users participating in the project.                              |
| Source             | Source or supplier of subject animals.                           |
