import { Meteor }      from 'meteor/meteor'

import React           from 'react'

import Container       from '@material-ui/core/Container'
import Grid            from '@material-ui/core/Grid'
import Box             from '@material-ui/core/Box'
import AppBar          from '@material-ui/core/AppBar'
import Toolbar         from '@material-ui/core/Toolbar'
import Typography      from '@material-ui/core/Typography'
import Badge           from '@material-ui/core/Badge'
import Button          from '@material-ui/core/Button'
import IconButton      from '@material-ui/core/IconButton'
import Tooltip         from '@material-ui/core/Tooltip'
import Snackbar        from '@material-ui/core/Snackbar'
import Fab             from '@material-ui/core/Fab'

import MenuIcon             from '@material-ui/icons/Menu'
import AddIcon              from '@material-ui/icons/Add';
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';

import { makeStyles  } from '@material-ui/core/styles'
import { primary,
         secondary   } from './Themes'

const useStyles = makeStyles(theme => (
{
  root :
  {
    flexGrow     : 1,
    borderRadius : 4,
  },

  bar :
  {
    backgroundColor : primary,
    borderRadius    : 4,
  },

  menu :
  {
    marginRight : theme.spacing(2),
  },

  title :
  {
    flexGrow : 1,
  },

  import :
  {

  },

  snackbar :
  {
    [theme.breakpoints.down('xs')] :
    {
      bottom: 90,
    }
  }
}))

export default function HeadingMenu()
{
  const cls = useStyles()

  return (
    <React.Fragment>
    <Grid id='HeadingRoot' className={cls.root}>
      <AppBar position='static' className={cls.bar}>
        <Toolbar>
            <IconButton edge='start' className={cls.menu}   color='inherit' aria-label='menu'><MenuIcon/></IconButton>
            <Typography variant='h6' className={cls.title}  color='inherit'                  >Video Activity Search</Typography>
            <IconButton edge='end'   className={cls.import} color='inherit'                  ><Badge badgeContent={4} color='secondary'><AddIcon/></Badge></IconButton>
        </Toolbar>
      </AppBar>
    </Grid>
    </React.Fragment>
  )
}

function gitUpdate(e)
{
  console.log('Git Updating')

/*
  Meteor.call('gitUpdate', {}, (err, res) =>
  {
    console.log(res || 'No Response')
    console.log(err || 'No Error')
  })
*/
}
