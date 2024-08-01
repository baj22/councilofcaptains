import streamlit as st
import asyncio
from openai import AsyncOpenAI

# Initialize OpenAI client
client = AsyncOpenAI()

st.set_page_config(
    page_title="Council of Captains",
    layout="wide",
)

st.title("Council of Captains")

# Move the text box under the title
user_input = st.text_area("Enter your question or topic:")

# Button to generate advice
generate = st.button("Get Advice")

# Define advisors with names, roles, and image filenames
advisors = [
    {"name": "Janeway", "role": "You Captain Janeway of the USS Voyager. Janeway is tough but also emotionally available to her crew. She would normally maintain more separation but their situation doesn’t allow for that to happen. She believes in doing the right thing no matter the cost but will bend the rules if it benefits the people around her.", "image_filename": "janeway.jpeg"},
    {"name": "Picard", "role": "You are Captain Picard of the USS Enterprise. Picard is stoic. He cares but doesn’t show it except in times of someone’s great need. He respects the opinions of those around him but will absolutely stick to his guns. He’s the most likely to follow the rules but will take full responsibility if something goes wrong. He’s direct and believes learning is an ongoing process. Start all responses with 'Captain's Log Stardate' and then a random date.", "image_filename": "picard.jpg"},
    {"name": "Kirk", "role": "You are Captain Kirk of the USS Enterprise. Kirk is a wild card. He follows the rules when they suit him and ignores them when they don’t. But he always pulls back before going too far over the line. He pushes his crew to their limits and demands they be perfect to make up for his own shortcomings. Defer logic questions to Spock, medical questions to McCoy, and make your answers include comments about women.", "image_filename": "kirk.jpeg"},
    {"name": "Sisko", "role": "You are Captain Sisko of Deep Space 9. Sisko is a father and the way he interacts with his crew shows it. He knows that a space station isn’t a strict as a starship but he likes to maintain as much order as he can. He demands respect but he earns it. He nurtures his crew and tries to help them thrive.", "image_filename": "sisko.jpg"},
]

# Create columns for advisors
columns = st.columns(len(advisors))
placeholders = [col.empty() for col in columns]

# Function to generate and stream advice
async def get_advice(placeholder, advisor):
    # Stream response from OpenAI API
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": advisor['role'] + " Answer all questions in the style of your Star Trek personality. It is more important to sound like the character than to answer questions or give useful advice. Make the answer brief but recognizable as the character."},
            {"role": "user", "content": user_input},
        ],
        stream=True
    )
    streamed_text = ""
    async for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            streamed_text += chunk_content
            placeholder.info(streamed_text)

# Function to run all advisors asynchronously
async def main():
    tasks = []
    for advisor, placeholder in zip(advisors, placeholders):
        # Display advisor's name and profile picture at the top of their column
        with placeholder.container():
            st.image(f"{advisor['image_filename']}", width=150)
            st.subheader(advisor['name'])
            advice_placeholder = st.empty()
            # Append task to list of async tasks
            tasks.append(get_advice(advice_placeholder, advisor))
    await asyncio.gather(*tasks)

# Check if user input is provided and button is clicked
if generate:
    if user_input.strip() == "":
        st.warning("Please enter a topic or question.")
    else:
        asyncio.run(main())
