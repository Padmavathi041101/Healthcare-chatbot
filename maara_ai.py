# Standard library imports
import os
import json
import maara
import pytz

# Third-party library imports
from openai import OpenAI
from typing import Dict, Set, List, Optional
from datetime import datetime
from translator import GoogleTranslator

  
translator = GoogleTranslator()
#translator
def translator_ins(input, language):
  return translator.translate(input, target_language=language)

#Batch translator
def translate_dialogue(dialogue, target_language):
    for message in dialogue:
        message['content'] = translator_ins(message['content'], target_language)
    return dialogue


history_file = "historys.json"
if os.path.exists(history_file):
    with open(history_file, "r") as file:
        historys = json.load(file)
else:
    historys = []

def save_history():
    """Saves the current historys list to a file."""
    with open(history_file, "w") as file:
        json.dump(historys, file)



client = OpenAI()

System_prompt = maara.system_prompt(str(datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')))

def maara_ai_assistant(prompt):
    global historys       
    messages = [{"role": "system", "content": System_prompt},] + historys[-6:] + [{ "role": "user", "content": prompt },]

    while True:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            temperature=0,
            top_p=1,)
        response_text = response.choices[0].message.content
        action, action_input, thoughts, location = maara.extract_action_and_input(response_text)
        
        #Google search tool
        if action:
            if action[-1] == "Search":
                tool = maara.google_search
                if action_input:
                    observation = tool(action_input[-1])
                    messages.extend([
                        { "role": "system", "content": response_text },
                        { "role": "user", "content": f"Observation: {observation}" },
                    ])
        
        #Google search tool
            elif action[-1] == "Map":
                print("get_location_coordinates called")
                latitude, longitude = maara.get_location_coordinates(location)
                print("get_location_coordinates call sucessful")
                if latitude == None or longitude == None:
                  return "Unable to find the location. Would you please try entering the exact place?"
                if action_input:
                    print("search_place called")
                    observation = maara.search_place(action_input[-1], latitude, longitude)
                    print("search_place call successful")
                    messages.extend([
                        { "role": "system", "content": response_text },
                        { "role": "user", "content": f"Observation: {observation[0:5]}" },
                    ])

            elif action[-1] == "Response To Human":
                messages.extend([{ "role": "system", "content": action_input[-1] }])
                historys.extend([  # Change square brackets to parentheses
                    { "role": "assistant", "content": prompt },
                    { "role": "user", "content": action_input[-1] },
                ])
                save_history() 
                return action_input[-1]
                
        else:
            historys.extend([  # Change square brackets to parentheses
                { "role": "assistant", "content": prompt },
                { "role": "user", "content": response_text },
            ])
            save_history() 
            return response_text
        

def maara_ai_mulitlang_assistant(prompt, language):

    global historys       
    history = translate_dialogue(historys[-6:], "en")
    messages = [{"role": "system", "content": System_prompt},] + history + [{ "role": "user", "content": prompt },]

    while True:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            temperature=0,
            top_p=1,)
        response_text = response.choices[0].message.content
        action, action_input, thoughts, location = maara.extract_action_and_input(response_text)
        
        #Google search tool
        if action:
            if action[-1] == "Search":
                tool = maara.google_search
                if action_input:
                    observation = tool(action_input[-1])
                    messages.extend([
                        { "role": "system", "content": response_text },
                        { "role": "user", "content": f"Observation: {observation}" },
                    ])
        
        #Google search tool
            elif action[-1] == "Map":
                latitude, longitude = maara.get_location_coordinates(location)
                if action_input:
                    observation = maara.search_place(action_input[-1], latitude, longitude)
                    messages.extend([
                        { "role": "system", "content": response_text },
                        { "role": "user", "content": f"Observation: {observation[0:5]}" },
                    ])

            elif action[-1] == "Response To Human":
                response_text = translator_ins(action_input[-1], language)
                messages.extend([{ "role": "system", "content": response_text }])
                historys.extend([ 
                    { "role": "assistant", "content": prompt },
                    { "role": "user", "content": response_text },
                ])
                save_history() 
                return response_text
                
        else:
            response_text = translator_ins(response_text, language)
            historys.extend([ 
                { "role": "assistant", "content": prompt },
                { "role": "user", "content": response_text },
            ])
            save_history() 
            return response_text