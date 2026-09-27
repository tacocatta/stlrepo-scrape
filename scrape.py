import requests

URL = "https://stltestrepo-production.up.railway.app/api/tests"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIyLCJ1c2VybmFtZSI6IlRlc3QxMjM0Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODk2ODc0NzMsImV4cCI6MTc4OTc3Mzg3M30.gxsYb1n_l8L4f1Bo0zig9p9ABkwZbSqDz8pQkmtAJUc"

headers = {
    "Authorization": f"Bearer {token}"
}

# Make the GET request to the API endpoint
response = requests.get(URL, headers=headers)
if response.status_code == 200:
    print("Request successful!")

# print(response.json())
tests = response.json()["tests"]

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
    file_path = f"tests/{name}.pdf"
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {name} to {file_path}")