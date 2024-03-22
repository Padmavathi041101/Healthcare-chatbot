import re, json

#Phrasing tool
action_pattern = r"Action: (.+?)\n+"
input_pattern = r"Action Input: \'''(.+?)\'''"
thought_pattern = r"Thought: (.+?)\n+"
location_pattern = r"Location: (.+?)\n+"

def extract_action_and_input(text):
    action = re.findall(action_pattern, text, re.DOTALL)
    action_input = re.findall(input_pattern, text, re.DOTALL)
    thoughts = re.findall(thought_pattern, text, re.DOTALL)
    location = re.findall(location_pattern, text, re.DOTALL)
    return action, action_input, thoughts, location

