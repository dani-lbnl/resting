# For testing
cd ..
TOP=`pwd`
cd $TOP/webserver
cd doc
make html
cd $TOP/webserver/website/static/website
mkdir doc
cp -R $TOP/webserver/doc/_build/html/* doc
cd $TOP
# If not yet authenticated, run:
# docker login registry.nersc.gov
cd postgres
sudo ./build.sh
docker push registry.nersc.gov/m3670/acts_postgres:12
cd ../webserver
sudo ./build.sh
docker push registry.nersc.gov/m3670/acts_webserver:3.7
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

