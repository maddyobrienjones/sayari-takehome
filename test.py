import requests
import json

# sending post request to the API using the request details shown in the site's network activity when searching
req = requests.post("https://firststop.sos.nd.gov/api/Records/businesssearch",
                    headers = {
                      "accept": "*/*",
                      "accept-language": "en-US,en;q=0.9",
                      "authorization": "undefined",
                      "content-type": "application/json",
                      "sec-fetch-dest": "empty",
                      "sec-fetch-mode": "cors",
                      "sec-fetch-site": "same-origin",
                      "sec-gpc": "1"
                    },
                    data='{\"SEARCH_VALUE\":\"X\",\"STARTS_WITH_YN\":\"true\",\"ACTIVE_ONLY_YN\":true}')

# request returns json string which needs to be converted into a dictionary
businesses = json.loads(req.text)
# split into "template" and "rows", only care about "rows"
businesses = businesses["rows"]

# despite sending the proper request, not all start with the letter X, must be cleaned
business_names = list(businesses.keys())
for key in business_names:
    if businesses[key]["TITLE"][0][0] != "X":
        businesses.pop(key,None)


