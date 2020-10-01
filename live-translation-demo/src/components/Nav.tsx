import React from 'react'
import { View, StyleSheet, ViewStyle } from 'react-native'
import { TopNavBar, MenuItem, useTheme, AppTheme } from '@ciorg/ccl'
import { useHistory } from './Router'

const createStyles = ({ colors, sizes, spacing }: AppTheme) =>
  StyleSheet.create({
    baseContainer: {
      flexGrow: 1,
      width: spacing.giant,
      backgroundColor: colors.defaultBackground,
    } as ViewStyle,
    titleContainer: {
      width: '100%',
      minHeight: sizes.topNav * 2,
      backgroundColor: colors.primary,
    } as ViewStyle,
  })

export const Nav = ({ apps, pages, onToggleNav }: any) => {
  const history = useHistory()
  const theme = useTheme()
  const styles = createStyles(theme)

  return (
    <View style={styles.baseContainer}>
      <TopNavBar menu onPress={onToggleNav} float transparent />
      <View style={styles.titleContainer} />
      {apps.map((app: any) => (
        <MenuItem label="" icon={app.icon} onPress={() => history.push(`/${app.id}`)} />
      ))}
      {pages.map((page: any) => (
        <MenuItem label="" icon={page.icon} onPress={() => history.push(`/${page.path}`)} />
      ))}
    </View>
  )
}
