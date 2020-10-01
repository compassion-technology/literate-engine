import React, { useState, useEffect } from 'react'
import { View, FlatList } from 'react-native'
import { Button } from '@ciorg/ccl'
import { APIKEY, GET_MOD_LIST, UPDATE_MOD } from './../env'
import { Text } from 'react-native'

export const Moderation = () => {
  const loadData = () => {
    try {
      const options = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          apikey: APIKEY,
        },
      }
      const url = GET_MOD_LIST + `en`
      fetch(url, options).then(async (response) => {
        if (response.ok) {
          const json = await response.json()
          console.log(json)
          setData(json)
        } else {
          console.log(`Response not okay`)
        }
      })
    } catch (err) {
      console.log(`Error occured making call`)
    }
  }
  const [data, setData] = useState<any[]>([])
  useEffect(() => {
    loadData()
  }, [])
  return (
    <View style={{ width: '40%', alignSelf: 'center', paddingVertical: 20 }}>
      <Button label="Load Messages" onPress={() => loadData()} />
      <FlatList data={data} renderItem={({ item }) => <TranslationItem t={item} />} />
    </View>
  )
}

interface translation {
  conversation_id?: string
  id: string
  issues?: any
  mod_status: string
  moderate: boolean
  original_lang: string
  translations?: any
}

interface TranslationItemProps {
  t: translation
}

const TranslationItem = ({ t }: TranslationItemProps) => {
  const [translation, setTranslation] = useState(t)
  return (
    <View
      style={{
        borderWidth: 3,
        backgroundColor:
          translation.mod_status === 'approved_manual'
            ? 'rgba(0, 166, 0, 0.5)'
            : translation.mod_status === 'rejected_manual'
            ? 'rgba(212, 0, 0, 0.5)'
            : 'rgba(0, 0, 0, 0.1)',
        marginTop: 10,
        height: 60,
      }}
    >
      <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
        <View style={{ flexDirection: 'column' }}>
          <Text>{'Lang: ' + translation.original_lang + ' | Conversation Id:' + translation.conversation_id}</Text>
          <Text>{'Message: ' + translation.translations[translation.original_lang]}</Text>
          <Text>{'Issue: ' + translation.issues}</Text>
        </View>
        <View style={{ flexDirection: 'row' }}>
          {translation.mod_status != 'approved_manual' && (
            <Button
              label="approve"
              onPress={() => {
                translation.mod_status = 'approved_manual'
                updateMod(translation.id, 'approve')
                setTranslation({ ...translation })
              }}
            />
          )}
          {translation.mod_status != 'rejected_manual' && (
            <Button
              label="reject"
              onPress={() => {
                translation.mod_status = 'rejected_manual'
                updateMod(translation.id, 'reject')
                setTranslation({ ...translation })
              }}
            />
          )}
        </View>
      </View>
    </View>
  )
}

const updateMod = (id: string, action: string) => {
  try {
    const options = {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        apikey: APIKEY,
      },
    }
    const url = UPDATE_MOD + id + '/' + action
    fetch(url, options).then(async (response) => {
      if (response.ok) {
        const json = await response.json()
        console.log(json)
      } else {
        console.log(`Response not okay`)
      }
    })
  } catch (err) {
    console.log(`Error occured making call`)
  }
}
