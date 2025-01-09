import requests
from bs4 import BeautifulSoup


def check_results(indexNumber, name):
    url = "https://results.knec.ac.ke/Home/CheckResults"
    payload = {
        "indexNumber": indexNumber,
        "name": name
    }

    # Sending a POST request with the payload data
    response = requests.post(url, data=payload)

    # Check if the request was successful before parsing
    if response.status_code == 200:
        # Parse the response content using Beautiful Soup
        page = BeautifulSoup(response.content, 'html.parser')

        # Extract the results section
        results_table = page.find("table", class_="table-borderless")
        if results_table:
            # Extract general information like the student's name, school, and mean grade
            general_info = [row.get_text(strip=True) for row in results_table.find_all("th")]

            # Extract detailed subject grades
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
            return {"error": "Results table not found."}
    else:
        return {"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}


# Example usage
results = check_results("02123304112", "ELIZABETH THOYA")

# Print results
if "error" in results:
    print(results["error"])
else:
    print("General Info:")
    for info in results["general_info"]:
        print(info)

    print("\nDetailed Results:")
    for subject in results["detailed_results"]:
        print("\t".join(subject))
