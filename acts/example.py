import rest_client

server = 'covidscreen.lbl.gov'

# ## Retrieve token

# unauthenticated_database_connection = rest_client.DatabaseConnection(server)

# # Files containing credentials should not be readable by other users

# authentication_token = unauthenticated_database_connection.retrieve_authentication_token('khiga','gN03#AwJ!Wla')

# ## Use token to interact with database

# authenticated_database_connection = rest_client.DatabaseConnection(server,token=authentication_token)

username = 'khiga'
password = 'gN03#AwJ!Wla'

authenticated_database_connection = rest_client.DatabaseConnection(server,username=username,password=password)

print(authenticated_database_connection.authenticated_relative_request_and_receive('image/'))
