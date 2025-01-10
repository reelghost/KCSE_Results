import requests
from bs4 import BeautifulSoup
import streamlit as st
from time import sleep

def check_results(index_number, name="**"):
    url = "https://results.knec.ac.ke/Home/CheckResults"
    payload = {
        "indexNumber": index_number,
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


def fetch_school_results(school_code, max_attempts=300):
    st.write(f"Fetching results for school code: {school_code}")
    results_table = []
    counter = 1

    while counter <= max_attempts:
        index_number = f"{school_code}{counter:03}"
        results = check_results(index_number)

        if "error" in results:
            if results["error"] == "Not found":
                st.write(f"Index number {index_number}: Not found.")
                break
            else:
                st.error(results["error"])
                break
        else:
            name_and_index = results["general_info"][1]  # 2nd in the list
            mean_grade = results["general_info"][-1].strip("Mean Grade:")  # Last in the list

            # Append result to display table
            results_table.append([index_number, name_and_index, mean_grade])

            # Display table in real-time
            st.table(results_table)

        counter += 1
        sleep(0.5)  # Sleep for 0.5 seconds to avoid being blocked by the server


# Streamlit UI
st.title("KNEC Results Fetcher")
school_code = st.text_input("Enter school code:", "")
if school_code:
    fetch_school_results(school_code)
