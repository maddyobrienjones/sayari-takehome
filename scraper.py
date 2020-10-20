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
# json is split into "template" and "rows", only care about "rows"
businesses = businesses["rows"]

# despite sending the proper request, not all businesses returned start with the letter X, must be cleaned
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
    # request returns another json which can be loaded into a list of dictionaries
    info = json.loads(info.text)
    # first level of json only has one relevant key (DRAWER_DETAIL_LIST), so we index into that
    # and loop through corresponding list of dictionaries
    for dict in info["DRAWER_DETAIL_LIST"]:
        # each dictionary contains information for one attribute (attribute is stored in LABEL)
        # if that attribute doesn't have a corresponding column yet, add it in and fill with value
        if dict["LABEL"] not in df.columns:
            df[dict["LABEL"]] = ""
            df.at[df.ID == b, dict["LABEL"]] = dict["VALUE"]
        else:
            df.at[df.ID == b, dict["LABEL"]] = dict["VALUE"]

df.to_csv("request_data.csv")

