from playwright.sync_api import sync_playwright
import requests
from main import HouseRequests
import re
import datetime


def scrape_property_listings():
    house_listings = []
    with sync_playwright() as p:
        for page in range(1, 19):  # modify upper boundary to number of pages on website
            url = "https://www.unihomes.co.uk/student-accommodation/manchester" + f"?page={page}"
            # Launch the browser (WebKit for Safari)
            browser = p.webkit.launch(headless=False)
            page = browser.new_page()

            # Navigate to the target URL
            page.goto(url)

            # Wait for the container with all listings to load
            page.wait_for_selector('.col-12.properties_listing_container')

            # Query all individual listings inside the container
            listings = page.query_selector_all(
                '.col-12.properties_listing_container .col-12.col-sm-6.col-xl-4.property-listing-column')

            for listing in listings:
                address = listing.inner_text().replace("\n", " ").replace("Featured", "").replace("Bills Included",
                                                                                                  "").strip()  # This will get the full text of the listing

                link = listing.query_selector('a').get_attribute("href")
                img = page.query_selector_all('.aspect-ratio-airbnb.swiper-slide.swiper-slide-active')

                # new code
                swiper_wrapper = page.query_selector('.swiper-wrapper')
                image_elements = swiper_wrapper.query_selector_all('img')
                image_links = []
                for img in image_elements:
                    src = img.get_attribute('src')
                    if src:
                        if src[0:4] != "data":
                            image_links.append(src)

                try:
                    split_listing(address, link, image_links)
                except:
                    pass

                house_listings.append(address)

            # Print the result (all listings in an array)
        for house in house_listings:
            # print(house)
            pass
            # Close the browser
        browser.close()


def split_listing(listing, link, img_link):
    bathrooms_split = listing.split(" bathrooms")
    bathrooms_number = bathrooms_split[0].strip()  # no of bathrooms
    bedrooms_split = bathrooms_split[1].split(" Bedroom")
    bedrooms_number = bedrooms_split[0].strip()  # number of bedrooms
    new_arr = bedrooms_split[1]
    if "House" in new_arr:
        new_arr = new_arr.split("House")
    else:
        new_arr = new_arr.split("Apartment")
    new_arr = new_arr[1].strip()
    road = new_arr.split(",")
    date_avai_from = road[-1].split("from ")[1]  # date available from
    road_area = road[0]
    road = road[1]
    road = road.split("£")
    road = road[1].split("per")
    cost_pw = road[0].strip()  # cost pw
    added = road[-1].split(" ")[-1]  # date added
    postcode = get_postcode("Manchester, United Kingdom", road_area)
    print(f"Property has {bedrooms_number} bedrooms, {bathrooms_number} bathrooms, is in {road_area}, costs £{cost_pw} per week, was added {added} and is available from {date_avai_from}, postcode is {postcode}, link is {link}, image link is {img_link}")

    add_to_database(bedrooms_number, bathrooms_number, postcode, cost_pw, added, date_avai_from, link, img_link)


def get_postcode(city, area):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        'q': f'{area}, {city}',
        'format': 'json',
        'addressdetails': 1
    }

    headers = {
        'User-Agent': 'YourAppName/1.0 (your_email@example.com)'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:

            postcode = data[0].get('address', {}).get('postcode')
            return postcode
        else:
            return "No results found."
    else:
        return f"Error: {response.status_code}"


def date_to_epoch(date_str):
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

    date_obj = datetime.strptime(date_str, "%d %B %Y")

    return int(date_obj.timestamp())


def add_to_database(bedrooms_number, bathrooms_number, postcode, cost_pw, added, date_avai_from, link, img_links):
    try:
        house_requests = HouseRequests()
        house_requests.add_house(bedrooms_number, bathrooms_number, postcode, cost_pw, added, date_avai_from, link, img_links)
        house_requests.session.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # scrape_property_listings()
    pass
