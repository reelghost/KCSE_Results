
import requests
from bs4 import BeautifulSoup

def check_results(indexNumber, name):
    url = "https://results.knec.ac.ke/Home/CheckResults"
    payload = {
        "indexNumber": indexNumber,
        "name": name
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        page = BeautifulSoup(response.content, 'html.parser')

        results_table = page.find("table", class_="table-borderless")
        if results_table:
            general_info = [row.get_text(strip=True) for row in results_table.find_all("th")]

            detailed_results = []
            results_grid = page.find("table", id="grid")
            if results_grid:
                for row in results_grid.find("tbody").find_all("tr"):
                    columns = [col.get_text(strip=True) for col in row.find_all("td")]
                    detailed_results.append(columns)

            return {
                "general_info": general_info,
                "detailed_results": detailed_results
            }
        else:
            return {"error": "Not found"}
    else:
        return {"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}


# List of names to try
names_list = ["MWANASITI", "JOSEPHINE"]

# Loop through index numbers 001 to 100
counter = 1
while counter <= 300:
    index_number = f"02127115{counter:03}"

    for name in names_list:
        print(f"Checking results for index number: {index_number}, name: {name}")

        results = check_results(index_number, name)

        if "error" in results:
            print(results["error"])
        else:
            print("General Info:")
            for info in results["general_info"]:
                print(info)

            print("\nDetailed Results:")
            for subject in results["detailed_results"]:
                print("\t".join(subject))

    counter += 1