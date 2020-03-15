
import { Session } from 'meteor/session'
import { Meteor  } from 'meteor/meteor'
import { render  } from 'react-dom'

import React      from 'react'
import Router     from '/imports/ui/Router'

import { ThemeProvider  } from '@material-ui/styles'
import { createMuiTheme } from '@material-ui/core/styles'
import { blue, purple   } from '@material-ui/core/colors/blue'

const theme = createMuiTheme({
  palette: {
    primary: blue,
    secondary: purple,
  },
})

Meteor.startup(() =>
{
  Session.set('RESULTS', null)
  Session.set('FIRST',   true)

  render( <ThemeProvider theme={theme}>
            <Router />
          </ThemeProvider>, document.getElementById('react-target'))
})
