Steps to set up the project.
1. run " git clone https://github.com/ongraphpythondev/backend_test.git "
2. move to the projet folder & create virtualenv using command "virtualenv venv"
3. run "pip install -r requirements.txt".
4. move to the project base dirctory
5. run "python manage.py migrate"
6. run django server "python manage.py runserver"

Now you have successfully run the server locally. You can test APIs using Postman or thunderclient


Unit Testing:
1. You can run test using "python manage.py test" (don't need to run django server)


Assumptions:
1. User can be seller or buyer both.
2. User can publish the bonds, A uuid will be generated for each bond and linked to user(seller) who published the bond.
3. Only authenticated user can access the all APIs.
4. User can't see bonds publised by himself.
5. User can't buy his own bond.
6. User can't buy bond if some user buy the bond already.


Here is the list of all endpoints & their request body

1.  POST -> http://127.0.0.1:8000/api/signup

    json body:
    
          {
           "email":"vip@gmail.com",
           "password":"vip12345"
           }
           
    Status: 200 OK

    Response body:
    
        {
          "message": "user created"
        }
        

2.  POST -> http://127.0.0.1:8000/api/login

    json body:
    
          {
           "email":"vip@gmail.com",
           "password":"vip12345"
           }
     
    Status: 200 OK

    Response body:
    
        {
          "message": "logged in",
          "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InZpcEBnbWFpbC5jb20iLCJwYXNzd29yZCI6InZpcDEyMzQ1IiwidXVpZCI6IjIwOTZlZjMwLWVjMTEtNDNhNi05NjI5LWE1MmJlN2RmMmFhNyIsImV4cCI6MTY0OTQzMDgzMn0.qPNLMm6ashErMJmmmNyR74EFn_ixjvDxQ7bx2VPIOiE"
        }
        

3.  POST -> http://127.0.0.1:8000/api/publishbond

    json body:
    
        {
        "name":"Bondtypeorname",
        "price":31,
        "number_of_bond": 3
        }

    Headers:
    
        {
            "Accept": "application/json",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InZpcEBnbWFpbC5jb20iLCJwYXNzd29yZCI6InZpcDEyMzQ1IiwidXVpZCI6IjIwOTZlZjMwLWVjMTEtNDNhNi05NjI5LWE1MmJlN2RmMmFhNyIsImV4cCI6MTY0OTQzMDgzMn0.qPNLMm6ashErMJmmmNyR74EFn_ixjvDxQ7bx2VPIOiE" 
        }
    
    Status: 200 OK

    Response body:
    
        {
          "message": "bond published",
          "uuid": "3890427a-9662-438e-a447-1e653b9a10ac"
        }


4. GET -> http://127.0.0.1:8000/api/bondlist
    json body: None

    Headers:
    
        {
            "Accept": "application/json",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InZpcEBnbWFpbC5jb20iLCJwYXNzd29yZCI6InZpcDEyMzQ1IiwidXVpZCI6IjIwOTZlZjMwLWVjMTEtNDNhNi05NjI5LWE1MmJlN2RmMmFhNyIsImV4cCI6MTY0OTQzMDgzMn0.qPNLMm6ashErMJmmmNyR74EFn_ixjvDxQ7bx2VPIOiE" 
        }

    Status: 200 OK

    Response body:
    
            {
            "bonds": [
            {
              "id": "fbedc5e9-67df-47e1-9514-066341b27acc",
              "name": "Befdsffdfw",
              "price": "310.0000",
              "number_of_bond": 3,
              "seller_id": 1,
              "buyer_id": null
            },
            {
              "id": "f78ea895-9289-449b-93c0-55c17550558a",
              "name": "Befdsffdsffdfw",
              "price": "310.0000",
              "number_of_bond": 3,
              "seller_id": 2,
              "buyer_id": 3
            }
          ]
        }
        

5.  GET -> http://127.0.0.1:8000/api/listinusdollar

    json body: None

    Headers:
    
        {
            "Accept": "application/json",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InZpcEBnbWFpbC5jb20iLCJwYXNzd29yZCI6InZpcDEyMzQ1IiwidXVpZCI6IjIwOTZlZjMwLWVjMTEtNDNhNi05NjI5LWE1MmJlN2RmMmFhNyIsImV4cCI6MTY0OTQzMDgzMn0.qPNLMm6ashErMJmmmNyR74EFn_ixjvDxQ7bx2VPIOiE" 
        }

    Status: 200 OK

    Response body:
    
        {
        "bonds": [
        {
          "id": "fbedc5e9-67df-47e1-9514-066341b27acc",
          "name": "Befdsffdfw",
          "price": 15.3766,
          "number_of_bond": 3,
          "seller_id": 1,
          "buyer_id": 3
        },
        {
          "id": "f78ea895-9289-449b-93c0-55c17550558a",
          "name": "Befdsffdsffdfw",
          "price": 15.3766,
          "number_of_bond": 3,
          "seller_id": 2,
          "buyer_id": 2
        },
        {
          "id": "3890427a-9662-438e-a447-1e653b9a10ac",
          "name": "Befdsffdfw",
          "price": 15.3766,
          "number_of_bond": 3,
          "seller_id": 3,
          "buyer_id": null
        }
         ]
       }
    

6.  POST -> http://127.0.0.1:8000/api/buybound

    json body: 
    
        {
        "id":"fbedc5e9-67df-47e1-9514-066341b27acc" #uuid of bond
        }

    Headers:
    
        {
            "Accept": "application/json",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InZpcEBnbWFpbC5jb20iLCJwYXNzd29yZCI6InZpcDEyMzQ1IiwidXVpZCI6IjIwOTZlZjMwLWVjMTEtNDNhNi05NjI5LWE1MmJlN2RmMmFhNyIsImV4cCI6MTY0OTQzMDgzMn0.qPNLMm6ashErMJmmmNyR74EFn_ixjvDxQ7bx2VPIOiE" 
        }

    Status: 200 OK

    Response body:
    
       {
        'message':'bond bought successfully'
       }
