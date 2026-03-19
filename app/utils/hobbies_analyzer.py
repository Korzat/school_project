import json
import re
from pathlib import Path

def sanitize_input(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s\-]', '', text)
    return text

def analyze_hobbies(user_input: str) -> str:
    sanitized_input = sanitize_input(user_input)

    json_path = Path(__file__).parent.parent / "data" / "hobbies_professions.json"

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            professions_data = json.load(f)
    except Exception as e:
        print(f"Error loading hobbies data: {e}")
        return None

    profession_scores = {profession: 0 for profession in professions_data.keys()}

    for profession, data in professions_data.items():
        keywords = data.get("keywords", [])
        for keyword in keywords:
            if keyword in sanitized_input:
                profession_scores[profession] += 1

    max_score = max(profession_scores.values())

    if max_score == 0:
        return None

    best_professions = [prof for prof, score in profession_scores.items() if score == max_score]

    if len(best_professions) == 1:
        return best_professions[0]

    return best_professions[0]
