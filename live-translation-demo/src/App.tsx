import React from 'react'
import { View, useWindowDimensions } from 'react-native'
import { ThemeProvider, useTheme, Hero } from '@ciorg/ccl'
import { Router, Switch, Route } from './components/Router'
import { Moderation } from './pages/Moderation'
import { PostMessage } from './pages/PostMessage'

// const approve = async (id: string) => {
//   console.log('approved ' + id)
// }
const AppContent = () => {
  return (
    <Switch>
      <Route exact path="/">
        <Hero height="100%" title="LIVE TRANSLATION DEMO" backgroundImage={{ uri: './hero.png' }} />
      </Route>
      <Route exact path="/moderation">
        <Moderation />
      </Route>
      <Route exact path="/post-message">
        <PostMessage />
      </Route>
    </Switch>
  )
}

const App = () => {
  const theme = useTheme()
  const { height, width } = useWindowDimensions()

  return (
    <Router>
      <ThemeProvider>
        <View style={{ height, width, backgroundColor: theme.colors.white }}>
          <AppContent />
        </View>
      </ThemeProvider>
    </Router>
  )
}

export default App
