import unittest
import rest_client
import project

class TestClient(unittest.TestCase):

    def test_csv_upload(self):
        # Create CSV files
        with open('test_independent.csv','w') as csvfile:
            print('charfield,intfield,floatfield,urlfield,textfield',file=csvfile)
            for i in range(10):
                print(chr(65+i) + ',' + str(i) + ',' + str(i) + ',https://localhost/,' + chr(65+i),file=csvfile)

        # need to get username, password information in
        connection = rest_client.BatchConnection(project.server,username,password)
        connection.upload('test_independent.csv','Independent')
                    
        with open('test_dependent.csv','w') as csvfile:
            print('charfield,intfield,floatfield,urlfield,textfield',file=csvfile)
            for i in range(10):
                print(chr(65+i) + ',' + str(i) + ',' + str(i) + ',https://localhost/,' + chr(65+i),file=csvfile)
            
    def test_upload(self):
        pass

    def test_filter(self):
        pass

    def test_modify(self):
        pass
    
    def test_delete(self):
        pass

unittest.main()
