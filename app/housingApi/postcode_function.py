import requests



custom_ward_mapping = {
    "M1": "City Centre",
    "M2": "Spinningfields",
    "M3": "Deansgate",
    "M4": "Northern Quarter",
    "M5": "Salford Quays",
    "M6": "Pendleton",
    "M7": "Strangeways",
    "M8": "Cheetham Hill",
    "M9": "Blackley",
    "M11": "Beswick",
    "M12": "Ardwick",
    "M13": "Fallowfield",
    "M14": "Withington",
    "M15": "Chorlton",
    "M16": "Whalley Range",
    "M17": "Old Trafford",
    "M18": "Gorton",
    "M19": "Levenshulme",
    "M20": "Didsbury",
    "M21": "Chorlton-cum-Hardy",
    "M22": "Wythenshawe",
    "M23": "Woodhouse Park",
    "M24": "Heywood",
    "M25": "Prestwich",
    "M26": "Radcliffe",
    "M27": "Swinton",
    "M28": "Walkden",
    "M29": "Little Hulton",
    "M30": "Eccles",
    "M31": "Partington",
    "M32": "Stretford",
    "M33": "Sale",
    "M34": "Denton",
    "M35": "Mossley",
    "M36": "Ashton-under-Lyne",
    "M37": "Droylsden",
    "M38": "Audenshaw",
    "M39": "Barton-upon-Irwell",
    "M40": "Harpurhey",
    "M41": "Partington",
    "M42": "Stalybridge",
    "M43": "Gorse Hill",
    "M44": "Irlam",
    "M45": "Whitefield",
    "M46": "Atherton",
    "M47": "Saddleworth",
    "M48": "Boothstown",
    "M49": "Walkden",
    "M50": "Salford Quays",
    "M51": "Swinton",
    "M52": "Kersal",
    "M53": "Kearsley",
    "M54": "Kersley",
    "M55": "Manchester City Centre",
    "M56": "Baguley",
    "M57": "Hulme",
    "M58": "Blackley North",
    "M59": "Manchester North East",
    # More postcodes can be added here
}
import requests

# Example dictionary for Manchester postcodes to wards (you can expand this with actual data)



def get_manchester_area(postcode):
    """
    Takes a UK postcode and returns the corresponding area in Manchester
    using the Postcodes.io API if not found in the custom dictionary.
    """
    postcode = postcode.replace(" ", "").upper()  # Normalize postcode

    # Check if postcode is already in the dictionary
    if postcode in custom_ward_mapping:
        return custom_ward_mapping[postcode]

    # If not found in the dictionary, make an API request
    url = f"https://api.postcodes.io/postcodes/{postcode}"

    try:
        response = requests.get(url)
        data = response.json()

        # Check if "result" exists in API response
        if response.status_code == 200 and data.get("result"):
            district = data["result"].get("admin_district", "Unknown District")
            ward = data["result"].get("admin_ward", "Unknown Ward")

            # Return ward from API response
            return f"{ward}"

        elif response.status_code == 404:
            return "Invalid postcode"
        else:
            return "Unknown area (API response error)"

    except requests.exceptions.RequestException as e:
        return f"Network error: {str(e)}"




