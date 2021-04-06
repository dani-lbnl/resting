FROM postgres:12

WORKDIR /

# This is used to change the home directory of user postgres to /var/lib/postgres, since the base image mounts a volume at /var/lib/postgresql/data, but we want to use the Spin system to keep persistent storage on a different volume
RUN cd /etc && mv passwd dist_passwd && sed 's/sql/s/' dist_passwd > passwd

# This script is run automatically and creates the database if it does not yet exist, and starts the database in any case
COPY custom_entry_point.sh custom_entry_point.sh

CMD ["/custom_entry_point.sh"]
