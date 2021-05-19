import re
import project
import os
import stat

repository_directory = '../'
database_directory = repository_directory + 'postgres/'
webserver_directory = repository_directory + 'webserver/'
website_directory = webserver_directory + 'website/'
app_directory = website_directory + f'{project.app_name}/'
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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

    return_value = ""
    
    for model_name in project.models.keys():
        # It seems that Django REST Framework might have a bug that assumes that lowercase view names are used
        model_name_lower = model_name.lower()
        return_value += f"router.register(r'{model_name_lower}', views.{model_name}ViewSet,basename='{model_name_lower}')\n"        

    return return_value
        
urls_template = f'''
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views
from {project.app_name} import views

## Create a router and register viewsets

router = DefaultRouter()

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

## Currently assuming that these images will only be used with Spin

postgres_build_template = f'''
#!/bin/sh
docker build -t registry.nersc.gov/{project.NERSC_project_id}/{project.app_name}_postgres:12 .
'''
generate(postgres_build_template,database_directory + 'build.sh')
os.chmod(database_directory + 'build.sh',stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

website_build_template = f'''
#!/bin/sh
docker build -t registry.nersc.gov/{project.NERSC_project_id}/{project.app_name}_webserver:3.7 .
'''
generate(website_build_template,webserver_directory + 'build.sh')
os.chmod(webserver_directory + 'build.sh',stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

# This must be written before the Dockerfile runs
website_sed_script_settings_template = f'''
/import os/a\
import hashlib

/^ALLOWED_HOSTS/c\
ALLOWED_HOSTS = ['.nersc.gov','.nersc.org','.lbl.gov']\
URL_FIELD_NAME = 'record_url'

/^INSTALLED_APPS/a\
    'rest_framework',\
    'rest_framework.authtoken',\
    'django_filters',\
    'django.contrib.postgres',\
    '{project.app_name}.apps.{project.app_name.capitalize()}Config',

