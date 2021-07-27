PostgreSQL Docker image
=======================

PostgreSQL (Postgres) appears to be the recommended production-level database for use with Django.

A Docker container that includes Postgres will run under Spin and be available to the Docker container running the Django-based website.

There are official Docker images for recent versions of Postgres, and much configuration can be done by setting environmental variables; it may not be necessary to create a custom image. Spin obtains images directly from DockerHub by default, although to avoid extra downloads, the stock images can be pushed to `registry.nersc.gov`.

However, in our particular case, it is convenient to add custom files to the official Postgres image.

.. |tag| replace:: ``registry.nersc.gov/m3670/acts_postgres:12``

This repository includes a Dockerfile that obtains a recent Postgres image and copies in files. In the ``postgres`` directory within the respository, the ``build.sh`` script builds the Docker image, with the tag |tag|.

To move the Docker image to ``registry.nersc.gov``, making it accessible to Spin, one can locally execute

``docker login registry.nersc.gov``

followed by

``docker push`` |tag|

Cory Snavely noted that Spin automatically restarts containers if there is no response to an automated health check request. For this reason, the entry point is a custom script. If the database has already been initialized, the script starts the database server.

As Cory has also noted, a container only runs for as long as the entry point is running. For this reason, the script executes a shell, which waits because the container is intended to be run with the ``-it`` options. 

The database should not be created until storage and secrets are available through the Spin system. The database container will create a database automatically upon startup if a database does not already exist. In order to clear the database, one can execute a shell from Spin and run

``dropdb -U postgres postgres``

and

``createdb -U postgres postgres``

Access to the database server is described in the Django configuration section of this documentation.

