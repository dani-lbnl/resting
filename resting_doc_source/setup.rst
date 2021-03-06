Setup
=====

To use RESTInG to deploy a service, one first works from a computer (the "development system") to be used to build images containing the service software. At present, RESTInG will work with Docker and Podman.

These systems are not needed until one is ready to deploy the data management service, following project-specific customization, but it is probably preferable to determine if they can be properly installed on the development system before starting the customization process.

Docker is presently required for deployment on NERSC Spin and will work on standalone systems. Please note that use of Docker Desktop may require a paid Docker subscription.

The Podman option is only available for standalone systems running Linux. We understand that it is possible to run Linux virtual machines on Windows and Mac systems, although we have not tested this. Unfortunately, due to a bug that might be resolved in later versions than presently available through Debian 11 (see https://github.com/containers/podman/issues/11457#issuecomment-916260531), the containers cannot communicate properly. This can be repaired manually as described below.

Docker
------

On a Windows or Mac computer, go to https://docs.docker.com/get-docker/ and follow the appropriate Docker Desktop installation directions, then start Docker Desktop. 

On the Debian 10 computer on which RESTInG was developed, it was necessary to install the docker.io package, which can be done by running as root::

  apt-get install docker.io

On Debian 11, one might run::

  apt install docker.io

It is safest to run Docker using sudo; it may be necessary to run a command such as the following as root to gain sudo privileges::

  adduser <username> sudoers
  
Then as outlined at https://docs.docker.com/get-started/ , one can confirm that Docker is installed properly::

  sudo docker run hello-world
  sudo docker image ls
  sudo docker ps --all

The following sections describe the Docker image customization procedure in detail. A summary of the procedure appears at the end of this chapter.

Note that the ``project.py`` file (to be described later) should include the following line::

  engine = 'docker'

Podman
------

Podman is available under Debian 11, and can be installed by running as root::

  apt install podman

It should not be necessary to modify /etc/containers/registries.conf because the Docker Hub registry is explicitly given in the generated Dockerfiles.
  
Note that the ``project.py`` file (to be described later) should include the following line::

  engine = 'podman'

Unfortunately, the hostnames given to the containers are not automatically availble; this can be fixed by first finding the IP address assigned to the database container::
  sudo podman container inspect db | fgrep IPAddress

and then starting a shell in the webserver container::

  sudo podman exec -it ws /bin/bash

and appending an entry for the database server to the ``/etc/hosts``::

  echo '<IP address of database container> db db' >> /etc/hosts

after which one can initialize the system as usual, as described in the next chapter. This process might be automated at a later time.
  
Testing RESTInG
---------------

Within the RESTInG repository, one can directly supply all of the typical Django description files in the ``webserver/website`` subtree (all files in this tree are copied into the image). However, RESTInG provides a tool for generating default versions of these files from a simple description file, ``resting/project.py``. The ``resting/project.py`` file included in the repository can be used to generate a service that runs locally and which can be used as a basis for automated testing. Most users will not need to run these tests; they are aimed at assisting RESTInG developers. The "resting/test.sh" script builds the Docker images for local use. 

Project data declaration
------------------------
  
The ``resting/project.py`` file should be customized the needs of one's project before using RESTInG to generate the files that describe the data management service. This file is imported by RESTInG scripts, which expect the following variables to be defined within ``resting/project.py``:

 - ``app_name``, the name chosen for the web interface Django app; this can be any name that is acceptable to Django and is only used internally

 - ``server_name``, the fully-qualified domain name at which the data management service will be accessible

 - ``api_prefix``, a string that precedes all references to the Django REST Framework API; for example, specifying ``api`` would cause all API references to begin with ``https://<server_name>/api/``

 - ``index_template``, the filename of the Django template (in the ``resting/website/templates/`` directory) which will be rendered into the site homepage; if left blank, a GET request to the root URL for the site will redirect to the Django REST Framework site

 - ``models``, a Python dictionary that describes the data to be accessible through the web interface, described in detail in the upcoming subsection.

 - ``engine``, which should be set to ``'docker'`` or ``'podman'``; Note that podman is presently only available on Linux systems
   
 - ``platform``, which should be set to ``'spin'`` for deployment on NERSC Spin, or ``'linux'``, ``'mac'``, or ``'cygwin'`` as appropriate for deployment to a standalone server. For standalone deployment, the following variables must also be set:

   - ``secrets_directory``, a directory name expressed relative to the root directory of the repository, in which one must provide a file named ``password``, which contains only the plaintext password used for communication between the website container and the PostgreSQL container

   - ``pgdata_directory``, a directory name expressed relative to the root directory of the repository, which will be used as a working directory by the PostgreSQL container

   - ``ssl_certificate_file``, the name of the SSL certificate file, which must be placed in the ``webserver/ssl/certs`` subdirectory of the repository

   - ``ssl_certificate_key_file``, the name of the SSL certificate key file, which must be placed in the ``webserver/ssl/certs`` subdirectory of the repository

The `models` dictionary
^^^^^^^^^^^^^^^^^^^^^^^
   
The ``models`` dictionary has the format::

  { 
      ModelName_str : {
          ModelAttribute_str : {
             "type" : Instanciation_str,
             "filters" : [ FilterName_str, ... ]
          }, ...
      }, ...
  }

Each entry in the dictionary corresponds to a Django model, which might be thought of as a separate database table, that will be automatically created. The key of each entry is a string that will be the model name; the contents of the string must be a valid Python identifier and must not contain a sequence of two underscores, since those are interpreted as filters. The value of each model entry is itself a dictionary with entries corresponding to the model attributes.

In these model attribute dictionaries, each entry corresponds to a single attribute. The key of each entry is a string that will name the attribute, and the value is a dictionary containing additional information about the attribute. Although the keys are specified as strings, it is important to note that the contents of the strings must be valid Python identifiers because of the way in which they are used to generate Python code.

Each of these attribute information dictionaries contains two entries. The key ``'type'`` is associated with the exact Django model field instanciation call that should appear in the model definition (it is assumed that a ``from django.db import models`` has been executed). The key ``'filters'`` is associated with a list of strings that are filter names defined by the Django REST Framework Filters package and which will be accessible in the corresponding filter forms.

.. Please note that arbitrary Python code could be included in the ``'type'`` strings and subsequently executed by Django from ``models.py``; it is your responsibility to ensure that this code is safe.

As an example, this structure defines a database that stores only one type of Django model, named ``Source``, with five different types of fields::

  models = {
      'Source':{
          'patientid' : {
              'type' : 'models.CharField(max_length=32,blank=True)',
              'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
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
    }
	
In the ``models`` dictionary, there must be at least one model (such as the one in the above example) for which it is not necessary to specify any attributes mapping to other models. We will call these "independent" models. Other models which reference the independent models will be called "dependent" models. Data for independent models must be saved in the database before they can be referenced by dependent models. If the ``models`` descriptions allow relationship fields to be left blank (with ``null = True, blank = True`` field parameter settings in ``project.py``), incomplete dependent model entries can be made and later updated. However, in most cases, it is likely to be more convenient to specify model relationships during the creation of later model instances. The relationships are expressed in the form of Django query calls, which we will discuss in detail in the chapter desribing the Python client module.
.. One can then specify all attributes of later models, including relationships to model records already stored in the database, in single files that can then be easily transformed into database records.

Finishing customization
-----------------------

After customizing the ``resting/project.py`` file, run a command such as ``./start.sh`` or ``sh start.sh`` from within the ``resting`` subdirectory of the repository. This generates Python files that describe the website, such as ``models.py``, ``serializers.py``, ``views.py``, and ``urls.py``, and writes them into their proper locations in directories within the ``webserver/website`` tree. One may then edit and customize these files as with a manual installation of Django REST Framework, although the default files are sufficient to provide a data management service that will be appropriate for most needs. This is the appropriate moment to copy templates into the ``webserver/website/templates`` subdirectory, or static files into the ``webserver/website/<app_name>/static/<app_name>`` subdirectory, or TLS certificate and certificate key files and the password file into the directories specified in ``resting/project.py``, for a standalone server. For a production server, one should uncomment ``DEBUG = False`` at the end of ``webserver/website/website/sed_script_settings.py``

One then runs a command such as ``./finish.sh`` or ``sh finish.sh`` from within the ``resting`` subdirectory. This generates the documentation for the data management service, builds the database and website Docker images, and for a NERSC Spin deployment, pushes these images to the NERSC registry.

For deployment on NERSC Spin or a standalone server, please continue with the instructions provided in the corresponding chapter.

Docker image generation summary
-------------------------------
The following is a summary of the procedure is used to generate Docker images that describe the data management service and to push these to the NERSC Spin registry, if appropriate.

#. Clone the RESTInG repository.

#. For deployment on NERSC Spin set ``platform = 'spin'`` in project description file ``resting/project.py``
   
#. For deployment on a standalone server (DNS records and TLS certificates will be discussed specifically for Spin in the Spin deployment chapter):
   
   #. Request creation of an appropriate DNS record; users with LBNL affiliation can go to https://iprequest.lbl.gov/ to submit a request. An A+PTR record is a typical choice.
      
   #. Generate an SSL/TLS certificate request

      #. Run ``generate.sh`` in the ``certificate`` directory, entering relevant identifying information
	 
      #. Or on a system with openssl run a command such as ``openssl req -new -newkey rsa:2048 -nodes -addext "subjectAltName = DNS:<development_server_name>" -keyout <server_name>.key -out <server_name>.csr``

   #. Request an SSL/TLS certificate; users with LBNL affiliation can use the following procedure:

      #. Go to https://certificates.lbl.gov/

      #. Paste the contents of the ``<server_name>.csr`` file into the text box and submit

      #. Once approved, download the "Certificate (w/ chain), PEM encoded" from the link received by e-mail

      #. Reorder the contents of the certificate file, removing the first certificate and inverting the order of all others

   #. In project description file ``resting/project.py``,
	 
      #. Set ``platform = 'standalone'`` and
      
      #. Set ``secrets_directory`` and ``pgdata_directory`` to directories on the host filesystem that are to contain the database password file and to store the data within the database, respectively; by default, these are the ``secrets`` and ``pgdata`` subdirectories within the repository
      
      #. Set ``ssl_certificate_file`` and ``ssl_certificate_key_file`` to the locations of the SSL certificate and private key, within the Docker image; note that the contents of ``webserver/ssl`` directory of the repository are automatically and recursively copied onto the ``/etc/ssl`` directory in the Docker image.

   #. Create a file named ``password`` within the ``secrets_directory`` specified above. This file should contain some plaintext password. Users will never have to reference this password directly. Both containers will automatically mount the directory to obtain access to the password.

#. Change to the ``resting`` directory within the repository.
   
#. Run ``start.sh`` to generate the basic service description files.

#. Perform any desired modifications to the service description files.

   #. For a production server, one should uncomment ``DEBUG = False`` at the end of ``webserver/website/website/sed_script_settings.py``

#. Run ``finish.sh`` to generate the Docker images (and to push them to the NERSC registry for deployment on NERSC Spin).
