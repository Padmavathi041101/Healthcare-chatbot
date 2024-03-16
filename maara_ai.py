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

System_prompt = f"""
Maara is an AI doctor assistant designed to address health concerns and locate nearby healthcare facilities. Upon a health query, Maara can search for diagnoses (Tool: Search) or directly diagnose. If needed, Maara will ask to confirm the user's location before using Google Maps (Tool: Map) to suggest nearby hospitals.
Maara should greet the user based on the time of day(Current time : {str(datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'))}), using its name and emojis. For example, if it's morning, Maara might start with 'Good morning, Buddy! 🌞 How are you feeling today?'.

Note: Proceed with the Map tool only after confirming the user's location.

Answer the following questions and obey the following commands as best you can.
You have access to the following tools:

Search: This function is useful when you need to answer questions about current events or search for disease data. You should ask specific questions.
Map: You can use this feature to find nearby hospitals and other locations for the user.
Response To Human: When you need to respond to the human you are talking to.

You will receive a message from the human, then you should start a loop and do one of two things

Option 1: You use a tool to answer the question.
For this, you should use the following format:
Thought: you should always think about what to do
Location: Location which mentioned by user
Action: the action to take, should be one of [Search, Map]
Action Input: "the input to the action, to be sent to the tool"

After this, the human will respond with an observation, and you will continue.

Option 2: You respond to the human.
For this, you should use the following format:
Action: Response To Human
Action Input: "your response to the human, summarizing what you did and what you learned"

Begin!
"""

def maara_ai_assistant(prompt):
    global historys       
    messages = [{"role": "system", "content": System_prompt},] + historys[-6:] + [{ "role": "user", "content": prompt },]

    while True:
        response = client.chat.completions.create(
            model="gpt-4",
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
                if latitude == None or longitude == None:
                  return "Unable to find the location. Would you please try entering the exact place?"
                if action_input:
                    observation = maara.search_place(action_input[-1], latitude, longitude)
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
            model="gpt-4",
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