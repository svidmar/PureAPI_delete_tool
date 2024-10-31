# Pure API Deletion Tool

## Overview

This Python script can be used to bulk delete content in Elsevier's Pure system, through the API. It reads UUIDs from a CSV file named uuids.csv (located in the same directory as the script) and sends DELETE requests to a specified endpoint in the Pure API. The user can dynamically select an endpoint, input the base URL, and provide the API key at runtime, ensuring flexibility and security. 

Before processing, the script provides a summary with the number of UUIDs to be deleted, allowing for user confirmation to prevent accidental deletions. But - goes without saying - use with caution and at your own risk :-) 

## Prerequisites

	•	Python 3.x
	•	Requests library: Install via pip install requests
	•	An API-key for Pure with write permission to relevant endpoints

## Usage

	1.	Prepare uuids.csv:
	•	Place the file in the same directory as the script.
	•	Ensure it contains a column named UUID with the UUIDs to be deleted.
	2.	Run the Script:

papidt.py


	3.	Provide Information When Prompted:
	•	Base URL: Enter the base URL for your Pure (e.g., xyz.elsevierpure.com).
	•	API Key: Enter your API key. This will not be logged or stored.
	•	Select Endpoint: Choose an endpoint by selecting the corresponding number.
	4.	Confirmation:
	•	The script displays a warning with the number of UUIDs to be deleted and the selected endpoint.
	•	Type yes to confirm, or any other input to cancel.

## Available Endpoints

The following endpoints can be selected for deletion:

	•	activities, applications, awards, classification-schemes, data-sets, equipment, events, external-organizations, external-persons, journals, organizations, persons, prizes, projects, publishers, research-outputs, users

## Logging

The script logs each deletion’s progress and response status code to:

	•	The console
	•	A log file: delete_requests.log (created in the same directory as the script)

## Example Output

Enter the base URL (e.g., vbn.aau.dk): vbn.aau.dk
Enter your API key: [Your_API_Key]

Available endpoints:
1. activities
2. applications
3. awards
...

Select an endpoint by number: 1
Selected endpoint: activities

WARNING: This will delete 10 activities. Are you sure? (yes/no): yes
UUID: 123e4517-e89b-12h3-a456-426614175000 - Status Code: 204
UUID: 123e4517-e99b-12c3-a456-426614177001 - Status Code: 204
...

## Error Handling

	•	FileNotFoundError: If uuids.csv is missing, the script logs an error and exits.
	•	Invalid Input: If an invalid endpoint number is entered, the script logs an error and exits.
	•	General Exceptions: Any other exceptions are logged with an error message.