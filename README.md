# DataJoint Element - Lab

DataJoint Element for lab metadata. DataJoint Elements collectively standardize and
automate data collection and analysis for neuroscience experiments. Each Element is a
modular pipeline for data storage and processing with corresponding database tables that
can be combined with other Elements to assemble a fully functional pipeline.

+ `element-lab` features a DataJoint pipeline design for lab related information, such
  as Lab, User, Project, Protocol, Source.

+ `element-lab` is not a complete workflow by itself, but rather a modular design of
  tables and dependencies.

+ `element-lab` can be flexibly attached to any DataJoint workflow.

+ See the [Element Lab documentation](https://elements.datajoint.org/description/lab/)
  for the background information and development timeline.

+ For more information on the DataJoint Elements project, please visit
  https://elements.datajoint.org.  This work is supported by the National Institutes of
  Health.


## Installation

```console
pip install element-lab
```

If you already have an older version of ***element-lab*** installed using `pip`, upgrade
with

```console
pip install --upgrade element-lab
```

## Element usage

+ `element-lab` is not a complete workflow by itself, but rather a modular design of
  tables and dependencies that can be flexibly attached to any DataJoint workflow.

+ See the
  [workflow-calcium-imaging](https://github.com/datajoint/workflow-calcium-imaging) and
  [workflow-array-ephys](https://github.com/datajoint/workflow-array-ephys) repositories
  for example usages of `element-lab`.

## Citation

+ If your work uses DataJoint and DataJoint Elements, please cite the respective
  Research Resource Identifiers (RRIDs) and manuscripts.

+ DataJoint for Python or MATLAB
    + Yatsenko D, Reimer J, Ecker AS, Walker EY, Sinz F, Berens P, Hoenselaar A, Cotton
      RJ, Siapas AS, Tolias AS. DataJoint: managing big scientific data using MATLAB or
      Python. bioRxiv. 2015 Jan 1:031658. doi: https://doi.org/10.1101/031658

    + DataJoint ([RRID:SCR_014543](https://scicrunch.org/resolver/SCR_014543)) -
      DataJoint for `<Select Python or MATLAB>` (version `<Enter version number>`)

+ DataJoint Elements
    + Yatsenko D, Nguyen T, Shen S, Gunalan K, Turner CA, Guzman R, Sasaki M, Sitonic D,
      Reimer J, Walker EY, Tolias AS. DataJoint Elements: Data Workflows for
      Neurophysiology. bioRxiv. 2021 Jan 1. doi:
      https://doi.org/10.1101/2021.03.30.437358

    + DataJoint Elements ([RRID:SCR_021894](https://scicrunch.org/resolver/SCR_021894))
      - Element Lab (version `<Enter version number>`)
