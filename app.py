import streamlit as st
from maara_ai import *

doc_path = 'icons/docter.png'
user_path = 'icons/user-icon.png'
github_icon_path = 'icons/git.png'
linkedin_icon_path = 'icons/linkedin.png'

doc_base64 = maara.get_image_as_base64(doc_path)
user_base64 = maara.get_image_as_base64(user_path)
github_base64 = maara.get_image_as_base64(github_icon_path)
linkedin_base64 = maara.get_image_as_base64(linkedin_icon_path)

languages = {
    'English': 'en',
    'Tamil': 'ta',
    'Malayalam': 'ml',
    'Kannada': 'kn',
    'Telugu': 'te'
}

def user_message(message):
    st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="margin-right: 10px;">
                <img src="data:image/png;base64,{user_base64}" width="34" height="34" />
            </div>
            <div style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 10px; font-size:18px;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

def bot_message(message):
    st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="margin-right: 10px;">
                <img src="data:image/png;base64,{doc_base64}" width="34" height="34" />
            </div>
            <div style="background-color: #2196F3; color: white; padding: 10px; border-radius: 10px; font-size:18px;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)


def main(i):
    st.sidebar.title("Preferred language")
    

    if "last_language" not in st.session_state:
        st.session_state.last_language = 'en'  
    
    selected_language_name = st.sidebar.selectbox('Choose your language:', list(languages.keys()), index=0)
    selected_language_code = languages[selected_language_name]

    if selected_language_code != st.session_state.last_language:
        st.session_state.chat_history = []
        st.session_state.last_language = selected_language_code  


        history_file = "historys.json"
        if os.path.exists(history_file):
            os.remove(history_file)
            st.info('Chat history has been cleared due to language change.')

    st.title("Maara AI Doctor👨🏻‍⚕️")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Prompt here")
    if user_input:
        for message, is_bot_response in st.session_state.chat_history:
            if is_bot_response:
                bot_message(message)
            else:
                user_message(message)

        st.session_state.chat_history.append((user_input, False))
        user_message(user_input)

        if selected_language_code == 'en':
            bot_response = maara_ai_assistant(user_input)
        else:
            bot_response = maara_ai_mulitlang_assistant(user_input, selected_language_code)

        bot_message(bot_response)
        st.session_state.chat_history.append((bot_response, True))

if __name__ == "__main__":
    main(0)