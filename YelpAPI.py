import requests

latitude = 33.838614
longitude = -118.376501

url = f"https://api.yelp.com/v3/businesses/search?latitude={latitude}&longitude={longitude}&radius=40000&sort_by=distance&limit=4"

headers = {
    "accept": "application/json",
    "Authorization": ""
}

response = requests.get(url, headers=headers)
response = response.json()

businesses_nearby = []
for spots in range(3):
    try:
        businesses_nearby.append((response["businesses"][spots]["categories"][0]["title"]))
    except IndexError:
        while len(businesses_nearby) != 2:
            spots += 1
            try:
                businesses_nearby.append((response["businesses"][spots]["categories"][0]["title"]))
            except IndexError:
                continue

    if len(businesses_nearby) == 2:
        break

#print(businesses_nearby)
