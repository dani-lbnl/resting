Python client module
====================

Although web interfaces generated as described above are immediately usable, the ``resting/rest_client.py`` module contains code that simplifies programmatic access. With this module, users can easily establish authenticated connections to the database, and retrieve, store, and update information in the database. The necessary HTTP requests and the interpretation of responses are performed transparently by the module.

This module also allows bulk upload of records from comma-separated value (CSV) files. Plugins for reading additional file formats can be supplied by the user.

Each CSV file is assumed to contain records corresponding to a single type of model. We will first describe the upload of CSV files describing independent models or dependent modules that do not have required relationships to other models. Once these are stored, one can then load records from files corresponding to independent models that have required relationships to existing records, or update records in dependent modules with optional relationships.

In the client code that moves information from CSV files into databases, the following is assumed:

- Each CSV file holds records of only one type of model, although multiple files may be used as sources of records for an given model.
- The first line consists of header labels for the corresponding columns.
- Only columns with headers that exactly match model attribute names in ``resting/project.py`` contain information that is to be stored in the database, all other columns are ignored. CSV files do not have to contain headers that are optional (that is, with ``null = True, blank = True`` field parameter settings in ``project.py``).

As a consequence of these assumptions, the model descriptions in ``project.py`` can describe everything from a superset of all model attributes contained in multiple CSV files, to an intersection of model attributes contained in multiple CSV files.

Users will often need to write small programs to make data files consistent with the expected format. In the simplest cases, this might simply involve rewriting header lines.

.. Example programs used in the ACTS project can be found in the ``acts`` directory of the repository. These programs change header names and add columns describing image thumbnail locations, and also find maximum field lengths to inform the model field definitions. The ``generate_Source_description.py`` program creates a dictionary containing all available attributes and places it in ``project_Source.py``, which one can complete to describe the ``Source`` model.

.. With these modifications and the specification of model descriptions, users can choose to store records drawn from multiple files that contain anything from a common subset of the attributes contained all files to a superset of attributes found in all files. 

For dependent models, it is likely to be convenient to provide information establishing these relationships in the data files along with other model attribute data. For these relationship attributes, the CSV files can contain strings that represent queries; when the dependent model instances are created, these queries are performed, and the filter results are used as field values.

