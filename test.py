### Tests for receipts API ###

import requests
import json
import os
import sys

# global variables
if not len(sys.argv) == 2:
    print("Please run as python test.py <ip:port>")
    exit()
api_base_url = "http://"+sys.argv[1]
test_receipts = {}

def test_process(path="tests/"):
    global test_receipts

    for file in os.listdir(path):

        url = api_base_url+"/receipts/process"
        headers = {'Content-Type': 'application/json'}

        test_response = requests.post(url, data=open(path+file).read(), headers=headers)
        
        if test_response.status_code == 200:
            id = json.loads(test_response.text)["id"]
            test_receipts[id] = json.loads(open(path+file).read())
            if file[:5] == "ERROR":
                print(file, "processed successfully when it shouldn't have")
        elif test_response.status_code == 400:
            if not file[:5] == "ERROR":
                print(file, "returned error when it shouldn't have")

    print("/receipts/process tests done")
    return

def test_points():
    global test_receipts

    # test ids generated earlier
    for id in test_receipts.keys():
        #print("Testing the following receipt:", test_receipts[id])
        url = api_base_url+"/receipts/"+id+"/points"
        test_response = requests.get(url)
        if test_response.status_code == 404:
            print("/receipts/"+str(id)+"/points returned status 404")
        #print(test_response.text)

    # test cases with invalid id
    url = api_base_url+"/receipts/100000/points"
    test_response = requests.get(url)
    #print("Invalid id test 1 returned", test_response.text, "and status", test_response.status_code)
    if not test_response.status_code == 404:
        print("Unexpected status", test_response.status_code, "returned for invalid id /receipts/100000/points")

    url = api_base_url+"/receipts/test/points"
    test_response = requests.get(url)
    #print("Invalid id test 2 returned", test_response.text, "and status", test_response.status_code)
    if not test_response.status_code == 404:
        print("Unexpected status", test_response.status_code, "returned for invalid id /receipts/test/points")

    print("/receipts/{id}/points tests done")
    return

def run_tests():
    print("Testing /receipts/process...")
    test_process()

    print("\nTesting /receipts/{id}/points...")
    test_points()

run_tests()