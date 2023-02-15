#!/usr/bin/env python3

import sys
import random
import requests
import populate

# Check if the user has provided a seed value as an argument
if len(sys.argv) < 2:
    print("No seed value provided. Aborting...")
    sys.exit(1)

# Retrieve the seed value from the command-line argument
seed = sys.argv[1]

# Generate the test data using the seed value
users, msgs = populate.get_data(seed)

# Define the URL of the website to test
URL = "http://127.0.0.1:80"

# Test for the /users endpoint
resp = requests.get(URL+"/users")

# Ensure the response status code is 200
assert resp.status_code == 200

# Ensure the response content type is JSON
assert 'application/json' in resp.headers['content-type']

# Ensure the number of users returned in the response matches the number of generated users
assert len(resp.json()["users"]) == len(users)

# Test the /users endpoint with a random limit value
length = random.randint(1,len(users))
resp = requests.get(URL+"/users?limit=" + str(length))
assert resp.status_code == 200
assert 'application/json' in resp.headers['content-type']
assert len(resp.json()["users"]) == length

# Test the /users endpoint with a negative limit value
length = -1
resp = requests.get(URL+"/users?limit=" + str(length))
assert resp.status_code == 500

# Test the /users endpoint with a SQL injection attack
resp = requests.get(URL+"/users?limit=1' or '1'='1")
assert resp.status_code == 500

# Test for the /messages endpoint
resp = requests.get(URL+"/messages")

# Ensure the response status code is 200
assert resp.status_code == 200

# Ensure the response content type is JSON
assert 'application/json' in resp.headers['content-type']

# Ensure the number of messages returned in the response matches the number of generated messages
assert len(resp.json()) == len(msgs)

# Test the /messages endpoint with a valid POST request
first = resp.json()[0]["name"]
resp = requests.post(URL+"/messages",data = {'name':first})
assert resp.status_code == 200
assert len(resp.json()) == 1

# Test the /messages endpoint with a SQL injection attack
resp = requests.post(URL+"/messages",data = {'name':"he' OR '1'='1"})
assert resp.status_code == 200

# Print a message indicating the testing is complete
print("All tests have passed successfully!")
