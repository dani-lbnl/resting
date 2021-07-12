print(autodoc_mock_imports)
import urllib.request
#import urllib.parse
import json
import ssl

import project
import csv

import re

class DataPlugin:

    def __init__(self):
        raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
    
class CSVDataPlugin(DataPlugin):

    def __init__(self,model_name,filename,delimiter=',',quotechar='"',**fmtparams):
        self.csv_file = open(filename,'r')
        self.csv_reader = csv.reader(self.csv_file,delimiter=delimiter,quotechar=quotechar,**fmtparams)

        self.header = self.csv_reader.__next__()

        self.column_count = len(self.header)

        self.attributes = {}

        model_description = project.models[model_name]
        for attribute,info in model_description.items():
            try:
                csv_column = self.header.index(attribute)
            except:
                continue
            else: 
                attribute_type = info['type']
                # Associate recognized attributes with CSV column numbers and types
                # This will ignore all CSV columns that aren't labeled with a recognized attribute name
                if 'Int' in attribute_type:
                    self.attributes[attribute] = (csv_column,int)
                elif 'Float' in attribute_type: 
                    self.attributes[attribute] = (csv_column,float)
                else: #if 'Char' in attribute_type or 'Text' in attribute_type or 'URL' in attribute_type:
                    # No conversion
                    # This also catches ForeignKey, ManyToManyField, OneToOneField
                    self.attributes[attribute] = (csv_column,str)
                    
    # It might not be necessary to do conversions since all data. However, this at least ensures that some error checking is done on the data.

    def __next__(self):
        row = self.csv_reader.__next__()
        # The CSV reader does not recognize that comma-separated sequences in square brackets are not separate columns
        if len(row) != self.column_count:
            #### Should allow incomplete rows when a field isn't required
            print('WARNING: row has incorrect number of columns (this can be caused by blank lines or by forgetting to put comma-separated sequences between quote characters (default: ")')
            return None
        return_value = {}
        #### This fails on CSV files with only headers
        for attribute,guidance in self.attributes.items():
            string_value = row[guidance[0]]
            if string_value == '' and guidance[1] != str:
                return_value[attribute] = None
            elif guidance[1] == int:
                return_value[attribute] = int(float(string_value))
            else:
                return_value[attribute] = guidance[1](string_value)
        return return_value
    
    def close(self):
        self.csv_file.close()

class DatabaseConnection:
    
    def __init__(self,fqdn_or_ip_address,username=None,password=None,token=None):
        '''
Manages HTTPS communication with specified web server using Django REST framework

Parameters
----------
fqdn_or_ip_address : string
    Fully-qualifed domain name or IP address of web server

username : string
    Django username

password : string
    Django password

token : string
    Authentication token associated with user account on web server using Django REST framework; files containing tokens should not be readable by other users who should not have corresponding access to the web server.
        '''

        assert type(fqdn_or_ip_address) == str
        
        self.fqdn_or_ip_address = fqdn_or_ip_address

        self.username = username

        self.password = password
        
        self.token = token

        if self.token == None and self.username != None and self.password != None:

            self.token = self.retrieve_authentication_token(self.username,self.password)
            
    def set_authentication_token(self,authentication_token):

        self.token = authentication_token
        
    def request_and_receive(self,uri,headers={},unencoded_data=None,encoded_data=None):
        '''
Send HTTPS request to server and return response

Parameters
----------
uri : string
    Universal resource identifier, beginning with "https://" prefix

headers : dict
    Headers to be included in HTTPS request

unencoded_data : dict
    Data to be sent in request using POST method after conversion to "percent-encoding." If this is specified, ``encoded_data`` must not be specified. If neither is specified, a GET method is used.

encoded_data : bytes
    Data to be sent verbatim in request using POST method. This is ignored if ``unencoded_data`` must not be specified.

Returns
-------
dict
    Response, represented by a dictionary
        '''
        if unencoded_data != None:
            assert encoded_data == None

            encoded_data = (json.dumps(unencoded_data)).encode(encoding='utf-8')
            headers['Content-Type'] = 'application/json'

        request = urllib.request.Request(url=uri,headers=headers,data=encoded_data)            

        # It doesn't appear that there's any need to close a connection explicitly
        returned = urllib.request.urlopen(request)

        # convert bytes to str and then to dict
        return json.loads(returned.read().decode('utf-8'))

    def relative_request_and_receive(self,relative_location,headers={},unencoded_data=None,encoded_data=None):
        '''
Send HTTPS request to server and return response

Parameters
----------
relative_location : string
    Part of the universal resource identifier, following the "https://<hostname>/" prefix

headers : dict
    Headers to be included in HTTPS request

unencoded_data : dict
    Data to be sent in request using POST method after conversion to "percent-encoding." If this is specified, ``encoded_data`` must not be specified. If neither is specified, a GET method is used.

encoded_data : bytes
    Data to be sent verbatim in request using POST method. This is ignored if ``unencoded_data`` must not be specified.

Returns
-------
dict
    Response, represented by a dictionary
        '''

        uri = 'https://' + self.fqdn_or_ip_address + '/' + relative_location
        
        return self.request_and_receive(uri,headers=headers,unencoded_data=unencoded_data,encoded_data=encoded_data)

