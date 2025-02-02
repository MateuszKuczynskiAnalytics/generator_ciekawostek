from flask import Flask, render_template, jsonify
import openai
import os
import random
import string
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Categories for fun facts
FACT_CATEGORIES = [
    "Science", "History", "Animals", "Technology", "Space",
    "Geography", "Human Body", "Psychology", "Food", "Sports",
    "Inventions", "Music", "Movies", "Art", "Culture"
]

FACT_SUBJECTS = [
    "Octopuses", "Black holes", "Ancient Rome", "Sharks",
    "AI", "The Moon", "The Eiffel Tower", "Dinosaurs",
    "The Internet", "Neuroscience", "Bananas", "Time Travel",
    "T-Rex", "NASA", "Greek Mythology", "Volcanoes"
]

FACT_PLACES = [
    "Earth", "Mars", "The Ocean", "The Amazon Rainforest",
    "The Sahara Desert", "Antarctica", "The Deep Sea",
    "Mount Everest", "The International Space Station",
    "The Moon", "A Hidden Cave", "An Old Library",
    "An Ancient Ruin"
]

def generate_random_fact_card():
    """Generate a randomized fun fact structure (category, subject, place)."""
    fact_category = random.choice(FACT_CATEGORIES)
    fact_subject = random.choice(FACT_SUBJECTS)
    fact_place = random.choice(FACT_PLACES)

    return {
        "Fact Category": fact_category,
        "Fact Subject": fact_subject,
        "Fact Place": fact_place
    }

def get_fun_fact_from_openai(fact_card):
    """Generate a fun fact based on the structured fact card using OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  
            messages=[
                {"role": "system", "content": "You are an expert in fun, surprising, and little-known facts. Your job is to retrieve **real** fun facts based on given criteria."},
                {"role": "user", "content": f"Give me a **concise** (maximum 2-3 sentences, up to 40 words) fun fact about {fact_card['Fact Subject']} in {fact_card['Fact Place']} related to {fact_card['Fact Category']}. Make it **fascinating, funny, and easy to read**. Do NOT make up new facts, only return well-known fun facts from history, science, or pop culture."}
            ],
            max_tokens=80,  # Hard limit on response length
            temperature=0.8,  # Increased randomness for more unique responses
        )
        # Extract the response
        fun_fact = response["choices"][0]["message"]["content"].strip()
        return fun_fact
    except Exception as e:
        return f"Error generating fun fact: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-fact")
def generate_fun_fact():
    fact_card = generate_random_fact_card()
    fun_fact = get_fun_fact_from_openai(fact_card)
    
    return jsonify({"fun_fact": fun_fact})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
