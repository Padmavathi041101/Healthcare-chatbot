from serpapi import GoogleSearch
import os


def search_place(search, latitude, longitude):
  params = {
    "engine": "google_maps",
    "q": search,
    "ll": f"@{latitude},{longitude},17z",
    "type": "search",
    "api_key": os.environ.get("serp_api")
  }
  information = []
  search = GoogleSearch(params)
  results = search.get_dict()
  local_results = results["local_results"] if "local_results" in results else [results["place_results"]]
  for i in range(len(local_results)):
      business_info = {
          "Name": local_results[i].get("title", None),
          "Type": local_results[i].get("type", None),
          "Address": local_results[i].get("address", None),
          "Phone": local_results[i].get("phone", None),
          "Rating": local_results[i].get("rating", None),
          "Operating_hours": local_results[i].get("operating_hours", local_results[i].get("hours", None)),
          "Website" : local_results[i].get("website", None)
      }

      business_info = {k: v for k, v in business_info.items() if v is not None}
      information.append(business_info)
  return information




