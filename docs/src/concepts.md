# Concepts

## Storage of high-level information about a laboratory 

Most pipelines track some information about the lab, including the facilities, experiment rigs, and users. This can help track which users lab members are associated with which projects or who is responsible for equipment.

Through our interviews and direct collaboration on the precursor projects, we identified the common motifs in the lab schemas. This Element works for diverse downstream pipelines and is always used in combination with other Elements for specific experiments. As such, it is validated jointly with the acquisition Elements such as
[Extracellular Array Electrophysiology](https://datajoint.com/docs/elements/element-array-ephys) 
and 
[Calcium Imaging](https://datajoint.com/docs/elements/element-calcium-imaging).

## Key Partnerships

Over the several years, many labs have developed DataJoint-based pipelines for lab management. The DataJoint team collaborated with several and interviewed these teams to understand their experiment workflow, associated tools, and interfaces. These teams include: 

- International Brain Laboratory
- BrainCoGs (Princeton Neuroscience Institute), Python pipeline, MATLAB pipeline 
- MoC3 (Columbia Zuckerman Institute) 
- Churchland Lab 
- Costa Lab (private repository) 
- Hillman Lab

## Element architecture

![element lab diagram](../../images/lab_diagram.svg)