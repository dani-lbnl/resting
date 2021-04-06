Customization
=============

This section discusses the required customization to be performed for any given application. Only a small amount of customization is needed for a basic database interface.

Customization is performed prior to building the website Docker image. While one can directly supply all of the typical Django description files in the `webserver/website` subdirectories (all files in this tree are copied into the image), this package provides a tool for generating default versions of these files using a simplified description supplied by the user.

Data description
----------------

Users supply the simplified website description in `utils/project.py`. The following variables must be defined:

 - `app_name`, the name chosen for the web interface Django app; this can be any name that is acceptable to Django

 - `models`, a Python dictionary that describes the data to be accessible through the web interface

The `models` dictionary has the format::

  { 
      ModelName_str : {
          ModelAttribute_str : {
             "type" : Instanciation_str,
             "filters" : [ FilterName_str, ... ]
          }, ...
      }, ...
  }

Each entry in the dictionary corresponds to a Django model / database table that will be automatically created. The key of each entry is a string that will be the model name. The value of each model entry is itself a dictionary with entries corresponding to the model attributes.

In these model attribute dictionaries, each entry corresponds to a single attribute. The key of each entry is a string that will name the attribute, and the value is a dictionary containing additional information about the attribute. Although the keys are specified as strings, it is important to note that the contents of the strings must be valid Python identifiers because of the way in which they are used to generate Python code.

Each of these attribute information dictionaries contains two entries. The key `'type'` is associated with the exact Django model field instanciation call that should appear in the model definition (it is assumed that a `from django.db import models` has been executed). The key `'filters'` is associated with a list of strings that are filter names defined by the Django REST Framework Filters package and which will be accessible in the corresponding filter forms.

Please note that arbitrary Python code could be included in the `'type'` strings and subsequently executed by Django from `models.py`; it is your responsibility to ensure that this code is safe.

As an example, this structure defines a database that stores only one type of Django model, named `Source`, with five different types of fields::

models = {
    'Source':{
        'patientid' : {
            'type' : 'models.CharField(max_length=32,blank=True)',
            'filters' : ['iexact','in','istartswith','icontains','iendswith','ir
egex','search'],
            },
	'age' : {
            'type' : 'models.IntegerField(null=True,blank=True)',
            'filters' : ['isnull','exact','gte','lte'],
            },
	'temperature' : {
            'type' : 'models.FloatField(null=True,blank=True)',
            'filters' : ['isnull','gte','lte'],
            },
	'url' : {
            'type' : 'models.URLField(max_length=256,blank=True)',
            'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'notes': {
            'type': 'models.TextField(max_length=1024,blank=True)',
            'filters': ['iexact','in','istartswith','icontains','iendswith','iregex','search']
            },
	}

In the `models` dictionary, there must be at least one model (such as the one in the above example) for which it is not necessary to specify any attributes mapping to other models. We will call these "independent" models. Other models which reference the independent models will be called "dependent" models. Data for independent models must be saved in the database before they can be referenced by dependent models. If the `models` descriptions allow relationship fields to be left blank (with `null = True, blank = True` field parameter settings in `project.py`), incomplete dependent model entries can be made and later updated. However, in most cases, it is likely to be more convenient to specify model relationships during the creation of ``later'' model instances. The relationships are expressed in the form of Django query calls, which we will discuss in detail later.
.. One can then specify all attributes of later models, including relationships to model records already stored in the database, in single files that can then be easily transformed into database records.

Although web interfaces generated as described above are immediately usable, the 'utils/drf_client.py` module contains code that simplifies programmatic access. With this module, users can easily establish authenticated connections to the database, and retrieve, store, and update information in the database. The necessary HTTP requests and the interpretation of responses are performed transparently by the module.

This module also allows bulk upload of records from comma-separated value (CSV) files. Plugins for reading additional file formats can be supplied by the user.

Each CSV file is assumed to contain records corresponding to a single type of model. We will first describe the upload of CSV files describing independent models or dependent modules that do not have required relationships to other models. Once these are stored, one can then load records from files corresponding to independent models that have required relationships to existing records, or update records in dependent modules with optional relationships.

In the client code that moves information from CSV files into databases, the following is assumed:

- Each CSV file holds records of only one type of model, although multiple files may be used as sources of records for an given model.
- The first line consists of header labels for the corresponding columns.
- Only columns with headers that exactly match model attribute names in `utils/project.py` contain information that is to be stored in the database, all other columns are ignored. CSV files do not have to contain headers that are optional (that is, with `null = True, blank = True` field parameter settings in `project.py`).

As a consequence of these assumptions, the model descriptions in `project.py` can describe everything from a superset of all model attributes contained in multiple CSV files, to an intersection of model attributes contained in multiple CSV files.

Users will often need to write small programs to make data files consistent with the expected format. Example programs used in the ACTS project can be found in the `acts` directory of the repository. These programs change header names and add columns describing image thumbnail locations, and also find maximum field lengths to inform the model field definitions. The `generate_Source_description.py` program creates a dictionary containing all available attributes and places it in `project_Source.py`, which one can complete to describe the `Source` model.

.. With these modifications and the specification of model descriptions, users can choose to store records drawn from multiple files that contain anything from a common subset of the attributes contained all files to a superset of attributes found in all files. 

For dependent models, it is likely to be convenient to provide information establishing these relationships in the data files along with other model attribute data. For these relationship attributes, the CSV files can contain strings that contain executable Python code return model instances (for a `OneToOneField`) or Django QuerySet (for a `ForeignKey` or `ManyToManyField`). These are automatically executed and the models are connected when the later model instances are created.

Please note that arbitrary Python code could be included in these relationship strings; it is your responsibility to ensure that this code in the CSV strings is safe.

Running `utils/generate_drf_site.py` then creates default `models.py`, `serializers.py`, `views.py`, and `urls.py` files to describe the website, and writes them into their proper locations in the website description directories.

After these files are generated, one can immediately run the `build.sh` script in the 'webserver' directory to build the website Docker image, and then push the container to the Spin repository for deployment.

