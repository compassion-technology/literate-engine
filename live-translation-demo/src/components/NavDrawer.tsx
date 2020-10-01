import React from 'react'
import { View, StyleSheet, ViewStyle, ImageStyle, Text, TextStyle, ImageBackground } from 'react-native'
import { TopNavBar, MenuItem, useTheme, AppTheme } from '@ciorg/ccl'
import { useHistory } from './Router'

const createStyles = ({ colors, sizes, spacing, typography }: AppTheme) =>
  StyleSheet.create({
    baseContainer: {
      flexGrow: 1,
      backgroundColor: colors.defaultBackground,
    } as ViewStyle,
    titleContainer: {
      width: '100%',
      minHeight: sizes.topNav * 2,
      backgroundColor: colors.primary,
      justifyContent: 'center',
      padding: spacing.increased,
    } as ViewStyle,
    titleText: {
      ...typography.caption,
      textAlign: 'center',
      color: colors.lightHighEmphasis,
      paddingTop: spacing.small,
    } as TextStyle,
    image: {
      flex: 1,
    } as ImageStyle,
  })

export const NavDrawer = ({ onToggleNav, apps, pages }: any) => {
  const history = useHistory()
  const theme = useTheme()
  const styles = createStyles(theme)

  return (
    <View style={styles.baseContainer}>
      <TopNavBar menu onPress={onToggleNav} float transparent />
      <View style={styles.titleContainer}>
        <ImageBackground style={styles.image} source={{ uri: './compassion_logo.png' }} resizeMode="contain" />
        <Text style={styles.titleText}>TRANSLATION MANAGER</Text>
      </View>
      {apps.map((app: any) => (
        <MenuItem label={app.name} icon={app.icon} onPress={() => history.push(`/${app.id}`)} />
      ))}
      {pages.map((page: any) => (
        <MenuItem label={page.name} icon={page.icon} onPress={() => history.push(`/${page.path}`)} />
      ))}
    </View>
  )
}
