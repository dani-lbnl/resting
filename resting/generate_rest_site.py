import re
import project
import os
import stat

# Assuming that this is run from the resting subdirectory in the repository
repository_directory = '../'
script_directory = repository_directory + 'resting/'
database_directory = repository_directory + 'postgres/'
webserver_directory = repository_directory + 'webserver/'
apache_directory = webserver_directory + 'apache/'
website_documentation_directory = webserver_directory + 'doc/'
website_directory = webserver_directory + 'website/'
app_directory = website_directory + f'{project.app_name}/'
if not os.access(app_directory,os.F_OK):
    os.mkdir(app_directory)
site_directory = website_directory + 'website/'
template_directory = website_directory + 'templates/'

### Will might want to use a class-based approach that can retrieve and hold information until a new query dict is provided

def validate_descriptions(model_descriptions):
    ''' Check the user-provided model description, throwing an Exception if an error is encountered. If the description passes this check, a form that adheres to this description will only be invalid if it contains bad filter value specifications.
    '''
    for model, description in model_descriptions.items():

        assert type(model) == str, str(model) + ' is not a Python str'

        for attribute, parameters in description.items():

            assert type(attribute) == str, str(attribute) + ' is not a Python str'

            # for parameter in ['type','filters']:
            
            #     assert parameter in descriptions[attribute], parameter + ' was not provided for ' + attribute

            assert type(description[attribute]['type']) == str, str(description[attribute]['type']) + ' is not a Python str'

            assert re.fullmatch('models\.\w+\(.*\)\s*',description[attribute]['type']) != None, description[attribute]['type'] + ' does not have the regular expression "model\.\w+\(.*\)\s*"'

            field_type = re.match('models\.\w+',description[attribute]['type']).group()
            
            assert type(description[attribute]['filters']) == tuple or type(description[attribute]['filters']) == list, str(description[attribute]['filters']) + ' is not a Python tuple or list'

            ## Check for reasonable filter choices
            
            if field_type in [ 'models.CharField','models.TextField','models.URLField','models.EmailField','models.FileField','models.FilePathField','models.RegexField','models.SlugField','models.UUIDField','models.GenericIPAddressField','models.ImageField' ]:
           
                for fltr in description[attribute]['filters']:
                    assert fltr in [ 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search', 'exact', 'contains', 'endswith','regex']

            elif field_type in [ 'models.FloatField', 'models.DecimalField' ]:
                
                for fltr in description[attribute]['filters']:
                    assert fltr in [ 'exact', 'isnull', 'gte', 'lte', 'gt', 'lt' ]

            elif field_type in [ 'models.IntegerField', 'models.SmallIntegerField', 'models.PositiveSmallIntegerField' ]:

                for fltr in description[attribute]['filters']:
                    assert fltr in [ 'isnull', 'in', 'exact', 'gte', 'lte', 'gt', 'lt' ]
# __range
            elif field_type == 'models.ForeignKey' or field_type == 'models.OneToOneField' or field_type == 'models.ManyToManyField':
                # No filtering available here, for now
                assert description[attribute]['filters'] == []

            else:
                message = field_type + ' is not recognized'
                raise AssertionError(message)
                
# self-documentation
# Also might need some way to describe the additional capabilities of the gallery, which are somewhat outside of the REST framework.

# This will throw an Exception if it finds something wrong in the user-defined model descriptions
validate_descriptions(project.models)

indent = '    '
        
# class Generator():

#     def __init__(self,file_template,target_directory,filename):

#         #self.model_descriptions = model_descriptions
#         self.file_template = file_template
#         self.filename = filename

#         if target_directory[-1] == '/':
        
#             self.full_path = target_directory + filename

#         else:

#             self.full_path = target_directory + '/' + filename
        
#         self.indent = '    '

#     def run(self):

#         with open(self.full_path,'w') as generated_file:
#             print(self.file_template,file=generated_file)
        
# class ModelsGenerator(Generator):

#     def __init__(self,model_descriptions,target_directory):

#         file_template = f'''
# from django.db import models
# from django.contrib.auth.models import User
# {self.model_classes(model_descriptions)}
# '''
        
#         Generator.__init__(self,file_template,target_directory,'models.py')

#     def model_classes(self,model_descriptions):

#         return_value = ""

#         for model,description in model_descriptions.items():
#             return_value += '\nclass ' + model + '(models.Model):\n'
#             for attribute,characteristics in description.items():
#                 if attribute != 'id':
#                     # Skip the default automatic primary key
#                     return_value += self.indent + attribute + ' = ' + characteristics['type'] + '\n'

#         return return_value

# modelsGenerator = ModelsGenerator(model_descriptions,'.')
# modelsGenerator.run()

def generate(template,full_path):
    with open(full_path,'w') as output_file:
        print(template,file=output_file)

## api.html

api_html_template = '''{% extends "rest_framework/base.html" %}
{% block branding %}
''' + f'''<a class='navbar-brand' rel='nofollow' href='https://{project.server_name}'>{project.server_name}</a>''' + '''
{% endblock %}
'''

generate(api_html_template,template_directory + 'api.html')
        
## models.py

def model_classes():

    return_value = ""
    
    for model,description in project.models.items():
        return_value += f'\nclass {model}(models.Model):\n'        
        for attribute,characteristics in description.items():
            if attribute != 'id':
                # Skip the default automatic primary key
                return_value += indent + attribute + ' = ' + characteristics['type'] + '\n'

    return return_value

# Substitutions are performed immediately
models_template = f'''
from django.db import models
from django.contrib.auth.models import User
{model_classes()}
'''

generate(models_template,app_directory + 'models.py')

## views.py

# def view_model_fields(description):

#     return_value = ""
    
#     for field,parameters in description.items():
#         if parameters['filters'] != []:
#             # Skip fields with no filters
#             #return_value += indent + indent + indent + "'" + field + "' : " + str(parameters['filters']) + ',\n'
#             return_value += '\n' + indent + indent + indent + f"'{field}': {str(parameters['filters'])},"    

#     return return_value
            
def view_classes():

    return_value = ""        
    
    for model,description in project.models.items():

        filter_template = f'''
class {model}Filter(rest_framework_filters.FilterSet):
    class Meta:
        model = {model}
'''

        return_value += filter_template

        # It appears that newlines are sometimes quoted when strings are
        # substituted into f-strings, so build strings by concatenation here

        return_value += indent + indent + 'fields = {\n'

        for field,parameters in description.items():
            if parameters['filters'] != []:
                # Skip fields with no filters
                return_value += indent + indent + indent + f"'{field}': {str(parameters['filters'])},\n"
        
        return_value += indent + indent + indent + '}\n'
        
        viewset_template = f'''
class {model}ViewSet(viewsets.ModelViewSet):
    filter_class = {model}Filter
    serializer_class = {model}Serializer
    queryset = {model}.objects.all()
    # https://www.django-rest-framework.org/api-guide/permissions/
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
'''

        return_value += viewset_template

    return return_value
        
views_template = f'''
from rest_framework import viewsets, permissions
import rest_framework_filters
from {project.app_name}.models import *
from {project.app_name}.serializers import *
{view_classes()}
'''

generate(views_template,app_directory + 'views.py')

## serializers.py

related_fields = {}

for model in project.models:
    related_fields[model] = {}

# I'll use the match method, so we'll start matching from the start of each string
related_name_given_re = re.compile('.*\((.*?)\s*,\s*related_name\s*=\s*(.*?)\s*(?:,|\)).*$')
no_related_name_given_re = re.compile('.*\((.*?)\s*,|\).*$')
    
for model,attributes in project.models.items():

    for attribute,information in attributes.items():

        if 'ForeignKey' in information['type']:
            match = related_name_given_re.match(information['type'])
            if match:
                related_fields[match[1]][match[2].strip('\'"')] = {'type':model,'many':True}
            else:
                match = no_related_name_given_re.match(information['type'])
                assert match != None, 'ERROR: ForeignKey declaration does not name related Model'
                related_fields[match[1]][model+'_set'] = {'type':model,'many':True}
                                                       
        elif 'OneToOneField' in information['type']:
            match = related_name_given_re.match(information['type'])
            if match:
                related_fields[match[1]][match[2].strip('\'"')] = {'type':model,'many':False}
            else:
                match = no_related_name_given_re.match(information['type'])
                assert match != None, 'ERROR: OneToOneField declaration does not name related Model'
                related_fields[match[1]][match[1].lower()] = {'type': model,'many':False}

        elif 'ManyToManyField' in information['type']:
            match = related_name_given_re.match(information['type'])
            if match:
                related_fields[match[1]][match[2].strip('\'"')] = {'type':model,'many':True}
            else:
                match = no_related_name_given_re.match(information['type'])
                assert match != None, 'ERROR: ManyToManyField declaration does not name related Model'
                related_fields[match[1]][model+'_set'] = {'type':model,'many':True}
            
def serializer_classes():

    return_value = ''

    for model in project.models:
        # The 'id' automatic primary field is always included because dependent records will submit queries through the web interface to find related objects and will need this information to save references to other objects. Apparently, there is a built-in restriction in Django REST Framework that prevents the record input forms from allowing modification of the 'id' field.
        #### It might be a mistake to use the HyperlinkModelSerializer rather than just the ModelSerializer because we have 'url' fields in the data, which are supposed to also be used internally.
        #### In order to follow model relationships in the reverse direction, we will probably have to add the fields explicitly here. This means searching project.py for relevant models.
        serializer_template_head = f'''
from {project.app_name}.models import {model}

class {model}Serializer(serializers.HyperlinkedModelSerializer):
'''
        
        serializer_template_tail = f'''
    class Meta:
        model = {model}
        fields = {['id'] + list(project.models[model].keys()) + list(related_fields[model].keys())}
'''
        
        return_value += serializer_template_head

        for related_field,information in related_fields[model].items():

            serializer_template_related = f'''
    {related_field} = serializers.HyperlinkedRelatedField(many={information['many']},view_name='{information['type'].lower()}-detail',read_only=True)
'''
            return_value += serializer_template_related
            
        return_value += serializer_template_tail

    return return_value

serializers_template = f'''
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
{serializer_classes()}
'''

generate(serializers_template,app_directory + 'serializers.py')

def router_registrations():

    if project.api_prefix == '':
        # API root page will be the landing page
        return_value = '''
router = DefaultRouter()

'''
        for model_name in project.models.keys():
            # It seems that Django REST Framework might have a bug that assumes that lowercase view names are used
            model_name_lower = model_name.lower()
            return_value += f"router.register(r'{model_name_lower}', views.{model_name}ViewSet,basename='{model_name_lower}')\n"        
        
    else:
        # probably better to check if defined
        if project.index_template != '':
            # A template filename has been provided
        
            # This follows the pattern in rest_framework/routers.py
            # also set the default view
            return_value = '''
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView

class CustomRouter(DefaultRouter):
    def get_urls(self):
        urls = super(DefaultRouter,self).get_urls()
        urls = format_suffix_patterns(urls)
        urls.append(url(r'^''' + project.api_prefix + '''/?$',self.get_api_root_view(api_urls=urls),name='api-root'))
        urls.append(url(r'^$',TemplateView.as_view(template_name="''' + project.index_template + '''")))
        return urls

router = CustomRouter()
'''
        else:
            # Redirect to where the static home page should be located
            return_value = '''
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

def home_page_view(request):
    return HttpResponseRedirect('/static/''' + project.app_name + '''/home/index.html')

class CustomRouter(DefaultRouter):
    def get_urls(self):
        urls = super(DefaultRouter,self).get_urls()
        urls = format_suffix_patterns(urls)
        urls.append(url(r'^''' + project.api_prefix + '''/?$',self.get_api_root_view(api_urls=urls),name='api-root'))
        urls.append(url(r'^$',home_page_view))
        return urls

router = CustomRouter()
'''
        
        for model_name in project.models.keys():
            # It seems that Django REST Framework might have a bug that assumes that lowercase view names are used
            model_name_lower = model_name.lower()
            return_value += f"router.register(r'{project.api_prefix}/{model_name_lower}', views.{model_name}ViewSet,basename='{model_name_lower}')\n"        

    return return_value
        
urls_template = f'''
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views
from {project.app_name} import views

## Create a router and register viewsets

{router_registrations()}
urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^api-token-auth/', authtoken_views.obtain_auth_token),
    url(r'api-auth/', include('rest_framework.urls')),
    url('^', include('django.contrib.auth.urls')),
    url('^admin/', admin.site.urls)
]
'''

generate(urls_template,site_directory + 'urls.py')

if project.platform == 'spin':
    
    apache2_template = ''

else:
    # Set up SSL
    # See file:///usr/share/doc/apache2-doc/manual/en/ssl/ssl_howto.html
    # Force redirection from http to https
    # file:///usr/share/doc/apache2-doc/manual/en/rewrite/avoid.html
    apache2_template = 'LoadModule ssl_module modules/mod_ssl.so'

    site_template = f'''
/<VirtualHost/a\
Redirect "/" "https://{project.server_name}/"'''

    generate(site_template,apache_directory + '000-default.conf.sed')
    
    ssl_template = f'''
/^\t*SSLCertificateFile/c\
		SSLCertificateFile	{project.ssl_certificate_file}

/^\t*SSLCertificateKeyFile/c\
		SSLCertificateKeyFile {project.ssl_certificate_key_file}
'''
    generate(ssl_template,apache_directory + 'default-ssl.conf.sed')
    
apache2_template += '''
Alias /static/ /srv/static/

<Directory /srv/static/>
Require all granted
</Directory>

WSGIScriptAlias / /srv/website/website/wsgi.py

WSGIPythonPath /srv/website

<Directory /srv/website/website/>
<Files wsgi.py>
Require all granted
</Files>
</Directory>

WSGIPassAuthorization On
'''

generate(apache2_template,apache_directory + 'append_to_apache2.conf')

if project.platform == 'spin':

    website_dockerfile_template = f'''
# There are version problems with mod_wsgi and psycopg2 in the latest (3.8) image, so stay with 3.7
FROM python:3.7

RUN apt-get update && apt-get -y install python3-djangorestframework apache2 libapache2-mod-wsgi-py3 python3-djangorestframework-filters

ENV PYTHONPATH /usr/lib/python3/dist-packages

EXPOSE 8000

WORKDIR /

# Copy in file(s) used to modify stock Apache file(s)
COPY apache etc/apache2/

# In order to access the CFS, this container will run as a NERSC user. This user will not have root privileges in this container, but will be in the root group. Some directory and file permissions must be changed in order for this user to run Apache properly.
# Apache configuration is done here through modification of the stock configuration files.
# Django is then directed to create the skeleton website
# This was the source of a helpful tip for standalone hosting: https://serverfault.com/questions/1046774/ah00035-access-to-denied-403-forbidden-django-mod-wsgi
RUN umask 007 && chmod -R g+w /var/run/apache2 && chgrp -R root /var/log/apache2 && chmod -R g+w /var/log/apache2 && cd /etc/apache2 && cat append_to_apache2.conf >> apache2.conf && mv ports.conf dist_ports.conf && sed 's/Listen 80/Listen 8000/' dist_ports.conf > ports.conf && cd sites-available && mv 000-default.conf dist_000-default.conf && sed 's/VirtualHost \*:80/VirtualHost \*:8000/' dist_000-default.conf > 000-default.conf && chmod g+rwx /srv && cd /srv && mkdir static && chmod o+x static && chmod g+rwx static && django-admin startproject website && chmod g+rwx website && chmod a+rx website && cd website && python manage.py startapp {project.app_name}

# Now that the website skeleton exists, copy in files for customization
COPY website srv/website/

# Modify stock files and copy static files
RUN cp /srv/website/templates/* /usr/lib/python3/dist-packages/rest_framework/templates/rest_framework/ && cd /srv/website/website && mv settings.py dist_settings.py && sed -f sed_script_settings.py dist_settings.py > settings.py && echo "INSTALLED_APPS.append('{project.app_name}.apps.{project.app_name.capitalize()}Config')" >> settings.py && cd /srv/website && python manage.py collectstatic

# Run the web server in the foreground so that the container does not immediately exit
CMD ["/usr/sbin/apache2ctl","-DFOREGROUND","-kstart"]
'''
else:
    # I frequently run into a problem with psycopg2; import psycopg2 attempts to import from psycopg2._psycopg, a module that does not exist, but is supposed to be part of the same package. This was why I switched from python:3.8 to python:3.7 when working on a Linux system, but it seems that this does not work on a Windows or Mac system, which might require yet another version.
    website_dockerfile_template = f'''
# There are version problems with mod_wsgi and psycopg2 in the latest (3.8) image, so stay with 3.7
FROM python:3.7

RUN apt-get update && apt-get -y install python3-djangorestframework apache2 libapache2-mod-wsgi-py3 python3-djangorestframework-filters

ENV PYTHONPATH /usr/lib/python3/dist-packages

EXPOSE 80
EXPOSE 443

WORKDIR /

# Copy in file(s) used to configure the web server
COPY apache etc/apache2/
COPY ssl etc/ssl/

# In order to access the CFS, this container will run as a NERSC user. This user will not have root privileges in this container, but will be in the root group. Some directory and file permissions must be changed in order for this user to run Apache properly.
# Apache configuration is done here through modification of the stock configuration files.
# Django is then directed to create the skeleton website
# This was the source of a helpful tip for standalone hosting: https://serverfault.com/questions/1046774/ah00035-access-to-denied-403-forbidden-django-mod-wsgi
RUN umask 007 && chmod -R g+w /var/run/apache2 && chgrp -R root /var/log/apache2 && chmod -R g+w /var/log/apache2 && cd /etc/apache2 && cat append_to_apache2.conf >> apache2.conf && cd sites-available && mv default-ssl.conf default-ssl.conf.original && mv 000-default.conf 000-default.conf.original && sed -f ../default-ssl.conf.sed default-ssl.conf.original > default-ssl.conf && sed -f ../000-default.conf.sed 000-default.conf.original > 000-default.conf && cd ../sites-enabled && ln -s /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-enabled/default-ssl.conf && ln -s /etc/apache2/mods-available/ssl.conf /etc/apache2/mods-enabled && ln -s /etc/apache2/mods-available/socache_shmcb.load /etc/apache2/mods-enabled && ln -s /etc/apache2/mods-available/ssl.load /etc/apache2/mods-enabled && chmod g+rwx /srv && cd /srv && mkdir static && chmod o+x static && chmod g+rwx static && django-admin startproject website && chmod g+rwx website && chmod a+rx website && cd website && python manage.py startapp {project.app_name}

# Now that the website skeleton exists, copy in files for customization
COPY website srv/website/

# Modify stock files and copy static files
RUN cp /srv/website/templates/* /usr/lib/python3/dist-packages/rest_framework/templates/rest_framework/ && cd /srv/website/website && mv settings.py dist_settings.py && sed -f sed_script_settings.py dist_settings.py > settings.py && echo "INSTALLED_APPS.append('{project.app_name}.apps.{project.app_name.capitalize()}Config')" >> settings.py && cd /srv/website && python manage.py collectstatic

# Run the web server in the foreground so that the container does not immediately exit
CMD ["/usr/sbin/apache2ctl","-DFOREGROUND","-kstart"]
'''
    
generate(website_dockerfile_template,webserver_directory + 'Dockerfile')

if project.platform == 'spin':
    tag_prefix = f'registry.nersc.gov/{project.NERSC_project_id}/'
    
    finish_template = f'''
#!/bin/bash
# Check for Python executable name
if python3 -V
then
    PYTHON=python3
elif python -V
then
    PYTHON=python
else
    echo Could not find Python executable, edit start.sh and set the PYTHON variable to the executable location.
    exit
fi
# Assume that we're starting in the resting directory, should check for this
APP_NAME={project.app_name}
cd ..
TOP=`pwd`
if [[ ${{MACHTYPE%cygwin}}=$MACHTYPE ]]
then
    SUDOPREFIX='sudo '
else
    SUDOPREFIX=''
fi
# Generate the site documentation
cd $TOP/webserver/doc
make SPHINXBUILD="$PYTHON -m sphinx.cmd.build" html
# Copy the site documentation to the doc subdirectory of the app static directory
# Might be able to just link instead
cd $TOP/webserver/doc/_build/html
cp -R * $TOP/webserver/website/$APP_NAME/static/$APP_NAME/doc
cd $TOP
# If already authenticated, this doesn't do any harm:
docker login registry.nersc.gov
cd postgres
${{SUDOPREFIX}}./build.sh
docker push {tag_prefix}{project.app_name}_postgres:12
cd ../webserver
${{SUDOPREFIX}}./build.sh
docker push {tag_prefix}{project.app_name}_webserver:3.7
'''
    
else:
    tag_prefix = ''
    
    finish_template = f'''
#!/bin/bash
# Check for Python executable name
if python3 -V
then
    PYTHON=python3
elif python -V
then
    PYTHON=python
else
    echo Could not find Python executable, edit start.sh and set the PYTHON variable to the executable location.
    exit
fi
# Assume that we're starting in the resting directory, should check for this
APP_NAME={project.app_name}
cd ..
TOP=`pwd`
if [[ ${{MACHTYPE%cygwin}}=$MACHTYPE ]]
then
    SUDOPREFIX='sudo '
else
    SUDOPREFIX=''
fi
# Seems to be necessary to allow the postgres user in the Postgres container to run initdb
chmod a+w {project.pgdata_directory}
# Generate the site documentation
cd $TOP/webserver/doc
make SPHINXBUILD="$PYTHON -m sphinx.cmd.build" html
# Copy the site documentation to the doc subdirectory of the app static directory
# Might be able to just link instead
cd $TOP/webserver/doc/_build/html
cp -R * $TOP/webserver/website/$APP_NAME/static/$APP_NAME/doc
cd $TOP
# Assume that there's no need to push to a repository
cd postgres
${{SUDOPREFIX}}./build.sh
cd ../webserver
${{SUDOPREFIX}}./build.sh
'''
    # https://docs.docker.com/network/bridge/
    run_template = f'''
#!/bin/bash
if [[ ${{MACHTYPE%cygwin}}=$MACHTYPE ]]
then
    SUDOPREFIX='sudo '
else
    SUDOPREFIX=''
fi
# Check that a secrets subdirectory exists
if [[ ! -d {project.secrets_directory} ]]
then
    echo Secrets directory {project.secrets_directory} does not exist.
    exit
fi
if [[ ! -r {project.secrets_directory}/password ]]
then
    echo 'password' file does not exist in secrets directory.
fi
# Create user-defined bridge network if one doesn't already exist
if [[ `docker network ls -f name={project.app_name}_network | wc -l` -eq 1 ]]
then
    ${{SUDOPREFIX}}docker network create {project.app_name}_network
fi
# The custom entry point script expects this image to be run with the -it flags
./run_db.sh
./run_ws.sh
# Execute shell, allowing user to perform final configuration
${{SUDOPREFIX}}docker exec -it ws /bin/bash /initialize.sh
'''

    generate(run_template,script_directory + 'run.sh')
    os.chmod(script_directory + 'run.sh',stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

    run_db_template = f'''
docker run -itd --network={project.app_name}_network -h db --mount type=bind,src={project.secrets_directory},dst=/secrets --mount type=bind,src={project.pgdata_directory},dst=/var/lib/postgres -e POSTGRES_PASSWORD_FILE=/secrets/password -e PGDATA=/var/lib/postgres/data --name db {project.app_name}_postgres:12
'''
    generate(run_db_template,script_directory + 'run_db.sh')
    os.chmod(script_directory + 'run_db.sh',stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

    run_ws_template = f'''
sudo docker run -d --network={project.app_name}_network -h ws --mount type=bind,src={project.secrets_directory},dst=/secrets -e POSTGRES_PASSWORD_FILE=/secrets/password -p 80:80/tcp -p 443:443/tcp --name ws {project.app_name}_webserver:3.7
'''
    generate(run_ws_template,script_directory + 'run_ws.sh')
    os.chmod(script_directory + 'run_ws.sh',stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

postgres_build_template = f'''
#!/bin/bash
docker build -t {tag_prefix}{project.app_name}_postgres:12 .
'''

website_build_template = f'''
#!/bin/bash
docker build -t {tag_prefix}{project.app_name}_webserver:3.7 .
'''
        
generate(postgres_build_template,database_directory + 'build.sh')
os.chmod(database_directory + 'build.sh',stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

generate(website_build_template,webserver_directory + 'build.sh')
os.chmod(webserver_directory + 'build.sh',stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

generate(finish_template,script_directory + 'finish.sh')
os.chmod(script_directory + 'finish.sh',stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

## doc.html

# def models():

#     return_value = ""        
    
#     for model,description in project.models.items():

#         filter_template = f'''
# class {model}Filter(rest_framework_filters.FilterSet):
#     class Meta:
#         model = {model}
# '''

#         return_value += filter_template

#         # It appears that newlines are sometimes quoted when strings are
#         # substituted into f-strings, so build strings by concatenation here

#         return_value += indent + indent + 'fields = {\n'

#         for field,parameters in description.items():
#             if parameters['filters'] != []:
#                 # Skip fields with no filters
#                 return_value += indent + indent + indent + f"'{field}': {str(parameters['filters'])},\n"
        
#         return_value += indent + indent + indent + '}\n'
        
#         viewset_template = f'''

index_rst_template = f'''
=====================
Website documentation
=====================

`Click here <https://{project.server_name}/>`_ to return to the website home page.

.. toctree::
   api
   python
'''
#  notebook
generate(index_rst_template,website_documentation_directory + 'index.rst')

filter_description = { 'exact':'case-sensitive match to specified value',
                       'iexact':'case-insensitive match to specified value',
                       'in':'case-sensitive match to specified values',
                       'istartswith':'case-insensitive match of beginning of string to specified value',
                       'icontains':'case-insensitive match of part of string to specified value',
                       'iendswith':'case-insensitive match of end of string to specified value',
                       'iregex':'case-insensitive match to specified regular expression ("." matches any character, "*" matches zero or more of the previous character, "[\ *characters*\ ]" matches any one of the characters, etc.)',
                       'search':'case-insensitive match of part of string to specified value',                       
                       'startswith':'case-sensitive match of beginning of string to specified value',
                       'contains':'case-sensitive match of part of string to specified value',
                       'endswith':'case-sensitive match of end of string to specified value',
                       'regex':'case-sensitive match to specified regular expression (. matches any character, * matches zero or more of the previous character)',
                       'isnull':'*true* (no value) or *false* (has value)',
                       'gte':'greater than or equal to specified value',
                       'lte':'less than or equal to specified value',
                       'gt':'greater than specified value',
                       'lt':'less than specified value'}

def fields_and_filters():
    output = ''
    for model in project.models:
        output += '* **' + model + '** model\n\n'
        for field in project.models[model]:
            output += '  * **' + field + '** field\n\n'
            for field_filter in project.models[model][field]['filters']:
                output += '    * **' + field_filter + '**\ : ' + filter_description[field_filter] + '\n'
            output += '\n'
        output += '\n'
    return output

api_rst_template = f'''
===
API
===

Examples
========

https://{project.server_name}/api/\ **model**\ /

To apply a **filter** described by a single **value** to a **field** and access the first page of matching **Model** records in HTML format, use:

https://{project.server_name}/api/\ **model**\ /?\ **field**\ __\ **filter**\ =\ **value**

To apply a **filter** described by **value1** and **value2** to a **field** and access the first page of matching **Model** records in HTML format, use:

https://{project.server_name}/api/\ **model**\ /?\ **field**\ __\ **filter**\ =\ **value1**\ %2C\ **value2**

or

https://{project.server_name}/api/\ **model**\ /?\ **field**\ __\ **filter**\ =\ **value1**\ ,\ **value2**

and likewise for additional values.

To apply a **filter** described by a single **value** to a **field** and access page **N** of matching **Model** records in HTML format, use:

https://{project.server_name}/api/\ **model**\ /?page=\ **N**\ &\ **field**\ __\ **filter**\ =\ **value**

To apply both **filter1** described by a single **value1** and **filter2** described by a single **value2** to a **field** and access the first page of matching **Model** records in HTML format, use:

https://{project.server_name}/api/\ **model**\ /?\ **field**\ __\ **filter1**\ =\ **value1**\ &\ **field**\ __\ **filter2**\ =\ **value2**

and likewise for additional fields and filters.

To apply a **filter** described by a single **value** to a **field** and access the first page of matching **Model** records in JSON format, use:

https://{project.server_name}/api/\ **model**\ /?\ **field**\ __\ **filter**\ =\ **value**\ &format=json

Available models, fields, and filters
=====================================

{fields_and_filters()}
'''

generate(api_rst_template,website_documentation_directory + 'api.rst')

python_rst_template = f'''
=========================
Python REST client module
=========================

Usage
=====

`Download the Python REST client module <https://{project.server_name}/static/{project.app_name}/downloads/rest_client.py>`_

Run the Python 3 interpreter or script from the directory containing the module, or use ``import sys`` and add the directory to the ``sys.path`` list.

Module reference
================

.. automodule:: rest_client
   :members: RecordConnection, DatabaseConnection 
'''

generate(python_rst_template,website_documentation_directory + 'python.rst')
