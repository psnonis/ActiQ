
import { Session } from 'meteor/session'
import { Meteor  } from 'meteor/meteor'
import { render  } from 'react-dom'

import React      from 'react'
import Router     from '/imports/ui/Router'

import { ThemeProvider  } from '@material-ui/core/styles'
import { createMuiTheme } from '@material-ui/core/styles'
import { makeStyles     } from '@material-ui/core/styles'
import { orange,
         blue,
         purple         } from '@material-ui/core/colors'

import Checkbox from '@material-ui/core/Checkbox';

const useStyles = makeStyles(theme => ({
  root: {
    color: theme.status.danger,
    '&$checked': {
      color: theme.status.danger,
    },
  },
  checked: {},
}));

function CustomCheckbox() {

  const cls = useStyles()

  return (
    <Checkbox
      defaultChecked
      classes={{
        root    : cls.root,
        checked : cls.checked,
      }}
    />
  );
}

const theme = createMuiTheme({
  status: {
    danger: orange[500],
  },
  palette: {
    primary: purple
  }
});

Meteor.startup(() =>
{
  Session.set('RESULTS', null)
  Session.set('FIRST',   true)

  render( <ThemeProvider theme={theme}>
            <Router />
          </ThemeProvider>, document.getElementById('react-target'))
})
