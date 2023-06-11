import apiKey
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

import prompt_file

app = Flask(__name__)
CORS(app)


def get_context_str_for_character(character):
    prompt_mapping = {
        "Lord Vishnu": prompt_file.VISHNU_PROMPT,
        "Lord Shiva": prompt_file.SHIVA_PROMPT,
        "Lord Buddha": prompt_file.BUDDHA_PROMPT,
        "Ironman": prompt_file.IRONMAN_PROMPT,
        "Lord Brahma": prompt_file.BRAHMA_PROMPT,
        "Lord Rama": prompt_file.RAMA_PROMPT,
        "Lord Krishna": prompt_file.KRISHNA_PROMPT,
        "spiderman": prompt_file.SPIDERMAN_PROMPT,
        "Lord Hanuman": prompt_file.HANUMAN_PROMPT,
        "Lord Ganesha": prompt_file.GANESHA_PROMPT,
        "Goddess Durga": prompt_file.DURGA_PROMPT,
        "Goddess Kali": prompt_file.KALI_PROMPT,
        "Lord Arjuna": prompt_file.ARJUNA_PROMPT,
        "Goddess Draupadi": prompt_file.DRAUPADI_PROMPT,
        "Lord Bhima": prompt_file.BHIMA_PROMPT,
        "Lord Yudhishthira": prompt_file.YUDHISTHIR_PROMPT,
        "Lord Nakula": prompt_file.NAKULA_PROMPT,
        "Lord Sahadev": prompt_file.SHAHADEV_PROMPT,
        "Lord Indra": prompt_file.INDRA_PROMPT,
        "Lord Agni": prompt_file.AGNI_PROMPT,
        "Lord Surya": prompt_file.SURYA_PROMPT,
        "Lord Chandra": prompt_file.CHANDRA_PROMPT,
        "Lord Vayu": prompt_file.VAYU_PROMPT,
        "Lord Varuna": prompt_file.VARUNA_PROMPT,
        "thor": prompt_file.THOR_PROMPT,
        "Captain America": prompt_file.CAPTAIN_AMERICA_PROMPT,
        "Thanos": prompt_file.THANOS_PROMPT
    }

    return prompt_mapping.get(character, None)



CharacterUSer = ""


@app.route('/character', methods=['POST'])
def characterSet():
    print(request.form)
    data = request.json
    characterType = data['character']
    global CharacterUSer
    CharacterUSer = characterType
    print("Character template-------------------------\n" + CharacterUSer)
    return CharacterUSer


@app.route('/chat', methods=['POST'])
def bot():
    print(request.form)
    data = request.json
    charcter = CharacterUSer
    chat = data["chat"]
    prompt = prompt_file.DEFAULT_TEXT_QA_PROMPT_TMPL.format(
        context_str=get_context_str_for_character(character=charcter), human_input=chat)
    # print(prompt)
    openai.api_key = apiKey.OPENAI_AUTH_TOKEN
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=400,
        temperature=0.5)
    respons_in_english = response["choices"][0]["text"]

    print(respons_in_english)
    return jsonify(respons_in_english.strip())


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=80)
