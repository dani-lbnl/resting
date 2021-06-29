# Assume that we're starting in the resting directory, should check for this
APP_NAME=`$PYTHON -c "import project;print(project.app_name)"`
cd ..
TOP=`pwd`
# Generate the site documentation
cd $TOP/webserver/doc
make html
cd $TOP/webserver/website/$APP_NAME
mkdir static
cd static
mkdir $APP_NAME
cd $APP_NAME
mkdir doc
cd $TOP/webserver/doc/_build/html
cp -R * $TOP/webserver/website/$APP_NAME/static/$APP_NAME/doc
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
