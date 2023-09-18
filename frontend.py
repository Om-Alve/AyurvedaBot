import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow import keras
from streamlit_chat import message as st_message

dosha_descriptions = [
    "You have Vata dosha:\n"
    "Vata is characterized by qualities of lightness, dryness, and mobility. "
    "People with dominant Vata dosha tend to be creative, quick-thinking, and energetic. "
    "They may have a slender build, dry skin, and are prone to anxiety and digestive issues. "
    "Balancing Vata involves warmth, grounding, and routine.",

    "You have Pitta dosha:\n"
    "Pitta is characterized by qualities of heat, sharpness, and intensity. "
    "Individuals with dominant Pitta dosha are often intelligent, focused, and assertive. "
    "They tend to have a medium build, fair skin, and a strong metabolism. "
    "Balancing Pitta involves cooling, calming, and avoiding excessive heat.",

    "You have Kapha dosha:\n"
    "Kapha is characterized by qualities of heaviness, stability, and moisture. "
    "People with dominant Kapha dosha are typically calm, compassionate, and strong. "
    "They often have a sturdy build, smooth skin, and can gain weight easily. "
    "Balancing Kapha involves stimulation, warmth, and regular exercise.",

    "You have Vata and Pitta dosha:\n"
    "Having both Vata and Pitta doshas means you may have a combination of their characteristics. "
    "It's important to balance both aspects, considering qualities of both doshas in your lifestyle and diet choices.",

    "You have Vata and Kapha dosha:\n"
    "Having both Vata and Kapha doshas means you may experience a mix of their qualities. "
    "Balancing this combination may require adjustments in both your physical activity and diet.",

    "You have Pitta and Kapha dosha:\n"
    "Having both Pitta and Kapha doshas means you may exhibit traits from both categories. "
    "To maintain balance, you'll need to address qualities of both doshas in your daily routine and nutrition."
]


mcq_questions = [
    {
        "question": "Question 1: Body Size",
        "options": ["Slim", "Medium", "Large"]
    },
    {
        "question": "Question 2: Body Weight",
        "options": ["Low, difficulties in gaining weight", "Moderate, no difficulties in gaining or losing weight", "Heavy, difficulties in losing weight"]
    },
    {
        "question": "Question 3: Height",
        "options": ["Short", "Average", "Tall"]
    },
    {
        "question": "Question 4: Bone Structure",
        "options": ["Light, small bones, prominent joints", "Medium bone structure", "Large, broad shoulders, heavy bone structure"]
    },
    {
        "question": "Question 5: Complexion",
        "options": ["Dark complexion, tans easily", "Fair skin, sunburns easily", "White, pale, tans evenly"]
    },
    {
        "question": "Question 6: General Feel of Skin",
        "options": ["Thin and dry, cool to touch, rough", "Smooth and warm, oily T-zone", "Thick and moist/greasy, cold"]
    },
    {
        "question": "Question 7: Texture of Skin",
        "options": ["Dry, pigmentation and aging", "Freckles, many moles, redness, rashes, and acne", "Options for question 7"]
    },
    {
        "question": "Question 8: Hair Colour",
        "options": ["Dull, black, brown", "Red, light brown, yellow", "Brown"]
    },
    {
        "question": "Question 9: Appearance of Hair",
        "options": ["Dry, black, knotted, brittle", "Straight, oily", "Thick, curly"]
    },
    {
        "question": "Question 10: Shape of Face",
        "options": ["Long, angular, thin", "Heart-shaped, pointed chin", "Large, round, full"]
    },
    {
        "question": "Question 11: Eyes",
        "options": ["Small, active, darting, dark eyes", "Medium-sized, penetrating, light-sensitive eyes", "Big, round, beautiful, glowing eyes"]
    },
    {
        "question": "Question 12: Eyelashes",
        "options": ["Scanty eyelashes", "Moderate eyelashes", "Thick/Fused eyelashes"]
    },
    {
        "question": "Question 13: Blinking of Eyes",
        "options": ["Excessive Blinking", "Moderate Blinking", "More or less stable"]
    },
    {
        "question": "Question 14: Cheeks",
        "options": ["Wrinkled, Sunken", "Smooth, Flat", "Rounded, Plump"]
    },
    {
        "question": "Question 15: Nose",
        "options": ["Crooked, Narrow", "Pointed, Average", "Rounded, Large open nostrils"]
    },
    {
        "question": "Question 16: Teeth and Gums",
        "options": ["Irregular, Protruding teeth, Receding gums", "Medium-sized teeth, Reddish gums", "Big, White, Strong teeth, Healthy gums"]
    },
    {
        "question": "Question 17: Lips",
        "options": ["Tight, thin, dry lips which chaps easily", "Lips are soft, medium-sized", "Lips are large, soft, pink, and full"]
    },
    {
        "question": "Question 18: Nails",
        "options": ["Dry, Rough, Brittle, Break", "Sharp, Flexible, Pink, Lustrous", "Thick, Oily, Smooth, Polished"]
    },
    {
        "question": "Question 19: Appetite",
        "options": ["Irregular, Scanty", "Strong, Unbearable", "Slow but steady"]
    },
    {
        "question": "Question 20: Liking Tastes",
        "options": ["Sweet / Sour / Salty", "Sweet / Bitter / Astringent", "Pungent / Bitter / Astringent"]
    },
]

