Initial service startup
=======================

After the initial deployment of a website, database, and persistent storage through the Spin system, create a website administrator user account; this is specific to a Django website and is unrelated to NERSC user accounts.

#. Select "Workloads" from the "Resources" menu, and select the "Workloads" tab.
   
#. Open the "three-dot" menu corresponding to the webserver workload.

#. Select "Execute Shell."

#. In the `/srv/website`, run

   #. `python manage.py makemigrations`

   #. `python manage.py migrate`      

   #. `python manage.py createsuperuser` and follow the prompts to create the account.

One can the log into the Django admin site `https://<server_name>/admin/` using this superuser account and create regular user accounts using the web interface.

Upon restarting the PostgreSQL workload, it may be necessary to execute a shell and execute `/custom_entry_point.sh`.