#     def quote_relative_request_and_receive(self,relative_location,headers={},unencoded_data=None,encoded_data=None):
#         '''
# Send HTTPS request to server and return response

# Parameters
# ----------
# relative_location : string
#     Part of the universal resource identifier, following the "https://<hostname>/" prefix

# headers : dict
#     Headers to be included in HTTPS request

# unencoded_data : dict
#     Data to be sent in request using POST method after conversion to "percent-encoding." If this is specified, ``encoded_data`` must not be specified. If neither is specified, a GET method is used.

# encoded_data : bytes
#     Data to be sent verbatim in request using POST method. This is ignored if ``unencoded_data`` must not be specified.

# Returns
# -------
# dict
#     Response, represented by a dictionary
#         '''

#         uri = 'https://' + self.fqdn_or_ip_address + '/' + urllib.parse.quote(relative_location)

#         return self.request_and_receive(uri,headers=headers,unencoded_data=unencoded_data,encoded_data=encoded_data)
    
    def retrieve_authentication_token(self,username,password):
        '''
Use credentials to retrieve authentication token

Parameters
----------
username : string
    Django username

password : string
    Django password

Returns
-------
string
    Authentication token
        '''

        login_data = {'username':username,'password':password}
        
        token_dict = self.relative_request_and_receive('api-token-auth/',unencoded_data=login_data)

        return token_dict['token']
    
    def authenticated_relative_request_and_receive(self,relative_location,headers={},unencoded_data=None,encoded_data=None):
        '''
Send HTTPS request to server, along with authentication token, and return response

Parameters
----------
relative_location : string
    Part of the universal resource identifier, following the "https://<hostname>/" prefix

headers : dict
    Headers to be included in HTTPS request

unencoded_data : dict
    Data to be sent in request using POST method after conversion to "percent-encoding." If this is specified, ``encoded_data`` must not be specified. If neither is specified, a GET method is used.

encoded_data : bytes
    Data to be sent verbatim in request using POST method. This is ignored if ``unencoded_data`` must not be specified.

Returns
-------
dict
    Response, represented by a dictionary
        '''

        assert self.token != None

        headers['Authorization'] = 'Token ' + self.token
        
        return self.relative_request_and_receive(relative_location,headers=headers,unencoded_data=unencoded_data,encoded_data=encoded_data)

#     def authenticated_quote_relative_request_and_receive(self,relative_location,headers={},unencoded_data=None,encoded_data=None):
#         '''
# Send HTTPS request to server, along with authentication token, and return response

