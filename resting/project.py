import os
import sys
import subprocess

split_cwd = os.path.split(os.getcwd())
# We should be running this from the resting directory within the repository, although this is a problem for documentation generation
#assert split_cwd[1] == 'resting'
repository_top_directory = split_cwd[0]

app_name = 'test'

## Run on NERSC Spin

#server_name = ''
#platform = 'spin'
NERSC_project_id = ''

## Run on a standalone server

server_name = 'localhost'
platform = 'linux'

# These are the file locations in the host filesystem, as needed on a standalone server
# Under Cygwin on a Windows computer, these must be translated to be recognized by Docker, which is installed separately
# http://stackoverflow.com/questions/8220108/ddg#8220141
if sys.platform == 'cygwin':
    completed_process = subprocess.run(['cygpath','-w',repository_top_directory + '/secrets'],capture_output=True)
    secrets_directory = completed_process.stdout.decode()[:-1]
    completed_process = subprocess.run(['cygpath','-w',repository_top_directory + '/pgdata'],capture_output=True)    
    pgdata_directory = completed_process.stdout.decode()[:-1]
else:
    secrets_directory = repository_top_directory + '/secrets'
    pgdata_directory = repository_top_directory + '/pgdata'

# The webserver/ssl directory within the repository and its contents are automatically copied recursively onto /etc/ssl within the webserver Docker image, these are required on a standalone server
# Specify the file locations within the Docker image
ssl_certificate_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'
ssl_certificate_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'

## Homepage

# This is the Django template for the site homepage, assumed to be in the webserver/website/templates directory within the repository. If blank, the API root will be the site homepage.
index_template = ''
#index_template = 'index.html'

## API

# Blank or null will use the default URL scheme, with the API root as the default landing page
# This is ignored if a homepage template is not given above
api_prefix = 'api'

# Description format:
# { 
#     ModelName_str : {
#         ModelAttribute_str : {
#             "type" : Instanciation_str,
#             "filters" : [ FilterName_str, ... ]
#         }, ...
#     }, ...
# }

models = {
    'Independent':{
        # # This is the default field added by Django
        # 'id' : {
        #     'type': 'models.AutoField(primary_key=True)',
        #     'filters' : ['exact','in']
        #     },
        'charfield' : {
            'type' : 'models.CharField(max_length=32,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'intfield' : {
            'type' : 'models.IntegerField(null=True,blank=True)',
            'filters' : ['isnull','exact','gte','lte'],
            },
        'floatfield' : {
            'type' : 'models.FloatField(null=True,blank=True)',
            'filters' : ['exact','isnull','gte','lte'],
            },
        'urlfield' : {
            'type' : 'models.URLField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'textfield' : {
            'type' : 'models.TextField(max_length=8192,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        },
    'Dependent':{
        # # This is usually automatically added by Django
        # 'id' : {
        #     'type': 'models.AutoField(primary_key=True)',
        #     'filters' : ['exact','in']
        #     },
        'charfield' : {
            'type' : 'models.CharField(max_length=32,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'intfield' : {
            'type' : 'models.IntegerField(null=True,blank=True)',
            'filters' : ['isnull','exact','gte','lte'],
            },
        'floatfield' : {
            'type' : 'models.FloatField(null=True,blank=True)',
            'filters' : ['exact','isnull','gte','lte'],
            },
        'urlfield' : {
            'type' : 'models.URLField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'textfield' : {
            'type' : 'models.TextField(max_length=8192,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'onetoonefield' : {
            'type' : 'models.OneToOneField(Independent,related_name="onetoonefield",on_delete=models.CASCADE)',
            'filters' : [],
            },
        'foreignkeyfield' : {
            'type' : 'models.ForeignKey(Independent,related_name="onetomanyfield",on_delete=models.CASCADE)',
            'filters' : [],
            },
        'manytomanyfield' : {
            'type' : 'models.ManyToManyField(Independent,related_name="manytomanyfield")',
            'filters' : [],
            },
        },
    }
