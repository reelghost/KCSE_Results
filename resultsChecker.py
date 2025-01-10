import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Define a mapping for grades to ensure proper sorting
GRADE_MAPPING = {
    "A": 1, "A- (MINUS)": 2,
    "B+ (PLUS)": 3, "B (PLAIN)": 4, "B- (MINUS)": 5,
    "C+ (PLUS)": 6, "C (PLAIN)": 7, "C- (MINUS)": 8,
    "D+ (PLUS)": 9, "D (PLAIN)": 10, "D- (MINUS)": 11,
    "E (PLAIN)": 12,
}

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


def fetch_school_results(school_code, max_attempts=300, max_consecutive_not_found=5):
    # Fetch school name
    results = check_results(f"{school_code}001")
    school_name = results["general_info"][2]
    st.markdown(f"<h5 style='text-align: center;'>{school_name}</h5>", unsafe_allow_html=True)
    results_table = []

    # Create a placeholder for the table
    placeholder = st.empty()

    consecutive_not_found = 0  # Counter for consecutive "Not found" errors

    for counter in range(1, max_attempts + 1):
        index_number = f"{school_code}{counter:03}"
        results = check_results(index_number)

        if "error" in results:
            if results["error"] == "Not found":
                consecutive_not_found += 1  # Increment consecutive "Not found" counter
                if consecutive_not_found >= max_consecutive_not_found:
                    st.info("End of results reached.")
                    break  # Exit loop after consecutive "Not found" errors
                continue  # Skip to next iteration if not found
            else:
                st.error(results["error"])
                break  # Stop if other errors occur
        else:
            consecutive_not_found = 0  # Reset counter if results found
            name_and_index = results["general_info"][1]  # 2nd in the list
            name = name_and_index.split("-", 1)[-1].strip()  # Extract only the name
            mean_grade = results["general_info"][-1].strip("Mean Grade:")  # Last in the list

            # Append result to display table
            results_table.append([index_number, name, mean_grade])

            # Convert to DataFrame, sort, and update dynamically
            df = pd.DataFrame(results_table, columns=["Index Number", "Name", "Mean Grade"])

            # Sort by Mean Grade (convert grade to numeric using mapping for sorting)
            df["Grade Numeric"] = df["Mean Grade"].map(GRADE_MAPPING)
            df = df.sort_values(by="Grade Numeric").drop(columns=["Grade Numeric"])

            # Update the dynamic table without the index column
            placeholder.dataframe(df.reset_index(drop=True), use_container_width=True)

    return results_table



# Streamlit UI
st.title("KNEC Results Fetcher")
school_code = st.text_input("Enter school code:", "")

if school_code:
    try:
        results = fetch_school_results(school_code)
        if results:
            # Convert final results to DataFrame
            df = pd.DataFrame(results, columns=["Index Number", "Name", "Mean Grade"])
            # Sort by Mean Grade
            df["Grade Numeric"] = df["Mean Grade"].map(GRADE_MAPPING)
            df = df.sort_values(by="Grade Numeric").drop(columns=["Grade Numeric"])
    except:
        st.error("Check school code and try again.")
st.markdown("<div style='text-align: center; font-size: 14px;'><a style='text-decoration: none;font-weight: bold;' target='_blank' href='https://github.com/reelghost'>reelghost✔</a> made it</div>", unsafe_allow_html=True)
