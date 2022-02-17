#!/bin/sh

# It is assumed that the Spin setup has made the secrets and storage available (allocating directories as needed), as described in the documentation.

# The presence of the $PGDATA directory is understood to indicate that the database has already been created.

# If the database does not already exist, create it
if [ ! -d $PGDATA ]
then
    # Databases cannot be created as root, all data and process ownership will be under the user "postgres" (already exists in the image)
    # Ownership of $PGDATA by the user under which Postgres runs is required in order to initiate the database
    mkdir -p --mode=777 $PGDATA
    chown -R postgres $PGDATA
    # This creates a database named "postgres" (default) with a database superuser named "postgres" (default); this should also respect the information in environment variables, such as the password file
    runuser -c "initdb --pwfile=$POSTGRES_PASSWORD_FILE" postgres
    # Being more specific with the host address didn't seem to work
    #echo 'hostnossl postgres postgres all md5' >> $PGDATA/pg_hba.conf
    # This isn't secure in general, although is safe within the Spin system. Ideally would hash the password. Python's hashlib has an MD5 hash algorithm but the hexdigest output doesn't appear to be what Postgres wants. There is no description in the documentation, but https://stackoverflow.com/questions/45395538/postgres-md5-password-plain-password says that the format should be "md5" + <hash of password concatenated with username>
    echo 'hostnossl postgres postgres all password' >> $PGDATA/pg_hba.conf
fi

# As Cory Snavely has noted, Spin automatically restarts containers if there is no response to an automated health check request. 

# Move to the home directory of user "postgres" to ensure that the logfile can be created and start the server
runuser -c "cd ${PGDATA%/data} && pg_ctl -D $PGDATA -l logfile start" postgres

# Since this container is intended to be run with '-it' options and as Cory  noted, the conainer will exit once the entry point exits, this script will start a shell as its last action.

/bin/sh
