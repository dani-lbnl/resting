import metadata

metadata_filename = '../metadata/metadata_ieee8023.csv'
username = 'khiga'
password = 'gN03#AwJ!Wla'
server = 'covidscreen.lbl.gov'

data = metadata.Metadata(metadata_filename,username,password,server)
data.push()

                





