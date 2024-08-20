import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Function to extract disaster event links from the GDACS main page
def extract_event_links():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the GDACS main page
    driver.get("https://www.gdacs.org/default.aspx")
    driver.implicitly_wait(10)  # Wait for elements to load

    # Dictionary to map event types to their corresponding full names and folder names
    event_types = {
        "EQ": "Earthquakes",
        "TC": "Cyclones",
        "FL": "Floods",
        "VO": "Volcanoes",
        "DR": "Droughts",
        "WF": "Wildfires"
    }

    # Dictionary to store lists of modified links for each event type
    all_links = {event: [] for event in event_types.values()}

    # Loop through each event type to extract and modify links
    for short_type, folder_name in event_types.items():
        event_links = driver.find_elements(By.CSS_SELECTOR, f'div[id^="gdacs_toc_{short_type}_"] a')
        for link in event_links:
            original_link = link.get_attribute('href')
            modified_link = original_link.replace("http://www.gdacs.org", f"https://www.gdacs.org/{folder_name}")
            all_links[folder_name].append(modified_link)

    driver.quit()
    return all_links

# Function to save the HTML content of each event page to the corresponding folder
def save_html_content(all_links, save_base_directory="D:\\Events"):
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Loop through each event type and its list of links
    for folder_name, links_list in all_links.items():
        # Create the event-specific folder if it doesn't exist
        save_directory = os.path.join(save_base_directory, folder_name)
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Save each link's HTML content with the event-specific filename
        for link in links_list:
            driver.get(link)
            page_source = driver.page_source

            # Extract the event ID from the link and use it to name the file
            event_id = link.split("eventid=")[1].split("&")[0]
            filename = f"{folder_name.lower()}_{event_id}.html"
            filepath = os.path.join(save_directory, filename)

            with open(filepath, "w", encoding="utf-8") as file:
                file.write(page_source)
            print(f"Saved {link} as {filename}")

    driver.quit()

if __name__ == "__main__":
    # Extract links for all event types
    event_links = extract_event_links()
    print("Extracted and Modified Event Links:")
    for event_type, links in event_links.items():
        print(f"{event_type}: {links}")

    # Save the HTML content of each link to its corresponding folder in D:\Events
    save_html_content(event_links)
