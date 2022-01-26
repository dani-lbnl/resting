Deployment on a standalone server
=================================

We assume that all steps in the Setup chapter have been performed for running on a standalone server. We assume that the server has a working Docker installation, as on the computer on which the Docker images were generated for the Spin system, and that the server is on a network on which it is visible to all intended clients.

#. From the ``resting`` subdirectory of the repository, run ``run.sh`` to start the Docker containers on the present computer.

#. Run ``docker exec -it ws /bin/bash`` to execute a shell in the container

#. In ``/srv/website``, run:

   #. ``python manage.py makemigrations``

   #. ``python manage.py migrate``      

   #. ``python manage.py createsuperuser`` and follow the prompts to create the account; this is specific to a Django website. One can the log into the Django admin site ``https://<server_name>/admin/`` using this superuser account and create regular user accounts using the web interface.

#. Network-specific and system-specific configuration might be needed in order to make the web service available to other computers. For example, on a Linux host without a firewall, one can make the services accessible to any other computer (assuming that incoming traffic is being properly routed to your computer) by editing ``/etc/hosts.allow`` and appending ``80, 443: ALL``
      
#. Run ``resting/stop.sh`` to stop the Docker containers, or ``resting/stop_db.sh`` and ``resting/stop_ws.sh`` to stop the database and web server containers separately.

#. Run ``resting/rerun.sh`` to stop and rerun the Docker containers, or ``resting/rerun_db.sh`` and ``resting/rerun_we.sh`` to stop and rerun the database and web server containers separately. This is useful in using newly generated Docker images to replace older containers.

#. Run ``resting/rm.sh`` to remove the Docker containers, or ``resting/rm_db.sh`` and ``resting/rm_ws.sh`` to remove the database and web server containers separately.
      
..
 Upon restarting the PostgreSQL workload, it may be necessary to execute a shell and execute ``/custom_entry_point.sh``.

 If one changes the project description file, such as by adding a new Django model, new database tables must be constructed. Ideally, these changes would be managed by the Django migration system. Unfortunately, we have found in practice that the system does not automatically detect the addition of a new model. If all else fails, it might be necessary to drop and initialize the database and to run ``python manage.py migrate`` once again, then upload the data once again, after creating the superuser account as before.

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

