import json

from django.test import TestCase


# create User test class
class UserTest(TestCase):
    def test_user_creation(self):
        # create a user
        response = self.client.post('/api/signup',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'user created')
        

# write a unit test for login function
class LoginTest(TestCase):
    def test_login(self):
        # create a user
        response = self.client.post('/api/signup',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        
        # login user
        response = self.client.post('/api/login',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        self.assertEqual(response.status_code, 200)


class BondListTest(TestCase):

    def test_bond_list(self):
        # create a user
        response = self.client.post('/api/signup',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        # login user
        response = self.client.post('/api/login',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        #get token form response
        token = response.json()['token']
        header = header = {'HTTP_X_HTTP_METHOD_OVERRIDE': 'GET', 'HTTP_token': token}
        response = self.client.get('/api/bondlist', **header)
        self.assertEqual(response.status_code, 200)


class PublishBondTest(TestCase):
    def test_publish_bond(self):
        response = self.client.post('/api/signup',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        # login user
        response = self.client.post('/api/login',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        #get token form response
        token = response.json()['token']
        header = header = {'HTTP_X_HTTP_METHOD_OVERRIDE': 'POST', 'HTTP_token': token}
        data = {
            'name': 'test',
            'price': 100,
            'number_of_bond': 10
        }
        response = self.client.post('/api/publishbond',json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
    

#create a test class for bond_list_usdoller
class BondListUsdollerTest(TestCase):
    def test_bond_list_usdoller(self):
        # create a user
        response = self.client.post('/api/signup',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        # login user
        response = self.client.post('/api/login',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        #get token form response
        token = response.json()['token']
        header = header = {'HTTP_X_HTTP_METHOD_OVERRIDE': 'POST', 'HTTP_token': token}
        response = self.client.get('/api/listinusdollar', **header)
        self.assertEqual(response.status_code, 200)


#create a test class for buy_bond
class BuyBondTest(TestCase):
    def test_buy_bond(self):
        # create a user
        response = self.client.post('/api/signup',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        # login user
        response = self.client.post('/api/login',json.dumps({'email': 'test@t.com', 'password': 'test12345'}),content_type="application/json")
        #get token form response
        token = response.json()['token']
        #create a bond
        response = self.client.post('/api/publishbond',json.dumps({'name': 'test', 'price': 100, 'number_of_bond': 10}), content_type="application/json", **{'HTTP_X_HTTP_METHOD_OVERRIDE': 'POST', 'HTTP_token': token})
        #get bond id
        bond_id = response.json()['uuid']
        #create another user
        response = self.client.post('/api/signup',json.dumps({'email': 'test2@t.com', 'password': 'test12346'}),content_type="application/json")
        # login user
        response = self.client.post('/api/login',json.dumps({'email': 'test2@t.com', 'password': 'test12346'}),content_type="application/json")
        #get token form response
        token = response.json()['token']
        #buy bond
        final_response = self.client.post('/api/buybond',json.dumps({'id': bond_id}), content_type="application/json", **{'HTTP_X_HTTP_METHOD_OVERRIDE': 'POST', 'HTTP_token': token})
        self.assertEqual(final_response.status_code, 200)

        



        
       