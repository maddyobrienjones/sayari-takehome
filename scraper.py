import requests
import json
import pandas as pd

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
business_IDs = list(businesses.keys())
for key in business_IDs:
    if businesses[key]["TITLE"][0][0].strip() != "X":
        businesses.pop(key,None)

# business IDs we will use to query the API
business_IDs = list(businesses.keys())

business_names = [businesses[x]["TITLE"][0] for x in business_IDs]

#creating dataframe to populate
df = pd.DataFrame({"ID": business_IDs, "NAME": business_names})

# running requests for each business
for b in df.ID:
    info = requests.get("https://firststop.sos.nd.gov/api/FilingDetail/business/"+b+"/false",
                        headers = {
                          "accept": "*/*",
                          "accept-language": "en-US,en;q=0.9",
                          "authorization": "undefined",
                          "sec-fetch-dest": "empty",
                          "sec-fetch-mode": "cors",
                          "sec-fetch-site": "same-origin",
                          "sec-gpc": "1"
                        })
    info = json.loads(info.text)
    for dict in info["DRAWER_DETAIL_LIST"]:
        if dict["LABEL"] not in df.columns:
            df[dict["LABEL"]] = ""
        else:
            df.at[df.ID == b, dict["LABEL"]] = dict["VALUE"]

df.to_csv("request_data.csv")

