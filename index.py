import requests
from bs4 import BeautifulSoup
from time import sleep

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
name = "**"

# Loop through index numbers 001 to 100
counter = 1
while counter <= 300:
    # index_number = f"02127115{counter:03}"
    index_number = f"02105109{counter:03}"

    results = check_results(index_number, name)

    if "error" in results:
        print(results["error"])
    else:
        school = results["general_info"][2]  # 3rd in the list
        name_and_index = results["general_info"][1]  # 2nd in the list
        mean_grade = results["general_info"][-1].strip("Mean Grade:")  # Last in the list
        print(f"{school} - {name_and_index} -> {mean_grade}")
        
        # for subject in results["detailed_results"]:
        #     print("\t".join(subject))

    counter += 1
    sleep(0.5)  # Sleep for 1 second to avoid being blocked by the server
    # break