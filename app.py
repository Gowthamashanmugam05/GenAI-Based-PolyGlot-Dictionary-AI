from flask import Flask, render_template, request, jsonify
import nltk
from nltk.corpus import wordnet as wn
from googletrans import Translator

# Download required datasets
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__, template_folder='home')

# Supported languages (Indian)
languages = {
    "hindi": "hi",
    "tamil": "ta",
    "telugu": "te",
    "marathi": "mr",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "punjabi": "pa",
    "bengali": "bn",
    "odia": "or",
    "english": "en",
}

labels = {
    "word_details": "Word Details",
    "translated_word": "Translated Word",
    "synonyms": "Synonyms",
    "antonyms": "Antonyms",
    "examples": "Example Sentences",
    "definitions": "Definitions",
    "no_synonyms": "No synonyms found.",
    "no_antonyms": "No antonyms found.",
    "no_examples": "No example sentences found.",
    "no_definitions": "No definitions found."
}

def generate_word_details(word, language_code, translated_labels):
    translator = Translator()
    try:
        # Direct translation of the main word
        translated_word = translator.translate(word, dest=language_code).text
        
        # Fetch WordNet data only for English and later translate results
        if language_code != 'en':
            synonyms = {lemma.name() for synset in wn.synsets(word, lang='eng') for lemma in synset.lemmas('eng')}
        else:
            synonyms = {lemma.name() for synset in wn.synsets(word) for lemma in synset.lemmas()}
            
        translated_synonyms = [translator.translate(synonym, dest=language_code).text for synonym in synonyms] or [translated_labels['no_synonyms']]

        antonyms = {ant.name() for synset in wn.synsets(word) for lemma in synset.lemmas() for ant in lemma.antonyms()}
        translated_antonyms = [translator.translate(antonym, dest=language_code).text for antonym in antonyms] or [translated_labels['no_antonyms']]

        examples = {example for synset in wn.synsets(word) for example in synset.examples()}
        translated_examples = [translator.translate(example, dest=language_code).text for example in examples] or [translated_labels['no_examples']]

        definitions = {synset.definition() for synset in wn.synsets(word)}
        translated_definitions = [translator.translate(definition, dest=language_code).text for definition in definitions] or [translated_labels['no_definitions']]

        return {
            "translated_word": translated_word,
            "synonyms": translated_synonyms,
            "antonyms": translated_antonyms,
            "examples": translated_examples,
            "definitions": translated_definitions,
        }
    except Exception as e:
        return {"error": f"Processing error {str(e)}"}



def translate_labels(labels, language_code):
    translator = Translator()
    try:
        return {key: translator.translate(value, dest=language_code).text for key, value in labels.items()}
    except Exception as e:
        return {key: value for key, value in labels.items()}  # Fallback to English if translation fails






# Modify this route to handle AJAX requests
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()  # Get JSON data sent via AJAX
    word = data.get('word')
    language = data.get('language').lower()

    if not word or not language:
        return jsonify({"error": "Please provide both the word and target language."})

    if language not in languages:
        return jsonify({"error": f"Sorry, the language '{language}' is not supported."})

    try:
        translated_labels = translate_labels(labels, languages[language])
        result = generate_word_details(word, languages[language], translated_labels)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def home():
    return render_template('login.html', languages=languages.keys())


@app.route('/index')
def index():
    return render_template('index.html', languages=languages.keys())




if __name__ == "__main__":
    app.run(debug=True)
