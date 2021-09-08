Configuration on standalone servers
===================================

To create a service that will run on a standalone service, rather than on a cloud-like platform such as NERSC Spin, run a RESTInG-based service, one may use the following procedure. It is assumed that the server has a working Docker installation, as on the computer on which the Docker images were generated for the Spin system.

#. Clone the RESTInG repository.

#. Create a project description file
   #. Set `platform = 'standalone'`.
   #. Set `secrets_directory` and `pgdata_directory` to directories on the host filesystem that are to contain the database password file and to store the data within the database, respectively.
   #. Set `ssl_certificate_file` and `ssl_certificate_key_file` to the locations of the SSL certificate and private key, within the Docker image; note that the contents of `webserver/ssl` directory of the repository are automatically and recursively copied onto the `/etc/ssl` directory in the Docker image.

#. Create a file named `password` within the `secrets_directory` specified above. This file should contain some plaintext password. Users will never have to reference this password directly. Both containers will automatically mount the directory to obtain access to the password.

#. Change to the `resting` directory within the repository.
   
#. Run `start.sh` to generate the basic service description files.

#. Perform any desired modifications to the service description files.

#. Run `finish.sh` to generate the Docker images.

#. Run `local_run.sh` to start the Docker containers on the present computer.

After the initial deployment of a website, database, and persistent storage through the Spin system, create a website administrator user account; this is specific to a Django website and is unrelated to NERSC user accounts.

#. Run `docker exec -it ws /bin/bash` to execute a shell in the container

#. In `/srv/website`, run

   #. `python manage.py makemigrations`

   #. `python manage.py migrate`      

   #. `python manage.py createsuperuser` and follow the prompts to create the account.

One can the log into the Django admin site `https://<server_name>/admin/` using this superuser account and create regular user accounts using the web interface.

Upon restarting the PostgreSQL workload, it may be necessary to execute a shell and execute `/custom_entry_point.sh`.

If one changes the project description file, such as by adding a new Django model, new database tables must be constructed. Ideally, these changes would be managed by the Django migration system. Unfortunately, we have found in practice that the system does not automatically detect the addition of a new model. If all else fails, it might be necessary to drop and initialize the database and to run `python manage.py migrate` once again, then upload the data once again, after creating the superuser account as before.

One should also set DEBUG = False in production.

..
   # Now deploy the images
   # To delete an existing database and start over, start a shell for the database workload and execute:
   # dropdb -U postgres postgres
   # createdb -U postgres postgres
   # For a new database, start a shell for the webserver and in /srv/website, run:
   # python manage.py makemigrations
   # python manage.py migrate
   # python manage.py createsuperuser
   # Then upload the initial metadata by going to the resting directory and running
   # python3 upload_csv.py
   The docker run -d -p 8000:8000 notation makes apache accessible after I start it from within the container. I don't have permission to access the resource, maybe some file doesn't exist. Presumably, we could run as root and map to port 80 instead. This is from the apache log: access to /api/ denied (filesystem path '/srv/website/website') because search permissions are missing on a component of the path; however, http://127.0.0.1:7000/static/acts/home/index.html works. The problem is likely to be the database or the secret. Also, want to force HTTPS wherever something sensitive might be transmitted. Maybe going to port 80 should just redirect.
   # might want to have the option of enforcing authenticated read access
