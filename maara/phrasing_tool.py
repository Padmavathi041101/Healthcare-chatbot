import re, json

#Phrasing tool
action_pattern = r"Action: (.+?)\n+"
input_pattern = r"Action Input: \"(.+?)\""
thought_pattern = r"Thought: (.+?)\n+"
location_pattern = r"Location: (.+?)\n+"

def extract_action_and_input(text):
    action = re.findall(action_pattern, text, re.DOTALL)
    action_input = re.findall(input_pattern, text, re.DOTALL)
    thoughts = re.findall(thought_pattern, text, re.DOTALL)
    location = re.findall(location_pattern, text, re.DOTALL)
    return action, action_input, thoughts, location


# Your regex patterns
def extract_info_from_json(json_string):
    extracted_data = {}
    description_match = re.search(r'"Description": "(.*?)"', json_string, re.DOTALL)
    extracted_data['Description'] = description_match.group(1) if description_match else None
    business_name_match = re.search(r'"Business Name": "(.*?)"', json_string)
    extracted_data['Business Name'] = business_name_match.group(1) if business_name_match else None
    service_product_match = re.search(r'"Service/Product": "(.*?)"', json_string, re.DOTALL)
    extracted_data['Service/Product'] = service_product_match.group(1) if service_product_match else None
    price_range_match = re.search(r'"Price Range": "(.*?)"', json_string, re.DOTALL)
    extracted_data['Price Range'] = price_range_match.group(1) if price_range_match else None
    address_match = re.search(r'"Address": "(.*?)"', json_string, re.DOTALL)
    extracted_data['Address'] = address_match.group(1) if address_match else None
    years_in_business_match = re.search(r'"Years in Business": "(.*?)"', json_string)
    extracted_data['Years in Business'] = years_in_business_match.group(1) if years_in_business_match else None
    business_email_match = re.search(r'"Business Email": "(.*?)"', json_string)
    extracted_data['Business Email'] = business_email_match.group(1) if business_email_match else None
    business_number_match = re.search(r'"Business Number": "(.*?)"', json_string)
    extracted_data['Business Number'] = business_number_match.group(1) if business_number_match else None
    category_match = re.search(r'"Category": "(.*?)"', json_string)
    extracted_data['Category'] = category_match.group(1) if category_match else None
    return extracted_data


