""" handle message translation moderation and storage for audit """
import uuid
import simplejson as json
import requests
import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, jsonify, request

app = Flask(__name__)


DYNAMO = boto3.resource('dynamodb')
TABLE = DYNAMO.Table('message-hub')
HEADERS = {
    "apikey":os.environ['apikey']
}


lang={'af':'Afrikaans','sq':'Albanian','am':'Amharic','ar':'Arabic',
'az':'Azerbaijani','bn':'Bengali','bs':'Bosnian','bg':'Bulgarian',
'zh':'Chinese (Simplified)','zh-TW':'Chinese (Traditional)',
'hr':'Croatian','cs':'Czech','da':'Danish','fa-AF':'Dari',
'nl':'Dutch','en':'English','et':'Estonian','fi':'Finnish',
'fr':'French','fr-CA':'French (Canada)','ka':'Georgian',
'de':'German','el':'Greek','ha':'Hausa','he':'Hebrew',
'hi':'Hindi','hu':'Hungarian','id':'Indonesian',
'it':'Italian','ja':'Japanese','ko':'Korean','lv':'Latvian',
'ms':'Malay','no':'Norwegian','fa':'Persian','ps':'Pashto',
'pl':'Polish','pt':'Portuguese','ro':'Romanian','ru':'Russian',
'sr':'Serbian','sk':'Slovak','sl':'Slovenian','so':'Somali',
'es':'Spanish','es-MX':'Spanish (Mexico)','sw':'Swahili',
'sv':'Swedish','tl':'Tagalog','ta':'Tamil','th':'Thai',
'tr':'Turkish','uk':'Ukrainian','ur':'Urdu','vi':'Vietnamese'}


def hello(event, context):
    """"Pointless boilerplate"""
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


#Dynamo key: ID, language, original

#get https://api.cot-refinery.com/dev/message_hub/languages
@app.route(
    "/<string:workspace>/<string:function>/languages",
    methods=["GET"])
def language_list(workspace, function): # pylint: disable=R0913,C0301,W0613  # Many arguments for reusable code and some extras to make the routing work
    """ Return all languages """
    return jsonify(lang),200



#post
#https://api.cot-refinery.com/dev/message_hub/message
#conversation_id
#language
#message_text
#moderation?

@app.route(
    "/<string:workspace>/<string:function>/message",
    methods=["POST"])
def post_message(workspace, function): # pylint: disable=R0913,C0301,W0613  # Many arguments for reusable code and some extras to make the routing work
    """ Add new message """
    message_data=request.data
    message=dict()
    resp=dict()
    if message['lang'] in lang and \
        message['moderate'] in ['true','false']:
        message['id']=str(uuid.uuid4())
        message['conversation_id']=message_data['conversation_id']
        message['lang']=message_data['lang']
        message['message_text']=message_data['message_text']
        message['moderate']=message_data['moderate']
        TABLE.put_item(Item=message)
        resp['status']='OK'
        ret=200
    else:
        resp['status']='Invalid'
        ret=400
    return jsonify(resp),ret



#get
#https://api.cot-refinery.com/dev/message_hub/message/id/lang

@app.route(
    "/<string:workspace>/<string:function>/message/<string:m_id>/<string:req_lang>",
    methods=["GET"])
def get_message(workspace, function,m_id,req_lang): # pylint: disable=R0913,C0301,W0613  # Many arguments for reusable code and some extras to make the routing work
    """ Return all languages """
    trans_message=TABLE.query(KeyConditionExpression=Key('id').eq(m_id) & Key('lang').eq(req_lang))
    if not trans_message:
        trans_message=translate_message(id,req_lang)
        TABLE.put_item(Item=trans_message)
    if trans_message['moderate']:
        ret_text=trans_message['moderated_message']
    else:
        ret_text=trans_message['message_text']
    return jsonify(ret_text),200

def translate_message(m_id,req_lang):
    """Translation Stub"""
    new_message=TABLE.query(KeyConditionExpression=Key('id').eq(m_id) & Key('original').eq('true'))
    new_text=new_message['message_text']
    new_message['lang']=req_lang
    new_message['message_text']=new_text

    #post_data=dict()
    #post_data['text']=new_message['message_text']
    #url="amazon.com/translate"
    #new_text=requests.post(url, data=json.dumps(post_data), headers=HEADERS)
    return new_message


#post
#https://api.cot-refinery.com/dev/message_hub/moderate/id/lang
#moderated_text

@app.route(
    "/<string:workspace>/<string:function>/moderate/<string:m_id>/<string:req_lang>",
    methods=["POST"])
def moderate_message(workspace, function,m_id,req_lang): # pylint: disable=R0913,C0301,W0613  # Many arguments for reusable code and some extras to make the routing work
    """ Add new message """
    message_data=request.data
    message=TABLE.query(KeyConditionExpression=Key('id').eq(m_id) & Key('lang').eq(req_lang))
    if message:
        message['moderated_text']=message_data['moderated_text']
        TABLE.put_item(Item=message)

"""
post
https://api.cot-refinery.com/dev/message_hub/conversation_create
participants
subject
private?
moderate all messages?
"""

"""
post
https://api.cot-refinery.com/dev/message_hub/conversation_list
keywords
"""


"""
https://api.cot-refinery.com/prod/data_receiver/skippygram/photo_entries
@app.route(
    "/<string:workspace>/<string:function>/<string:schema>/<string:table>",
    methods=["GET"])
"""
