from langchain import OpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import prompt_file, os
from langchain import PromptTemplate, LLMChain
from flask import Flask, request, jsonify
from flask_cors import CORS

from remove_prefix_middleware import RemovePrefixMiddleware

app = Flask(__name__)
app.wsgi_app = RemovePrefixMiddleware(app.wsgi_app)
CORS(app)


def get_context_str_for_character(character):
    if character == "Lord Vishnu":
        return prompt_file.VISHNU_PROMT
    elif character == "Lord Shiva":
        return prompt_file.SHIVA_PROMPT
    elif character == "Lord Buddha":
        return prompt_file.BUDDHA_PROMT
    elif character == "Ironman":
        return prompt_file.IRONMAN_PROMT
    elif character == "Lord Brahma":
        return prompt_file.BRHAMA_PROMT
    elif character == "Lord Rama":
        return prompt_file.RAMA_PROMT
    elif character == "Lord Krishna":
        return prompt_file.KRISHNA_PROMT
    elif character == "spiderman":
        return prompt_file.SPIDERMAN_PROMT
    elif character == "Lord Hanuman":
        return prompt_file.HANUMAN_PROMT
    elif character == "Lord Ganesha":
        return prompt_file.GANESHA_PROMT
    elif character == "Goddess Durga":
        return prompt_file.DURGA_PROMT
    elif character == "Goddess Kali":
        return prompt_file.KALI_PROMT
    elif character == "Lord Arjuna":
        return prompt_file.ARJUNA_PROMT
    elif character == "Goddess Draupadi":
        return prompt_file.DRAUPADI_PROMT
    elif character == "Lord Bhima":
        return prompt_file.BHIMA_PROMT
    elif character == "Lord Yudhishthira":
        return prompt_file.YUDHISTHIR_PROMT
    elif character == "Lord Nakula":
        return prompt_file.NAKULA_PROMT
    elif character == "Lord Sahadev":
        return prompt_file.SHAHADEV_PROMT
    elif character == "Lord Indra":
        return prompt_file.INDRA_PROMPT
    elif character == "Lord Agni":
        return prompt_file.AGNI_PROMPT
    elif character == "Lord Surya":
        return prompt_file.SURYA_PROMPT
    elif character == "Lord Chandra":
        return prompt_file.CHANDRA_PROMT
    elif character == "Lord Vayu":
        return prompt_file.VAYU_PROMPT
    elif character == "Lord Varuna":
        return prompt_file.VARUNA_PROMT
    elif character == "thor":
        return prompt_file.THANOS_PROMT
    elif character == "Captain America":
        return prompt_file.CAPTAIN_AMERICA_PROMT
    elif character == "Thanos":
        return prompt_file.THANOS_PROMT


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

    memoryUser = ConversationBufferWindowMemory(ai_prefix=characterType, memory_key="chat_history", k=3)
    global conversationWithSummary
    conversationWithSummary = LLMChain(
        llm=llmUser,
        # We set a low k=3, to only keep the last 3 interactions in memory
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
    return jsonify(response.strip())


@app.route('/health', methods=['GET'])
def health():
    return "OK"


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=80)
