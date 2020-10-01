import React, { useState, useEffect } from 'react'
import { Picker, View, Text } from 'react-native'
import { TextInput, Button } from '@ciorg/ccl'
import { APIKEY, MESSAGE_URL, CONVERSATION_URL } from './../env'

const languages = new Map([
  ['Afrikaans', 'af'],
  ['Albanian', 'sq'],
  ['Amharic', 'am'],
  ['Arabic', 'ar'],
  ['Azerbaijani', 'az'],
  ['Bengali', 'bn'],
  ['Bosnian', 'bs'],
  ['Bulgarian', 'bg'],
  ['Chinese (Simplified)', 'zh'],
  ['Chinese (Traditional)', 'zh-TW'],
  ['Croatian', 'hr'],
  ['Czech', 'cs'],
  ['Danish', 'da'],
  ['Dari', 'fa-AF'],
  ['Dutch', 'nl'],
  ['English', 'en'],
  ['Estonian', 'et'],
  ['Finnish', 'fi'],
  ['French', 'fr'],
  ['French (Canada)', 'fr-CA'],
  ['Georgian', 'ka'],
  ['German', 'de'],
  ['Greek', 'el'],
  ['Hausa', 'ha'],
  ['Hebrew', 'he'],
  ['Hindi', 'hi'],
  ['Hungarian', 'hu'],
  ['Indonesian', 'id'],
  ['Italian', 'it'],
  ['Japanese', 'ja'],
  ['Korean', 'ko'],
  ['Latvian', 'lv'],
  ['Malay', 'ms'],
  ['Norwegian', 'no'],
  ['Persian', 'fa'],
  ['Pashto', 'ps'],
  ['Polish', 'pl'],
  ['Portuguese', 'pt'],
  ['Romanian', 'ro'],
  ['Russian', 'ru'],
  ['Serbian', 'sr'],
  ['Slovak', 'sk'],
  ['Slovenian', 'sl'],
  ['Somali', 'so'],
  ['Spanish', 'es'],
  ['Spanish (Mexico)', 'es-MX'],
  ['Swahili', 'sw'],
  ['Swedish', 'sv'],
  ['Tagalog', 'tl'],
  ['Tamil', 'ta'],
  ['Thai', 'th'],
  ['Turkish', 'tr'],
  ['Ukrainian', 'uk'],
  ['Urdu', 'ur'],
  ['Vietnamese', 'vi'],
])

const langKeys = Array.from(languages, ([key, value]) => ({ key, value }))

interface messageStructure {
  create_dttm: number
  id: string
  text: string
}

export const PostMessage = () => {
  const [message, setMessage] = useState('')
  const [moderate, setModerate] = useState(false)
  const [selectedLang, setSelectedLang] = useState(languages.get('English'))
  const [conversation, setConversation] = useState<messageStructure[]>([])
  const [idInput, setIdInput] = useState('')
  const [conversationID, setConversationID] = useState('')
  useEffect(() => {
    retrieveConversation(conversationID)
    const interval = setInterval(() => {
      retrieveConversation(conversationID)
    }, 2000)
    return () => clearInterval(interval)
  }, [selectedLang, conversationID])
  const postMessage = () => {
    try {
      const options = {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          apikey: APIKEY,
        },
        body: JSON.stringify({
          conversation_id: conversationID,
          lang: selectedLang,
          message_text: message,
          moderate: moderate ? 'true' : 'false',
        }),
      }
      const url = MESSAGE_URL
      fetch(url, options).then(async (response) => {
        if (response.ok) {
          const json = await response.json()
          console.log(json)
          retrieveConversation(conversationID)
        } else {
          console.log(`Response not okay`, response)
        }
      })
    } catch (err) {
      console.log(`Error occured making call`)
    }
  }

  const retrieveConversation = (conversationId: string) => {
    if (!conversationID) {
      return
    }
    try {
      const options = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          apikey: APIKEY,
        },
      }
      const url = CONVERSATION_URL + '/' + conversationId + '/' + selectedLang
      fetch(url, options).then(async (response) => {
        if (response.ok) {
          let json = await response.json()
          json = json.reverse()
          if (conversation != json) {
            setConversation(json)
          }
        } else {
          console.log(`Response not okay`, response)
        }
      })
    } catch (err) {
      console.log(`Error occured making call`)
    }
  }
  return (
    <View>
      <View style={{ flexDirection: 'row', alignSelf: 'center', alignItems: 'center', marginVertical: 20 }}>
        <Text>Preferred Language: </Text>
        <Picker
          selectedValue={selectedLang}
          style={{ height: 30, width: 120, alignSelf: 'center' }}
          onValueChange={(itemValue) => setSelectedLang(itemValue)}
        >
          {langKeys.map((l) => (
            <Picker.Item label={l.key} value={l.value} />
          ))}
        </Picker>
        <TextInput label="Conversation ID:" onChangeText={setIdInput} value={idInput} />
        <Button
          label="Submit ID"
          contained
          onPress={() => {
            if (idInput) {
              setConversationID(idInput)
            }
          }}
        />
      </View>
      <View style={{ flexDirection: 'row', justifyContent: 'space-around' }}>
        <View style={{ alignContent: 'center', width: '40%' }}>
          <TextInput label="Message:" onChangeText={setMessage} value={message} />
          <Button
            label={moderate ? 'Needs Moderation' : 'No Moderation Needed'}
            onPress={() => setModerate(!moderate)}
            outlined
          />
          <View style={{ height: 50 }} />
          <Button
            label="Submit"
            contained
            large
            onPress={() => {
              if (message) {
                postMessage()
              }
            }}
          />
        </View>
        <View style={{ alignContent: 'center', width: '40%' }}>
          <Text style={{ fontWeight: 'bold', fontSize: 18, marginBottom: 10 }}>Conversation:</Text>
          {conversation.map((message) => (
            <View
              style={{
                borderColor: 'grey',
                borderWidth: 1,
                borderRadius: 5,
                padding: 3,
                margin: 3,
              }}
            >
              <Text style={{ fontSize: 10, color: 'grey' }}>{new Date(message.create_dttm).toTimeString() + ': '}</Text>
              <Text>{message.text}</Text>
            </View>
          ))}
        </View>
      </View>
    </View>
  )
}
