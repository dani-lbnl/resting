Additional information about the PostgreSQL Docker image
========================================================

PostgreSQL (Postgres) appears to be the recommended production-level database for use with Django.

A Docker container that includes Postgres will run under Spin and be available to the Docker container running the Django-based website.

In our particular case, it is convenient for RESTInG to add custom files to the official Postgres image. In the ``postgres`` directory within the respository, the ``build.sh`` script builds the Docker image, although it will not usually be necessary for users to run this directly.

Cory Snavely noted that Spin automatically restarts containers if there is no response to an automated health check request. For this reason, the entry point is a custom script. If the database has already been initialized, the script starts the database server.

As Cory has also noted, a container only runs for as long as the entry point is running. For this reason, the script executes a shell, which waits because the container is intended to be run with the ``-it`` options. 

The database should not be created until storage and secrets are available through the Spin system. The database container will create a database automatically upon startup if a database does not already exist. In order to clear the database, one can execute a shell from Spin and run

``dropdb -U postgres postgres``

and

``createdb -U postgres postgres``

Once this is done, one must perform the steps in the initial startup procedure since all database information has been erased.

Access to the database server is described in the Django configuration section of this documentation.

If one changes the project description file, such as by adding a new Django model, new database tables must be constructed. Ideally, these changes would be managed by the Django migration system. Unfortunately, we have found in practice that the system does not automatically detect the addition of a new model. If all else fails, it might be necessary to drop and initialize the database and to run `python manage.py migrate` once again, then upload the data once again, after creating the superuser account as before.

Upon restarting the PostgreSQL workload, it may be necessary to execute a shell and execute `/custom_entry_point.sh`.
