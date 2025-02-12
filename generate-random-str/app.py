from flask import Flask, render_template, jsonify
import openai
import os
import random
import string
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
#load_dotenv()
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
    "T-Rex", "NASA", "Greek Mythology", "Volcanoes",
    "Quantum Physics", "Rainforests", "Solar Flares", "Pirates",
    "Samurai", "Penguins", "Auroras", "Lightning",
    "Jellyfish", "The Great Wall of China", "Coral Reefs", "Chess",
    "Music Genres", "Ancient Egypt", "Supernovae", "Glaciers",
    "Medieval Castles", "The Milky Way", "Cave Paintings",
    "Ancient Greece", "Mountains", "Wolves", "The Human Brain",
    "Exoplanets", "Space Telescopes", "Robots", "Fungi",
    "Bees", "Kangaroos", "The Pyramids", "Tsunamis",
    "Meteors", "The Mariana Trench", "Comets", "Crystals",
    "Ancient Mesopotamia", "Venus Flytraps", "Lava Lakes",
    "The Roman Colosseum", "Rainbows", "The Speed of Light",
    "Fireworks", "Origami", "Electric Eels", "Planets",
    "Submarines", "Hummingbirds", "The Arctic Circle",
    "Wormholes", "Microbes", "Ancient Maps", "The Solar System",
    "Volcanic Islands", "Ancient China", "Icebergs", "The Jungle",
    "Geysers", "Space Stations", "Tropical Fish",
    "The Great Barrier Reef", "Caves", "Mythical Creatures",
    "Sandstorms", "Lightning Rods", "Satellites"
]

FACT_PLACES = [
    "Earth", "Mars", "The Ocean", "The Amazon Rainforest",
    "The Sahara Desert", "Antarctica", "The Deep Sea",
    "Mount Everest", "The International Space Station",
    "The Moon", "A Hidden Cave", "An Old Library",
    "An Ancient Ruin", "Venus", "Jupiter", "Saturn's Rings",
    "A Viking Ship", "The Great Pyramid of Giza", "The Arctic",
    "A Coral Reef", "An Active Volcano", "A Desert Oasis",
    "The Grand Canyon", "The Great Wall of China", "Stonehenge",
    "A Glacier", "An Ancient Castle", "The Mariana Trench",
    "A Hidden Waterfall", "The Galapagos Islands",
    "A Space Telescope", "An Old Lighthouse", "A Secret Laboratory",
    "The Bermuda Triangle", "A Meteor Crater", "A Fossil Dig Site",
    "The North Pole", "A Dense Forest", "A Volcanic Island",
    "A Space Station", "A Futuristic City", "A Shipwreck",
    "An Underwater City", "The Surface of the Sun",
    "A Hidden Valley", "A Jungle Temple", "An Enchanted Forest",
    "A Floating Iceberg", "The Bottom of the Ocean",
    "A Windy Desert", "A Star Observatory", "A Space Shuttle",
    "A Lost City", "A Frozen Lake", "A Mountain Range",
    "A Tropical Island", "A Cave System", "A Snowy Tundra",
    "A Hot Spring", "An Ancient Tomb", "A Rainforest Canopy",
    "An Alien Planet", "A Giant Redwood Forest", "A Lava Lake",
    "An Icy Moon", "A Distant Galaxy", "A Futuristic Spaceport",
    "A Flying Island", "A Hidden Geyser", "A Historical Battlefield",
    "A Cloud Forest"
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
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are an expert in fun, surprising, and little-known facts. Your job is to retrieve **real** fun facts based on given criteria."},
                {"role": "user", "content": f"Give me a **concise** (maximum 2-3 sentences, up to 40 words) fun fact about {fact_card['Fact Subject']} in {fact_card['Fact Place']} related to {fact_card['Fact Category']}. Make it **fascinating, funny, and easy to read**. Do NOT make up new facts, only return well-known fun facts from history, science, or pop culture."}
            ],
            max_tokens=80, 
            temperature=0.8,  
        )
        # Extract the response
        fun_fact = response["choices"][0]["message"]["content"].strip()
        return fun_fact
    except Exception as e:
        return f"Error generating fun fact: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

from flask import request

@app.route("/generate-fact")
def generate_fun_fact():
    # Get the category from the query parameter
    selected_category = request.args.get("category")
    
    # Generate a fact card, optionally filtering by category
    if selected_category and selected_category in FACT_CATEGORIES:
        fact_card = {
            "Fact Category": selected_category,
            "Fact Subject": random.choice(FACT_SUBJECTS),
            "Fact Place": random.choice(FACT_PLACES),
        }
    else:
        # Generate a fully random fact card if no category is selected
        fact_card = generate_random_fact_card()
    
    # Generate a fun fact using OpenAI
    fun_fact = get_fun_fact_from_openai(fact_card)
    
    return jsonify({"fun_fact": fun_fact})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
