import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description='Make a GET request to the search API.')
    parser.add_argument('--query', type=str, required=True, help='The search query for the API')
    parser.add_argument('--limit', type=int, default=10, help='Limit for the number of results')
    args = parser.parse_args()

    response = requests.get(f'http://127.0.0.1:5000/search?query={args.query}&limit={args.limit}')
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    if response.status_code == 200:
        print(f"JSON Response: {response.json()}")
    else:
        print("Failed to retrieve JSON data")

if __name__ == '__main__':
    main()
