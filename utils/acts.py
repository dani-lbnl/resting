import rest_client

server = 'covidscreen.lbl.gov'        
username = 'khiga'
password = 'gN03#AwJ!Wla'

connection = rest_client.DataConnection(server,username,password)

connection.upload('../acts/test_results.csv','Result')

#connection.upload('../acts/processed_metadata_ieee8023.csv','Source')

# Get blank form for describing filter queries
#source_filter_form = connection.get_filter_form('Source')
#result_filter_form = connection.get_filter_form('Result')

# Customize the query form
#source_filter_form['id']['in'] = [65,66]

# Make the request
#results = connection.download('Source',source_filter_form)

#print(results)
#print(connection.get_record_form('Source'))
