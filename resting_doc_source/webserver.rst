Web server Docker image
=======================

The ``webserver`` directory of our Bitbucket repository serves as the Docker "context" for the image containing the web server and website, except for the database component. It contains ``Dockerfile``, which describes the building of the image.

We can follow https://docs.docker.com/develop/develop-images/dockerfile_best-practices/ when constructing the ``Dockerfile``. In addition, Cory Snavely has recommended that we avoid dependence on specific base image versions and chain commands rather than running them with a sequence of directives.

We will start with the official Python 3 image, which also contains Django. Upon examination, this image appears to contain a Debian 10 (Buster) system, so one can view packages that are available through ``apt-get`` at http://www.debian.org . After Python 3 installation, our Dockerfile triggers the update of the list of available packages and then the installation of Django REST framework, the Apache 2 web server, a WSGI library, and a 3rd party filter library for Django REST framework::

  RUN apt-get update && apt-get -y install python3-djangorestframework apache2 libapache2-mod-wsgi-py3 python3-djangorestframework-filters

In a normal Debian installation, the Python packages installed through ``apt-get`` are usually immediately available through a Python ``import`` statement. This was not the case for the Docker Python 3 image; it was necessary to set the ``PYTHONPATH`` environmental variable::

  ENV PYTHONPATH /usr/lib/python3/dist-packages

Customized Apache configuration files, describing the setup that we now discuss, are copied into the image. Most of the configuration is specified in ``/etc/apache2/apache2.conf``, which has been included in this repository.

Under Spin, it is recommended that the Spin system handles SSL connections; one reason is that containers do not have to be changed if SSL software is updated, this is done at the Spin level. Under this approach, the Spin system accepts SSL connections and handles the certificate machinery, then passes requests along to the container as HTTP requests. Since SSL is not enabled by default in the Apache installation, there is no need to change this. Also, as discussed elsewhere in this documentation, certificates can be obtained through LBNL.

Apache can be directed to listen to a higher port number than the HTTP default of 80 so that privileged access is not needed. A modified version of ``/etc/apache2/ports.conf`` that directs Apache to listen on port 8000 rather than 80 is included in this repository.

Note that if we were to use the Django test server, which defaults to listening for loopback connections, one will instead execute a command such as::

  python manage.py runserver 0.0.0.0:8000

Apache is listening to port 8000 "inside" of the container, but that "container" port must be exposed and mapped to a "host" port of the host system. Although IP interfaces are automatically created for a running container, it does not appear to the host system that the server is listening on the specified container port on a newly created IP interface, but the server running in the container is accessible through the mapped host port on the host system. It is also accessible through the same host port number on the container IP address, which surprised me.

The Dockerfile then directs the creation of a Django website, copies custom code describing the website into the image, and then connects the website to the database. Since the website and database are running in separate containers, the setup is different from a situation in which both are running "natively" on the same system.

The ``settings.py`` file in the Django installation must be modified to use PostgreSQL rather than the default SQLite, and it must be directed to access the database server in another container.

.. |secrets_directory| replace:: ``/secrets``
.. |database_password_key| replace:: ``password`` 
.. |database_password_path| replace:: ``password``

As described in the Spin configuration, the secret, which is attached to both the Postgres container filesystem and the web server container filesystem in the same locations, is simply a text file located at |secrets_directory|/ |database_password_path|/ |database_password_key|. The custom ``settings.py`` file directs Python to read this file to obtain the database password.

Finally, as Cory noted, when a container is run and starts its entry point command, the process should continue in the foreground in order to prevent Spin from exiting. This is specifed to Docker as::

  CMD ["/usr/sbin/apache2ctl","-DFOREGROUND","-kstart"]

Unlike in a normal Debian installation, installation of a server package does not usually mean that the service is automatically started when a container is started.
  
To start a container and have the web server within accessible on port 80 of the host, one might run (with privileged access)::

  docker run -p 80:8000 <image name>

The ``build.sh`` script builds the Docker image as
  
.. Apache starts at root, switches to apache user
.. run with minimum capabilities in case someone hacks service
.. add: NET_BIND_SERVICE (global file system), otherwise same as example
