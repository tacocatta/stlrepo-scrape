import requests

LOGIN_URL = "https://stltestrepo-production.up.railway.app/login"
API_URL = "https://stltestrepo-production.up.railway.app/api/tests"

USERNAME = "RepoScrape"
PASSWORD = "RepoScrape"

def get_api_token():
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
    }

    return requests.post(LOGIN_URL, json=payload).json()["token"]

def main():
    token = get_api_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Make the GET request to the API endpoint
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    print("Request successful!")

    user_input = input("Do you want continue with the download? (y/n): ").strip().lower()
    if user_input != 'y':
        print("Download canceled.")
        return

    tests = response.json()["tests"]

    # Create a dictionary to store the URLs
    urls = dict()
    for test in tests:
        course = test["course"]
        unit = test["unit"]
        assessment_type = test["assessment_type"]
        version = test["version"]

        name = f"{course} {unit} {assessment_type } V{version}"

        url = test["file_path"]

        urls[name] = url
        # print(f"{course} {unit} {assessment_type } V{version}: {file_path}")

    # Download the files
    for name, url in urls.items():
        response = requests.get(url, stream=True)
        file_path = f"assessments/{name}.pdf"
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {name} to {file_path}")

if __name__ == "__main__":
    main()