page_refreshed = st.experimental_get_query_params().get('refresh')
    
if page_refreshed:
    # Reset session state and clear query parameters
    st.experimental_rerun()

st.session_state.features = []

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.history.append({"message": "Hello there!", "is_user": False})

if "count" not in st.session_state:
    st.session_state.count = 0

if "selected_options" not in st.session_state:
    st.session_state.selected_options = []
if "features" not in st.session_state:
    st.session_state.features = []

def generate_answer():
    if st.session_state.count >= len(mcq_questions):
        st.session_state.history.append({"message": st.session_state.user_input, "is_user": True})
        st.session_state.history.append({"message": "Thank you for answering all the questions", "is_user": False})
    else:
        st.session_state.history.append({"message": st.session_state.user_input, "is_user": True})
        
        question = mcq_questions[st.session_state.count]["question"]
        options = mcq_questions[st.session_state.count]["options"]
        question_and_options = f"{question}\n\nOptions:\n" + "\n".join([f"{i}. {option}" for i, option in enumerate(options, start=1)])
        st.session_state.history.append({"message": question_and_options, "is_user": False})
        
        try:
            user_input = int(st.session_state.user_input)
        except ValueError:
            user_input = None
            
        
        # Check if the input is a valid integer option and within the range of available options
        if user_input is not None and 1 <= user_input <= len(options):
            st.session_state.selected_options.append(user_input)
        
        st.session_state.count += 1
def predict_dosha():
    st.session_state.features = np.array(st.session_state.features).reshape(1, 20)
    model = keras.models.load_model('model')
    pred = np.argmax(model.predict(st.session_state.features))
    st.session_state.history.append({"message": dosha_descriptions[pred], "is_user": False})

user_input = st.text_input("Talk to the bot", key="user_input")

if st.button("Submit"):
    generate_answer()


for i in range(2,len(st.session_state.history)):
    m = st.session_state.history[i]["message"]
    if m.isdigit() and 1 <= int(m) <= 3:
        st.session_state.features.append(int(m) - 1)
    elif st.session_state.history[i]["is_user"]==True:
        print(mcq_questions[i-3]['options'])
        st.session_state.features.append(mcq_questions[i-3]['options'].index(m))
    
    
print(st.session_state.features)

if len(st.session_state.features) == 20:
    predict_dosha()
    
for i, chat in enumerate(reversed(st.session_state.history)):
    st_message(**chat, key=str(i))


