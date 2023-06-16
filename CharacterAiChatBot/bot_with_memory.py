from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain import OpenAI
from langchain import PromptTemplate, LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from googleanalytics import Analytics

import prompt_file
from remove_prefix_middleware import RemovePrefixMiddleware

app = Flask(__name__)
app.wsgi_app = RemovePrefixMiddleware(app.wsgi_app)
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
templateUser = ""
llmUser = ""
promptUser = ""
memoryUser = ""
conversationWithSummary = ""


@app.route('/character', methods=['POST'])
def characterSet():
    print(request.form)
    data = request.json
    characterType = data['character']
    templateSet = prompt_file.DEFAULT_TEXT_QA_PROMPT_TMPL.format(
        context_str=get_context_str_for_character(character=characterType), human_input="")
    global CharacterUSer
    global templateUser
    global promptUser
    global memoryUser
    CharacterUSer = templateSet
    print("Character template-------------------------\n" + CharacterUSer)
    templateUser = CharacterUSer + """
    {chat_history}
    Human: {human_input}""" + characterType + """:"""
    promptUser = PromptTemplate(
        input_variables=["chat_history", "human_input"],
        template=templateUser
    )
    global llmUser
    llmUser = OpenAI(temperature=0.5)
    # os.environ["OPENAI_API_KEY"] = "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"

    # We set a low k=3, to only keep the last 3 interactions in memory
    memoryUser = ConversationBufferWindowMemory(ai_prefix=characterType, memory_key="chat_history", k=3)
    global conversationWithSummary
    conversationWithSummary = LLMChain(
        llm=llmUser,
        prompt=promptUser,
        memory=memoryUser,
        verbose=True,
    )
    return CharacterUSer


@app.route('/chat', methods=['POST'])
def bot():
    print(request.form)
    data = request.json
    chat = data["chat"]
    response = conversationWithSummary.predict(human_input=chat)
    print(response)
    analytics.event('Chatbot Interaction', CharacterUSer, chat)
    return jsonify(response.strip())


@app.route('/health', methods=['GET'])
def health():
    return "OK"


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=80)