# This does not seem to work properly, switching to the simpler PageNumberPagination style
#'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',\
# Perhaps there is some conflict with the dynamic filtering system
/^MIDDLEWARE/i\
REST_FRAMEWORK = {\
    'DEFAULT_AUTHENTICATION_CLASSES': [\
        'rest_framework.authentication.TokenAuthentication',\
        'rest_framework.authentication.SessionAuthentication'\
        ],\
    'DEFAULT_FILTER_BACKENDS': [\
                                'rest_framework_filters.backends.DjangoFilterBackend'],\
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',\
    'PAGE_SIZE':20\
    }\

/^        'DIRS':/c\
        'DIRS': ['/usr/lib/python3/dist-packages/rest_framework/templates/'],

/^DATABASES/i\
# Allow connections to persist (default is 0 seconds)\
CONN_MAX_AGE = 60\
with open(os.environ['POSTGRES_PASSWORD_FILE'],'r') as password_file:\
    postgres_password = password_file.readline()\
postgres_password_hasher = hashlib.md5()\
postgres_password_hasher.update(postgres_password.encode())\
hashed_postgres_password = postgres_password_hasher.hexdigest()\

/^        'ENGINE'/c\
        'ENGINE': 'django.db.backends.postgresql',

/^        'NAME': os/c\
        'NAME': 'postgres',\
        'USER': 'postgres',\
        'PASSWORD': postgres_password,\
        'HOST': 'db',\
        'PORT': '5432'   
'''
generate(website_sed_script_settings_template,site_directory + 'sed_script_settings.py')

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
RUN umask 007 && chmod -R g+w /var/run/apache2 && chgrp -R root /var/log/apache2 && chmod -R g+w /var/log/apache2 && cd /etc/apache2 && cat append_to_apache2.conf >> apache2.conf && mv ports.conf dist_ports.conf && sed 's/Listen 80/Listen 8000/' dist_ports.conf > ports.conf && cd sites-available && mv 000-default.conf dist_000-default.conf && sed 's/VirtualHost \*:80/VirtualHost \*:8000/' dist_000-default.conf > 000-default.conf && chmod g+rwx /srv && cd /srv && mkdir static && chmod o+x static && chmod g+rwx static && django-admin startproject website && chmod g+rwx website && cd website && \
python manage.py startapp {project.app_name}

# Now that the website skeleton exists, copy in files for customization
COPY website srv/website/

# Use sed scripts to modify stock files
RUN cp /srv/website/templates/* /usr/lib/python3/dist-packages/rest_framework/templates/rest_framework/ && cd /srv/website/website && mv settings.py dist_settings.py && sed -f sed_script_settings.py dist_settings.py > settings.py

# Run the web server in the foreground so that the container does not immediately exit
CMD ["/usr/sbin/apache2ctl","-DFOREGROUND","-kstart"]
'''
generate(website_dockerfile_template,webserver_directory + 'Dockerfile')

## client.py

# def client_functions():

#     return_value = ""
           
#     # Loop over all models
#     for model, attributes in project.models.items():
        
#         # Create one blank form generator function for each model
#         return_value += '\ndef get' + model + 'FilterForm():\n'
#         return_value += indent + 'return_value = {\n'
#         for attribute,parameters in attributes.items():
#             return_value += indent + indent + "'" + attribute + "' : {\n"
            
#             for drffilter in parameters['filters']:

#                 return_value += indent + indent + indent + "'" + drffilter + "' : None,\n"
                
#             return_value += indent + indent + indent + '},\n'
                
#         return_value += indent + indent + '}\n'
#         return_value += indent + 'return return_value\n'        

#         # Create one form-based data retrieval function for each model
#         return_value += '\ndef retrieve' + model + '(filterForm):\n'

#         ## Check form for validity

#         # Store sequence of all permitted attributes
#         return_value += indent + 'model_attributes =' + attribute + '\n'

#         return_value += indent + 'return "' + model + '/" + generate_url_filter(model_attributes,filterForm)\n'
#         #return_value += indent + 'url = "' + model + '/" + generate_url_filter(model_attributes,filterForm)\n'        
        
#         # # Loop over all attributes in the form
#         # return_value += indent + 'for attribute in filterForm:\n'
        
#         # # Check that the present attribute is present in the model description
#         # return_value += indent + indent + 'assert attribute in model_attributes, "Error: " + attribute + " is not an ' + model + ' attribute."\n'

#         # # Loop over all filters associated with the present attribute in the form
#         # return_value += indent + indent + 'for drffilter in filterForm[attribute]:\n'

#         # # Check that the present filter is present in the model description
#         # return_value += indent + indent + indent + 'assert drffilter in model_attributes[attribute]["filters"], "Error: " + drffilter + " is not a valid filter for ' + model + ' attribute " + attribute + "."\n'

#         # # Add to the URL
#         # return_value += indent + indent + indent + 'if filterForm[attribute][drffilter] != None:\n'

#         # return_value += indent + indent + indent + indent + 'if type(filterForm[attribute][drffilter]) == int or type(filterForm[attribute][drffilter]) == float:\n'        
#         # return_value += indent + indent + indent + indent + indent + 'url += attribute + "__" + drffilter + "=" + str(filterForm[attribute][drffilter]) + "&"\n'
#         # return_value += indent + indent + indent + indent + 'elif type(filterForm[attribute][drffilter]) == str:\n'        
#         # return_value += indent + indent + indent + indent + indent + 'url += attribute + "__" + drffilter + "=" + filterForm[attribute][drffilter] + "&"\n'
#         # return_value += indent + indent + indent + indent + 'elif type(filterForm[attribute][drffilter]) == tuple or type(filterForm[attribute][drffilter]) == list:\n'
#         # return_value += indent + indent + indent + indent + indent + 'url += attribute + "__" + drffilter + "="\n'
#         # return_value += indent + indent + indent + indent + indent + 'start = True\n'        
#         # return_value += indent + indent + indent + indent + indent + 'for value in filterForm[attribute][drffilter]:\n'
#         # return_value += indent + indent + indent + indent + indent + indent + 'if start:\n'
#         # return_value += indent + indent + indent + indent + indent + indent + indent + 'url += str(value)\n'
#         # return_value += indent + indent + indent + indent + indent + indent + indent + 'start = False\n'        
#         # return_value += indent + indent + indent + indent + indent + indent + 'else:\n'        
#         # return_value += indent + indent + indent + indent + indent + indent + indent + 'url += "%2C" + str(value)\n'

#         # return_value += indent + 'return url\n'                

#     return return_value

# client_template = f'''
# import rest_client
# {client_functions()}
# '''

# generate(client_template,'client.py')