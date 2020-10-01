""" handle message translation moderation and storage for audit """
import time
import uuid
import ast
import decimal
#import requests
import operator
import simplejson as json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, jsonify, request

app = Flask(__name__)

TRANSLATE=boto3.client(service_name='translate', region_name='us-east-2')
DYNAMO = boto3.resource('dynamodb')
TABLE = DYNAMO.Table('message-hub')


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


#Dynamo key: ID

#get https://api.cot-refinery.com/dev/message_hub/languages
@app.route(
    "/<string:workspace>/<string:function>/languages",
    methods=["GET"])
def language_list(workspace, function): # pylint: disable=R0913,C0301,W0613 
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
    message_bytes=request.data
    message_str = message_bytes.decode("UTF-8")
    print(message_str)
    message_data = ast.literal_eval(message_str)

    message=dict()
    message['translations']=dict()
    resp=dict()
    if message_data['lang'] in lang and \
        message_data['moderate'] in ['true','false']:
        message['id']=str(uuid.uuid4())
        message['create_dttm']=decimal.Decimal(time.time())
        message['conversation_id']=message_data['conversation_id']
        message['original_lang']=message_data['lang']
        message['translations'][message_data['lang']]=message_data['message_text']
        message['moderate']=message_data['moderate']
        if message_data.get('moderate') == 'true':
            message['mod_status']='needs_review'
        TABLE.put_item(Item=message)
        resp['id']=message['id']
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
def get_message(workspace, function,m_id,req_lang): # pylint: disable=R0913,C0301,W0613  
    """ Return message, all languages """
    trans_message=TABLE.query(KeyConditionExpression=Key('id').eq(m_id))['Items'][0]
    if not trans_message['translations'].get(req_lang):
        trans_message=translate_message(trans_message,req_lang)
        TABLE.put_item(Item=trans_message)
    if trans_message['moderate']=="true":
        if str(trans_message.get('mod_status')).startswith('approved'):
            ret_text=trans_message['translations'].get(req_lang,'Unavailable')
        else:
            if str(trans_message.get('mod_status')).startswith('needs'):
                ret_text='Moderation Required'
            else:
                ret_text="Message Rejected"
    else:
        ret_text=trans_message['translations'].get(req_lang)
    return jsonify(ret_text),200

def translate_message(message,req_lang):
    """Translation Stub"""
    result=TRANSLATE.translate_text(Text=message['translations'][message['original_lang']],
        SourceLanguageCode=message['original_lang'],
        TargetLanguageCode=req_lang)
    new_text=result.get('TranslatedText')
    message['translations'][req_lang]=new_text

    return message

#get
#https://dev.api.cot-refinery.com/dev/message_hub/moderate_list/lang

@app.route(
    "/<string:workspace>/<string:function>/moderate_list/<string:req_lang>",
    methods=["GET"])
def get_moderation(workspace, function,req_lang): # pylint: disable=R0913,C0301,W0613  # Many arguments for reusable code and some extras to make the routing work
    """ Return all languages """
    mod_message=TABLE.scan(
            FilterExpression=Attr('moderate').eq('true')
            & Attr('original_lang').eq(req_lang)
            & Attr('mod_status').begins_with('needs'))['Items']
    return jsonify(mod_message),200

# needs, approved, completed, approved_by_human, approved_by_automation)
# auto_ok, human_ok, needs_human, auto_rejected, human_rejected.

#post
#https://api.cot-refinery.com/dev/message_hub/moderate/id/lang
#moderated_text

#@app.route(
#    "/<string:workspace>/<string:function>/moderate/<string:m_id>/<string:req_lang>",
#    methods=["POST"])
#def moderate_message(workspace, function,m_id,req_lang): # pylint: disable=R0913,C0301,W0613  # Many arguments for reusable code and some extras to make the routing work
#    """ Add new message """
#    message_data=request.data
#    message=TABLE.query(KeyConditionExpression=Key('id').eq(m_id) & Key('lang').eq(req_lang))
#    if message:
#        message['moderated_text']=message_data['moderated_text']
#        TABLE.put_item(Item=message)

@app.route(
    "/<string:workspace>/<string:function>/conversation/<string:conv_id>/<string:req_lang>",
    methods=["GET"])
def get_conversation(workspace, function, conv_id, req_lang): # pylint: disable=R0913,C0301,W0613  # Many arguments for reusable code and some extras to make the routing work
    """ Return all languages """
    resp_messages=list()
    conv_recs=TABLE.scan(
            FilterExpression=Attr('conversation_id').eq(conv_id))['Items']
    for conv_message in conv_recs:
        if not conv_message['translations'].get(req_lang):
            conv_message=translate_message(conv_message,req_lang)
            TABLE.put_item(Item=conv_message)
        if conv_message['moderate']=="true":
            if str(conv_message.get('mod_status')).startswith('approved'):
                ret_text=conv_message['translations'].get(req_lang,'Unavailable')
            else:
                if str(conv_message.get('mod_status')).startswith('needs'):
                    ret_text='Moderation Required'
                else:
                    ret_text="Message Rejected"
        else:
            ret_text=conv_message['translations'].get(req_lang)
        resp_messages.append(dict({'id':conv_message['id'], 'text':ret_text, 'create_dttm':conv_message.get('create_dttm',0)}))
    resp_messages.sort(key=operator.itemgetter('create_dttm'))


    return jsonify(resp_messages),200

#https://dev.api.cot-refinery.com/dev/message_hub/moderate/{id}/{approve/reject}
@app.route(
    "/<string:workspace>/<string:function>/moderate/<string:m_id>/<string:action>",
    methods=["PUT"])
def moderate_message(workspace, function, m_id, action): # pylint: disable=R0913,C0301,W0613  # Many arguments for reusable code and some extras to make the routing work
    """save moderated message status"""
    message=TABLE.query(KeyConditionExpression=Key('id').eq(m_id))['Items'][0]
    if action in {'approve','reject'}:
        if action == 'approve':
            message['mod_status']='approved_manual'
        else:
            message['mod_status']='rejected_manual'
        TABLE.put_item(Item=message)
    else:
        action='Invalid Action'
    return jsonify(action),200
