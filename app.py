from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import random
import re

app = Flask(__name__)
CORS(app)

SONG_LIST = [
    "Bohemian Rhapsody - Queen", "Imagine - John Lennon", "Shape of You - Ed Sheeran",
    "Billie Jean - Michael Jackson", "Hey Jude - The Beatles", "Rolling in the Deep - Adele",
    "Smells Like Teen Spirit - Nirvana", "Someone Like You - Adele", "Let it Be - The Beatles",
    "Hotel California - Eagles", "Halo - Beyoncé", "Uptown Funk - Mark Ronson ft. Bruno Mars",
    "Shake It Off - Taylor Swift", "Wonderwall - Oasis", "Lose Yourself - Eminem",
    "Thinking Out Loud - Ed Sheeran", "Sweet Child O' Mine - Guns N' Roses", "Take On Me - A-ha",
    "Toxic - Britney Spears", "Blinding Lights - The Weeknd"
]

# Load TinyLlama model and tokenizer
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

@app.route("/generate", methods=["GET"])
def generate_lyric():
    song = random.choice(SONG_LIST)
    artist = song.split(" - ")[1]
    song_title = song.split(" - ")[0]
    
    # Revised prompt without negative examples list
    prompt = (
        f"Generate 2-4 authentic lines of lyrics from the song '{song_title}' by {artist}. "
        "Provide only the lyrics without any titles, explanations, or special formatting. "
        "Format as separate lines without numbers or bullet points.\n\n"
        "Example:\n"
        "Is this the real life?\n"
        "Is this just fantasy?\n"
        "Caught in a landslide\n"
        "No escape from reality"
    )
    
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3
        )

        # Extract and clean response
        full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the original prompt text
        lyrics = full_text.replace(prompt, "").strip()
        
        # Enhanced cleaning pipeline
        cleaned = []
        forbidden_phrases = ["song title", "artist name", "quotation marks", "explanations", 
                            "example:", "format:", "do not include", "lyrics from"]
        
        for line in lyrics.split('\n'):
            # Clean each line
            line = re.sub(r'^[\d\.\-\*"\']+\s*', '', line)  # Remove numbers, bullets, quotes
            line = re.sub(r'[\[\(\{].*?[\]\)\}]', '', line)  # Remove bracketed content
            line = line.strip()
            
            # Validate line content
            if line and len(line) > 5:  # Reduced minimum length
                line_lower = line.lower()
                if (not any(phrase in line_lower for phrase in forbidden_phrases) and
                    not any(word in line_lower for word in [song_title.lower(), artist.lower()]) and
                    not line_lower.startswith(('http', 'www'))):
                    cleaned.append(line)
        
        # Final validation and formatting
        valid_lines = []
        for line in cleaned[:4]:  # Take first 4 valid lines
            if 8 <= len(line) <= 80:  # Reasonable line length check
                valid_lines.append(line)
                
        if 2 <= len(valid_lines) <= 4:
            lyric_snippet = '\n'.join(valid_lines)
            return jsonify({"lyric": lyric_snippet, "song_title": song})
        else:
            return jsonify({"lyric": "Couldn't generate valid lyrics. Please try again!", "song_title": song})

    except Exception as e:
        return jsonify({"error": str(e)})



@app.route("/check", methods=["POST"])
def check_guess():
    data = request.get_json()
    user_guess = data.get("guess", "").strip().lower()
    correct_full_title = data.get("correct_title", "")  # Full title with artist
    
    # Extract just the song title portion
    correct_title = correct_full_title.split(" - ")[0].strip().lower()
    
    return jsonify({
        "result": "correct" if user_guess == correct_title else "incorrect",
        "correct_title": correct_full_title  # Return full title for display
    })
if __name__ == "__main__":
    app.run(debug=True)