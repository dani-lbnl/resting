Application to COVID-19 results
===============================

This section describes the application of the website infrastructure for our COVID-19 project. The amount of work required for specialization to a typical application should be fairly small, since using a class-based approach with Django and Django REST Framework automatically invokes a lot of library code.

The Django models (corresponding to database tables) and class-based serializers and views are defined in the files within the `webserver/website/database` directory. The model fields are based on the information provided in `metadata/metadata_ieee8023.csv`; the Pandas-based program `metadata/move.py` was used to look through the metadata file and generate a rough model description in `metadata/models.py`, which was then modified as needed and saved to the `webserver/website/database` directory.

There are currently three models. The built-in Django `User` model is present for website authentication and is also referenced from the other models to track creators. The `Image` model contains starting image metadata, including filesystem locations. The `Result` model connects these starting images to files that store calculation results. Additionally, this model contains metadata about the calculations used to generate the results.

Since user authentication is required to store data in the database through the REST interface, customization begins with the creating of user accounts.

After the initial deployment of a website, database, and persistent storage through the Spin system, create a website administrator user account; this is specific to a Django website and is unrelated to NERSC user accounts.

#. Select "Workloads" from the "Resources" menu, and select the "Workloads" tab.
   
#. Open the "three-dot" menu corresponding to the webserver workload.

#. Select "Execute Shell."

#. In the `/srv/website`, run

   #. `python manage.py makemigrations`

   #. `python manage.py migrate`      

   #. `python manage.py createsuperuser` and follow the prompts to create the account.

One can the log into the Django admin site `https://covidscreen.lbl.gov/admin/` using this superuser account and create regular user accounts using the web interface. It is also possible to create a web interface to allow new users to self-register, but we have not implemented this at present and it is not yet clear if that would be desirable.

Once user accounts exist, they can be associated with `Image` and `Result` data entries.

Since Django might create entries in the database beyond those in the model description, it is safest to only add information to the database through the web interface. The `metadata/store_metadata.py` program reads the metadata stored in the `metadata/metadata_ieee8023.csv` file, obtains an authentication token from the website, converts entries into appropriate data types, packages each record in a JSON format, and with separate requests, sends each record for storage in the database.

As the database grows larger, it can be expensive to send and render all of its records. For this reason, empty Django QuerySets are returned when no query parameters are provided. One can still retrieve all records by specifically creating queries that do not exclude any records (such as specifying 'Unknown' on an `isnull` field).

Typically, an HTML page will include `img` tags containing URLs that return individual images. Presently, the CFS directories are mounted read-only at `/srv/static/`. For security, only image files that are specifically associated with a `Result` record should be accessible. For this reason, the Django URL dispatcher has been configured to recognize sets of URLs that reference `Result` records; in response, images associated with the stored records are sent. These URLs can then be incorporated into higher-level webpages that might be associated with class-based Django `Views`.

It appears that upon restarting the PostgreSQL workload, it is necessary to execute a shell and execute `/custom_entry_point.sh`, although this is listed as the `CMD` in the Dockerfile.

When the model definitions change, `python manage.py makemigrations` and `python manage.py migrate` do not always seem to make the necessary database corrections. Some custom programming might be necessary. However, when the amount of metadata is relatively small, it might be more convenient to rebuild the entire system.
