Deployment on NERSC Spin
========================

.. docker image: registry url
.. namespace: appear like folders within project
.. path: different workloads associated with same hostname

Adapting the procedure given in the `SpinUp Workshop for New Users.pdf` slides:

.. |project_id| replace:: ``<project_id>``
.. |namespace| replace:: ``<namespace>``
.. |database_image| replace:: ``registry.nersc.gov/`` |project_id| ``/<app_name>_postgres:12``
.. |database_password_name| replace:: ``db-password``
.. |database_password| replace:: <choose-any-valid-passwordfill-in-database-password>
.. |secrets_directory| replace:: ``/secrets``
.. |database_password_key| replace:: ``password`` 
.. |database_password_path| replace:: ``password``
.. |database_volume_name| replace:: ``postgres``
.. Default				    
.. |pgdata| replace:: ``/var/lib/postgres/data``
.. Default		  
.. |database_volume_mount_point| replace:: ``/var/lib/postgres``
.. This is critical, as settings.py needs to know the hostname (it will be "db")
.. |database_workload| replace:: ``db``
.. |webserver_workload| replace:: ``webserver``
.. |ingress_name| replace:: ``lb``				  
.. |hostname| replace:: |ingress_name|. |namespace| ``.development.svc.spin.nersc.org``
.. .. |hostname| replace:: |ingress_name|. |namespace| ``.production.svc.spin.nersc.org`

.. |webserver_image_tag| replace:: ``registry.nersc.gov/`` |project_id| ``/webserver:version``
.. |certificate_name| replace:: ``certificate``
.. Default			
.. |postgres_user| replace:: ``postgres``
.. |cname| replace:: ``<server_name>``
.. |key_file| replace:: |cname| ``.key``
.. |certificate_file| replace:: ``covidscreen_lbl_gov.cer``
.. |reordered_certificate_file| replace:: ``reordered_covidscreen_lbl_gov.cer``
.. |cfs_path| replace:: ``/global/cfs/cdirs/`` |project_id| ``/CXR/``
.. .. |source_thumbnail_path| replace:: ``/global/cfs/cdirs/`` |project_id| ``/www/CXR``
.. |source_thumbnail_path| replace:: ``/global/cfs/projectdirs/`` |project_id| ``/CXR``
			           
.. These are default values
..      * POSTGRES_USER = |postgres_user|     
..      * POSTGRES_DB = |postgres_user|
..   #. Expand the "Command" panel, confirm that "Interactive & TTY" is selected in the "Console" section

.. #. Set ``platform = 'spin'`` in the project description file and build the Docker images locally.
   
..
   #. Push those images to ``registry.nersc.gov``
      #. Open a session by running ``docker login registry.nersc.gov``
      #. Give images suitable names by running commands of the form ``docker tag <image> registry.nersc.gov/`` |project_id| ``/<image>:<version>``
      #. Or if the images will be run only using Spin, one can use the shortcut ``docker build -t registry.nersc.gov/`` |project_id| ``/<image>:<version>``
      #. Push the PostgreSQL image by running ``docker push`` |database_image|
      #. Push the web server image by running ``docker push`` |webserver_image_tag|
      #. Note that images can be managed by visiting ``registry.nersc.gov`` from a web browser
      
#. Log into Rancher 2 with Shibboleth at https://rancher2.spin.nersc.gov/

#. Select the appropriate project ID from the "development" or "production" drop-down menu

#. Create a namespace

   #. Click "Namespace", click "Add Namespace", set

      * Name: |namespace|

   #. Click "Create"

#. Create a "secret" to enable the web server container to access the Postgres container without leaving a password exposed in environment variables.
   
   #. Select "Secrets" from the "Resources" drop-down menu, click "Add Secrets, select "Available to a single namespace", select |namespace|
   #. Set the following values
      
      * Name: |database_password_name|
      * Key: |database_password_key|

   #. For "Value," you may enter any valid password. There is no need to remember it or reenter it anywhere.

   #. Click "Save"   
      
#. Create the database workload

   #. Select "Workloads" from the "Resources" drop-down menu, click "Deploy" and set

      * Name: |database_workload|
      * Image: |database_image|
     
   #. Set

      * Namespace: |namespace|
   
   #. Expand the "Environment Variables" panel, click the "Add Variable" button to enter

      * ``PGDATA`` = |pgdata|     
      * ``POSTGRES_PASSWORD_FILE`` = |secrets_directory|\/|database_password_path|

   #. Attach the secret to the database container filesystem
   
      #. Click "Volumes", click "Add Volumes", click "Use a Secret", select

	 * Secret: |database_password_name|
	   
      #. Check "Select Specific Keys", click |database_password_key|, set

	 * Key: |database_password_key|
	 * Path: |database_password_path|
	 * Mode: 444  
	
      #. Set "Mount Point" to |secrets_directory|

   #. Set up an NFS volume for persistent storage

      #. In the "Volumes" panel, click "Add Volumes", click "Add a new persistent volume (claim)"
	 
      #. Set

	 * Name: |database_volume_name|
	 * Source: "Use a Storage Class to provision a new persistent volume"
	 * Storage class: "nfs-client"
	 * Capacity: "1 GiB"

      #. Click "Define"

      #. Set

	 * Mount point: |database_volume_mount_point|

   #. Click "Save"      
      
   #. Click on "Show advanced options" at the bottom of the page

   #. Expand the "Security & Host Config" panel
	
   #. Under "Add Capabilities", select by control-click:
     
      * CHOWN
      * DAC_OVERRIDE
      * FOWNER
      * SETGID
      * SETUID
     
   #. Under "Drop Capabilities", select "ALL".

   #. Click "Launch" and wait for all pod (running instance of a workload) indicators to turn green.

   #. Note that this container will be accessible to other Spin containers at the FQDN |database_workload|.svc.cluster.local
      
#. Create the web server workload

   #. Select "Workloads" from the "Resources" drop-down menu, click "Deploy" and set

      * Name: |webserver_workload|
      * Image: |webserver_image_tag|
     
   #. Set

      * Namespace: |namespace|
   
   #. Expand the "Environment Variables" panel, click the "Add Variable" button to enter
	 
      * POSTGRES_PASSWORD_FILE = |secrets_directory|\/|database_password_path|

   #. Expand the "Volumes" panel

      #. Click on "Add Volume", click "Use a secret"
      
      #. Set
	 
	 * Secret: |database_password_name|

      #. Select

	 * "Select Specific Keys"

      #. Set
	 
	 * Key: |database_password_key|
	 * Path: |database_password_path|
	 * Mode: 444

      #. Select
	 
	 * "Read-Only"

      #. Set

	 * Mount: |secrets_directory|

      #. Click on "Add Volume", click "Bind-mount a directory from the node"

      #. Set

	 * Path on the Node: |cfs_path|
	 * The Path on the Node must be: ``An existing directory``
	 * Mount Point: /srv/static/nersc
	 * Read-Only: Checked  

      #. Click on "Add Volume", click "Bind-mount a directory from the node"

      #. Set

	 * Path on the Node: |source_thumbnail_path|
	 * The Path on the Node must be: ``An existing directory``
	 * Mount Point: /srv/thumbnails
	 * Read-Only: Checked  
	 
   #. Click on "Show advanced options" at the bottom of the page

      #. Expand the "Command" panel

      #. Set the appropriate values (determined by NERSC project) for

	 * User ID
	 * Filesystem Group
      
      #. Expand the "Security & Host Config" panel

      #. Set

	 * Run as Non-Root: Yes
      
      #. Under "Add Capabilities", select only "NET_BIND_SERVICE"
     
      #. Under "Drop Capabilities", select "ALL".

   #. Click "Launch" and wait for all pod indicators to turn green.

   #. One should now perform the Django initialization. Open the "Resources" drop-down menu, select "Workloads", then click the "three-dot" menu next to the |webserver_workload| workload, execute a shell, move to the `/srv/website` directory, and execute

      #. `python manage.py makemigrations`
      #. `python manage.py migrate`
      #. `python manage.py createsuperuser`
      
#. Request creation of a CNAME

   #. Go to https://iprequest.lbl.gov/ and request CNAME |cname| as an alias for FQDN |hostname| (ignore any spaces appearing here)
      
#. Generate an SSL/TLS certificate request

   #. Run ``generate.sh`` in the ``certificate`` directory, entering relevant identifying information
   #. Or on a system with openssl run a command of the form::
      
      openssl req -new -newkey rsa:2048 -nodes -addext "subjectAltName = DNS:covidsceen-dev.lbl.gov" -keyout covidscreen.lbl.gov.key -out covidscreen.lbl.gov.csr

#. Request an SSL/TLS certificate

   #. Go to https://certificates.lbl.gov/

   #. Paste the contents of the ``covidscreen.lbl.gov.csr`` file into the text box and submit

   #. Once approved, download the "Certificate (w/ chain), PEM encoded" from the link received by e-mail

   #. Reorder the contents of the certificate file, removing the first certificate and inverting the order of all others
      
#. Add an SSL/TLS certificate
      
   #. Select "Secrets" from the "Resources" drop-down menu, select the "Certificates" tab, click "Add Certificate", set

      * Name: |certificate_name|

   #. Select "Available to a single namespace", set

      * Namespace: |namespace|

   #. Under "Private Key", click "Read from a file", choose file |key_file|.

   #. Under "CA Certificate", click "Read from a file", choose file |reordered_certificate_file|

   #. Click "Save"
      
#. Add an ingress

   #. Select "Workload" from the "Resources" drop-down menu, select the "Load Balancing" tab, click "Add Ingress", set

      * Name: |ingress_name|
      * Namespace: |namespace|

   #. Select "Specify a hostname to use", set

      * Request Host: |hostname| (ignore any spaces appearing here)
	
   #. Set

      * Target: |webserver_workload|
      * Port: 8000

   #. Click "Add Rule"

   #. Select "Specify a hostname to use", set

      * Request Host: |cname|
	
   #. Set

      * Target: |webserver_workload|
      * Port: 8000
      
   #. Expand the "SSL/TLS Certificates" panel, click "Add Certificate", select
      
      * Choose a certificate
      * Certificate: |certificate_name|
      * Host: |cname|    
      * Available to a single namespace
      * Namespace: |namespace|

   #. Click "Save"
	
..
      #. Click on "Add Volume", click "Bind-mount a directory from the node", set

	 * Path on the Node:
	 * The Path on the Node must be: An existing directory
	 * Mount Point: |bind_mount_point|
	
      #. Select
      
	 * "Read-Only"

#. It might take several minutes before the Spin NGINX reverse proxy server allows web connections to the |webserver_workload| container.

#. After the initial deployment of a website, database, and persistent storage through the Spin system, create a website administrator user account; this is specific to a Django website and is unrelated to NERSC user accounts.

   #. Select "Workloads" from the "Resources" menu, and select the "Workloads" tab.
   
   #. Open the "three-dot" menu corresponding to the webserver workload.

   #. Select "Execute Shell."

   #. In the `/srv/website`, run

      #. `python manage.py makemigrations`
   
      #. `python manage.py migrate`      

      #. `python manage.py createsuperuser` and follow the prompts to create the account.

   #. One can then log into the Django admin site `https://<server_name>/admin/` using this superuser account and create regular user accounts using the web interface.
