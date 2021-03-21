# DataJoint Element - Lab

## Description of modality, user population 
Most pipelines track some information about the lab, including the facilities, experiment rigs, and users. All interviewed labs have some version of these elements. They also have custom interfaces and GUIs for entering.   

## Precursor projects and interviews
Over the past few years, several labs have developed DataJoint-based pipelines for lab management. Our team collaborated with several of them during their projects. Additionally, we interviewed these teams to understand their experiment workflow, associated tools, and interfaces. 
These teams include
Team / Institution / Pipeline repository 
+ International Brain Laboratory https://github.com/int-brain-lab/IBL-pipeline
+ BrainCoGs (Princeton Neuroscience Institute) https://github.com/BrainCOGS/U19-pipeline_python; https://github.com/BrainCOGS/U19-pipeline-matlab
>+ MoC3 (Columbia Zuckerman Institute) 
>+ Churchland Lab: https://github.com/ZuckermanBrain/datajoint-churchland/tree/master/churchland_pipeline_python
>+ Costa Lab (private repository)
>+ Hillman Lab: https://github.com/ZuckermanBrain/datajoint-hillman

## Development and validation
Through our interviews and direct collaboration on the precursor projects, we identified the common motifs in the lab schemas to create the Lab Management Element.
This element works for diverse downstream pipelines and is always used in combination with other elements for specific experiments. As such it is validated jointly with the acquisition elements such as the Neuropixels Element and Calcium Imaging Element.

## Element usage

+ See the [workflow-imaging](https://github.com/datajoint/workflow-imaging) and [workflow-ephys](https://github.com/datajoint/workflow-ephys) repositories for example usages of `elements-lab`.

+ See the [datajoint-elements](https://github.com/datajoint/datajoint-elements) repository for a detailed description of the DataJoint elements and workflows.

## Element architecture

![elements lab diagram](images/elements_lab_diagram.svg)