# Parameters
# ----------
# relative_location : string
#     Part of the universal resource identifier, following the "https://<hostname>/" prefix

# headers : dict
#     Headers to be included in HTTPS request

# unencoded_data : dict
#     Data to be sent in request using POST method after conversion to "percent-encoding." If this is specified, ``encoded_data`` must not be specified. If neither is specified, a GET method is used.

# encoded_data : bytes
#     Data to be sent verbatim in request using POST method. This is ignored if ``unencoded_data`` must not be specified.

# Returns
# -------
# dict
#     Response, represented by a dictionary
#         '''

#         assert self.token != None

#         headers['Authorization'] = 'Token ' + self.token
        
#         return self.quote_relative_request_and_receive(relative_location,headers=headers,unencoded_data=unencoded_data,encoded_data=encoded_data)
    
class DataConnection:

    def __init__(self,server,username=None,password=None):

        self.server = server
        self.server_re = self.server.translate({46:r'\.'})

        self.model_name_re = re.compile(r'^.+\(([A-Za-z_.]+),')
        
        # server_bytearray = bytearray(len(self.server)+self.server.count('.'))
        # dot_count = 0
        # for index in range(len(self.server)):
        #     if self.server[index] == '.':
        #         dot_count +=1
        #     server_bytearray[index + dot_count] = ord(self.server[index])
        # self.server_re = server_bytearray.decode()
        # print(self.server_re)
        
        if username != None and password != None:
            self.authenticated_database_connection = DatabaseConnection(self.server,username=username,password=password)
            assert self.authenticated_database_connection != None, 'ERROR: could not open authenticated database connection'
        else:
            self.authenticated_database_connection = None
            self.unauthenticated_database_connection = DatabaseConnection(self.server)

        self.model_descriptions = project.models

    def get_record_form(self,model_name):

        form = {}
        
        for attribute, description in self.model_descriptions[model_name].items():
            attribute_type = description['type']

            if 'Char' in attribute_type or 'Text' in attribute_type or 'URL' in attribute_type:
                form[attribute] = ''
            else:#    if 'Int' in attribute_type or 'Float' in attribute_type
                form[attribute] = None                
        
        return form
        
    def upload_record(self,unencoded_data,model_name):
        '''
Upload a single record to server. The record must be directly understandable under the Django REST Framework. A ForeignKey or OneToOneField will be represented by a URI yielding the detailed view for the related record. We have not yet planned for a ManyToManyField.

Parameters
----------
unencoded_data : dict
    Record description

model_name : string
    Name of corresponding model in project.models
        '''
        # Lower model name to get around what might be a bug in Django REST Framework
        self.authenticated_database_connection.authenticated_relative_request_and_receive(model_name.lower() + '/',unencoded_data=unencoded_data)

    def upload(self,filename,model_name,Plugin=CSVDataPlugin):
        '''
Upload all records in data file to server

Parameters
----------
filename : string
    Path to data file

model_name : string
    Name of corresponding model in project.models

Plugin : DataPlugin
    Plugin used to extract records from provided data file
        '''
        assert self.authenticated_database_connection != None, 'ERROR: username and/or password not provided for authenticated connection'
        
        source = Plugin(model_name,filename)

        # Determine if this model has relationship fields that might require that records be processed before being stored. Users will typically not know the default primary keys of related records, so we should provide more convenient methods of referencing database records. Since this is on the client side, we cannot run Python code that directly performs queries. Finding a way to send Python code seems like security risk.
        # We will instead accept URIs that describe queries. The purpose of the filter form is so that users don't need to learn the URI query system, although it's not difficult, but remembering the identifiers might be troublesome. Lookups needed to find related objects are probably usually less involved.
        # It might be convenient to specify abbreviated lookups rather than full URIs. Before sending a request, the client should check that any URI given is either a reasonable reference to a database record or a reasonable query. If something else is given, the client should transform it into a query URI if possible. For a direct reference to a database record, we can then attempt to store the new record. For an indirect reference, perform the query, ensure that only one record is returned for a ForeignKey or OneToOneField, and then store the modified record with the direct record reference. For a ManyToManyField, we need to find out more about what is expected.
        
        one_record = {}
        many_records = {}
        for attribute, parameters in project.models[model_name].items():
            if 'ForeignKey' in parameters['type'] or 'OneToOneField' in parameters['type']:
                # Extract the name of the related model
                match = self.model_name_re.match(parameters['type'])
                related_model_name_lower = match.group(1).lower()

                # Store compiled regular expressions to recognize URIs forms that might be valid references to stored model instances or valid filter requests
                #### These could be tightened, but they're really just a convenience to catch errors on the client side before clearly bad requests are sent
                one_record[attribute] = {'related_model_name_lower':related_model_name_lower,'direct_re':re.compile(r'^https?://' + self.server_re + '/' + related_model_name_lower + '/\d+/$'),'indirect_re':re.compile(r'^([A-Za-z_]+=.*?&)*[A-Za-z_]+=.*?[^/]$|^https?://' + self.server_re + '/' + related_model_name_lower + '/\?([A-Za-z_]+=.*?&)*[A-Za-z_]+=.*?[^/]$')}
            elif 'ManyToManyField' in parameters['type']:

                # Extract the name of the related model
                match = self.model_name_re.match(parameters['type'])
                related_model_name_lower = match.group(1).lower()

                # Store compiled regular expressions to recognize URIs forms that might be valid references to stored model instances or valid filter requests
                #### These could be tightened, but they're really just a convenience to catch errors on the client side before clearly bad requests are sent
                many_records[attribute] = {'related_model_name_lower':related_model_name_lower, 'direct_re':re.compile(r'^(\s*https?://' + self.server_re + '/' + related_model_name_lower + '/\d+/\s*)*$'), 'indirect_re':re.compile(r'^\s*(([A-Za-z_]+=.*?&)*[A-Za-z_]+=.*?[^/]\s*)*$|^\s*(https?://' + self.server_re + '/' + related_model_name_lower + '/\?([A-Za-z_]+=.*?&)*[A-Za-z_]+=.*?[^/]\s*)*$')}
                
        # It appears that the serializers only handle one dictionary-like object at a time, so generate a dictionary from each record and store it.
        processed_unencoded_data = {}
        for unprocessed_unencoded_data in source:

            # Skip bad lines
            if unprocessed_unencoded_data == None:
                continue

            for key, value in unprocessed_unencoded_data.items():

                if key in one_record:
                    if one_record[key]['direct_re'].match(value):
                        # URI is likely a direct model record reference and can be passed along directly for storage
                        processed_unencoded_data[key] = value
                    elif one_record[key]['indirect_re'].match(value):
                        # URI is likely a query string
                        if value[0:4] == 'http':
                            # Use the provided URI directly
                            #### This might not be the most efficient way to do this
                            urlsplit = urllib.parse.urlsplit(value)
                            path = one_record[key]['related_model_name_lower'] + '/?' + urlsplit.query
                        else:
                            # Construct a URI from the shorthand entry
                            #### We are assuming HTTPS here, since HTTP will redirect if HTTPS is available and we want to avoid that inefficiency. However, it's possible that someone will set up an HTTP-only server
                            path = one_record[key]['related_model_name_lower'] + '/?' + value
                        # Make the query request and confirm that only a single record is returned
                        matches = self.path_download(path)
                        #### should have a friendlier way of catching bad queries
                        assert len(matches) == 1
                        # It seems that Django represents references to objects using HTTP, not HTTPS
                        processed_unencoded_data[key] = 'http://' + self.server + '/' + one_record[key]['related_model_name_lower'] + '/' + str(matches[0]['id']) + '/'
                    else:
                        #### no usable model reference information has been provided
                        #### should make it easy for users to find the erroneous entry
                        #### should make it easy to not add duplicate entries and to remove duplicates
                        print(processed_unencoded_data)
                        raise AssertionError('Bad related model specification')

                elif key in many_records:

                    if many_records[key]['direct_re'].match(value):
                        # URIs are likely direct model record references and can be packed into a list and passed along for storage
                        processed_unencoded_data[key] = value.split()

                    elif many_records[key]['indirect_re'].match(value):
                        # Likely a query string
                        # We are requiring that all of the individual references use the same form (either a URI or an abbreviated form); a single record cannot use both forms 
                        queries = []
                       
                        if value[0:4] == 'http':
                            # Use the provided URIs directly
                            #### This might not be the most efficient way to do this
                            for uri in value.split():
                                urlsplit = urllib.parse.urlsplit(uri)
                                queries.append(many_records[key]['related_model_name_lower'] + '/?' + urlsplit.query)
                        else:
                            # Construct a URI from the shorthand entry
                            #### We are assuming HTTPS here, since HTTP will redirect if HTTPS is available and we want to avoid that inefficiency. However, it's possible that someone will set up an HTTP-only server
                            for abbreviation in value.split():
                                queries.append(many_records[key]['related_model_name_lower'] + '/?' + abbreviation)

                        urls = []
                        
                        # Make the query request and add all records
                        for query in queries:
                            matches = self.path_download(query)

                            assert len(matches) != 0
                            
                            for match in matches:

                                # It seems that Django represents references to objects using HTTP, not HTTPS
                                urls.append('http://' + self.server + '/' + many_records[key]['related_model_name_lower'] + '/' + str(matches[0]['id']) + '/')
                                
                        processed_unencoded_data[key] = urls
                        
                    else:
                        #### no usable model reference information has been provided
                        #### should make it easy for users to find the erroneous entry
                        #### should make it easy to not add duplicate entries and to remove duplicates
                        print(value)
                        raise AssertionError('Bad related model specification')

                else:
                    processed_unencoded_data[key] = value

            self.upload_record(processed_unencoded_data,model_name)
        
        source.close()

    # I'm not expecting people to filter on relationship fields because they can filter the related objects and then follow the relationships if needed. I don't see a need to exclude filters yet though
        
    def get_filter_form(self,model_name):
        form = {}
        for attribute,parameters in self.model_descriptions[model_name].items():
            filters = {}
            
            for attribute_filter in parameters['filters']:

                # Set empty values that provide hints about form use
                if attribute_filter in ['in']:
                    filters[attribute_filter] = []                    
                elif attribute_filter in ['istartswith','icontains','iendswith','iregex','search','startswith','contains','endswith','regex']:
                    filters[attribute_filter] = ''
                else:
                    #if attribute_filter in ['exact','iexact','gte','lte']:
                    filters[attribute_filter] = None
                    
            form[attribute] = filters
            
        # Always add filters for id field (added automatically by Django)
        form['id'] = {'exact':None, 'in':[]}
            
        return form
        
    def get_filter_url(self,model_name,filter_form):
        model_attributes = self.model_descriptions[model_name]
        url = '?'
        for attribute in filter_form:
            if attribute == 'id':
                for drffilter in filter_form[attribute]:
                    assert drffilter in ['exact','in'], "Error: " + drffilter + " is not a valid filter for ' + model_name + ' attribute " + attribute + "."
                    if filter_form[attribute][drffilter] != None and filter_form[attribute][drffilter] != '' and filter_form[attribute][drffilter] != [] and filter_form[attribute][drffilter] != ():

                        # It seems that '__exact' is not just superfluous, but actually wrong                        
                        if drffilter == 'exact':
                            url += attribute + "=" + str(filter_form[attribute][drffilter]) + "&"                            
                        elif type(filter_form[attribute][drffilter]) == tuple or type(filter_form[attribute][drffilter]) == list:
                            url += attribute + "__" + drffilter + "="                            
                            start = True
                            for value in filter_form[attribute][drffilter]:
                                if start:
                                    url += str(value)
                                    start = False
                                else:
                                    #### Might want to pass this through the encoder rather than hardcoding the separator
                                    url += "%2C" + str(value)
                            url += '&'
            else:
                assert attribute in model_attributes, "Error: " + attribute + " is not an ' + model_name + ' attribute."
                for drffilter in filter_form[attribute]:
                    assert drffilter in model_attributes[attribute]["filters"], "Error: " + drffilter + " is not a valid filter for ' + model_name + ' attribute " + attribute + "."
                    if filter_form[attribute][drffilter] != None and filter_form[attribute][drffilter] != '' and filter_form[attribute][drffilter] != [] and filter_form[attribute][drffilter] != ():

                        if type(filter_form[attribute][drffilter]) == int or type(filter_form[attribute][drffilter]) == float:
                            # It seems that '__exact' is not just superfluous, but actually wrong                        
                            if drffilter == 'exact':
                                url += attribute + "=" + str(filter_form[attribute][drffilter]) + "&"                            
                            else:
                                url += attribute + "__" + drffilter + "=" + str(filter_form[attribute][drffilter]) + "&"
                        elif type(filter_form[attribute][drffilter]) == str:
                            if drffilter == 'exact':
                                url += attribute + "=" + filter_form[attribute][drffilter] + "&"
                            else:
                                url += attribute + "__" + drffilter + "=" + filter_form[attribute][drffilter] + "&"
                        elif type(filter_form[attribute][drffilter]) == tuple or type(filter_form[attribute][drffilter]) == list:
                            # This will never correspond to an 'exact' filter
                            url += attribute + "__" + drffilter + "="
                            
                            start = True
                            for value in filter_form[attribute][drffilter]:
                                if start:
                                    url += str(value)
                                    start = False
                                else:
                                    #### Might want to pass this through the encoder rather than hardcoding the separator
                                    url += "%2C" + str(value)
                            url += '&'
        return url
        
    def filtered_download(self,model_name,filter_form):
        '''
Download all records specified by filter_form from server

Parameters
----------
model_name : string
    Name of corresponding model in project.models

filter_form : dict
    Description of filter parameters consistent with format used by self.get_filter_form()
        '''

        filter_url = self.get_filter_url(model_name,filter_form)
        ## Authenticated connections might not be required to download, might want to make that configurable
        # Lower model_name to get around what might be a bug in Django REST Framework
        if self.authenticated_database_connection == None:

            page = self.unauthenticated_database_connection.relative_request_and_receive(model_name.lower() + '/' + filter_url)
            results = page['results']        

            while True:

                if page['next'] == None:
                    break
                else:
                    next_page = self.unauthenticated_database_connection.relative_request_and_receive(page['next'].rsplit(self.server+'/')[1])
                    page = next_page
                    results.extend(page['results'])
            
        else:

            page = self.authenticated_database_connection.authenticated_relative_request_and_receive(model_name.lower() + '/' + filter_url)
            results = page['results']        

            while True:

                if page['next'] == None:
                    break
                else:
                    next_page = self.authenticated_database_connection.authenticated_relative_request_and_receive(page['next'].rsplit(self.server+'/')[1])
                    page = next_page
                    results.extend(page['results'])

        return results

    def path_download(self,path):

        ## Authenticated connections might not be required to download, might want to make that configurable
        # Lower model_name to get around what might be a bug in Django REST Framework
        page = self.authenticated_database_connection.authenticated_relative_request_and_receive(path)
        results = page['results']        
        
        while True:
            
            if page['next'] == None:
                break
            else:
                next_page = self.authenticated_database_connection.authenticated_relative_request_and_receive(page['next'].rsplit(self.server+'/')[1])
                page = next_page
                results.extend(page['results'])

        return results
    
