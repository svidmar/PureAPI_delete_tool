import csv
import requests
import logging
import os
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure logging to log progress and response codes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", handlers=[logging.FileHandler("delete_requests.log"), logging.StreamHandler()])

# Define available endpoints
available_endpoints = [
    "activities", "applications", "awards", "classification-schemes", "data-sets",
    "equipment", "events", "external-organizations", "external-persons", "journals",
    "organizations", "persons", "prizes", "projects", "publishers", "research-outputs", "users"
]

# Set a delay (in seconds) between requests to prevent rate-limiting
REQUEST_DELAY = 2

# Set up retry strategy for handling connection issues
retry_strategy = Retry(
    total=3,            # Retry up to 3 times
    backoff_factor=1,    # Wait 1, 2, 4 seconds between retries
    status_forcelist=[500, 502, 503, 504]  # Retry on server errors
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)

def delete_request(base_url, endpoint, api_key, uuid):
    url = f"https://{base_url}/ws/api/{endpoint}/{uuid}"
    headers = {
        "accept": "application/problem+json",
        "api-key": api_key
    }
    
    try:
        response = session.delete(url, headers=headers)
        logging.info(f"UUID: {uuid} - Status Code: {response.status_code}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while deleting UUID: {uuid} - {e}")
        return None

def count_uuids(csv_file):
    """Count the number of UUIDs in the 'UUID' column of the CSV file."""
    try:
        with open(csv_file, mode="r") as file:
            csv_reader = csv.DictReader(file)
            return sum(1 for row in csv_reader if row.get("UUID"))  # Only count rows with a UUID
    except FileNotFoundError:
        logging.error(f"The file '{csv_file}' was not found in the script's directory.")
        return 0

def main():
    # Prompt for base URL and API key
    base_url = input("Enter the base URL (e.g., xyz.elsevierpure.com): ")
    api_key = input("Enter your API key: ")

    # Display available endpoints and prompt for selection
    print("\nAvailable endpoints:")
    for i, endpoint in enumerate(available_endpoints, 1):
        print(f"{i}. {endpoint}")
    
    try:
        endpoint_choice = int(input("\nSelect an endpoint by number: "))
        if 1 <= endpoint_choice <= len(available_endpoints):
            endpoint = available_endpoints[endpoint_choice - 1]
            print(f"Selected endpoint: {endpoint}")
        else:
            logging.error("Invalid selection. Exiting script.")
            return
    except ValueError:
        logging.error("Invalid input. Please enter a number. Exiting script.")
        return

    # Set path for the CSV file in the same directory
    csv_file = os.path.join(os.path.dirname(__file__), "uuids.csv")
    
    # Count UUIDs in the CSV file for confirmation
    num_uuids = count_uuids(csv_file)
    if num_uuids == 0:
        logging.error("No UUIDs found in 'uuids.csv' or the file is missing. Exiting script.")
        return

    # Final warning and confirmation
    confirm = input(f"\nWARNING: This will delete {num_uuids} {endpoint}. Are you sure? (yes/no): ").strip().lower()
    if confirm != "yes":
        logging.info("Operation cancelled by the user.")
        return

    # Load UUIDs from CSV file and proceed with deletions
    try:
        with open(csv_file, mode="r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                uuid = row.get("UUID")
                if uuid:  # Ensure UUID is not empty
                    delete_request(base_url, endpoint, api_key, uuid)
                    time.sleep(REQUEST_DELAY)  # Delay to prevent rate-limiting
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
