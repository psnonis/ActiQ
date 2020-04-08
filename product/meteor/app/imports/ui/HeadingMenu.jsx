import { Meteor }      from 'meteor/meteor'

import React           from 'react'

import Grid            from '@material-ui/core/Grid'
import AppBar          from '@material-ui/core/AppBar'
import Toolbar         from '@material-ui/core/Toolbar'
import Typography      from '@material-ui/core/Typography'
import IconButton      from '@material-ui/core/IconButton'
import Drawer          from '@material-ui/core/Drawer'
import Badge           from '@material-ui/core/Badge'

import MenuIcon        from '@material-ui/icons/Menu'

import ImportsView     from './ImportsView'

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

  tools :
  {
    marginRight : theme.spacing(2),
  },

  title :
  {
    flexGrow : 1,
  },

  video :
  {
    foreground : 'white'
  },

  queue :
  {
  },
}))

//MF-1m3A8snY

export default function HeadingMenu()
{
  const [state, setState] = React.useState({ show  : false })
  const style             = useStyles()

  return (
    <React.Fragment>
    <Grid id='HeadingRoot' className={style.root}>
      <AppBar position='static' className={style.bar}>
        <Toolbar>
            <IconButton edge='start' className={style.tools} color='inherit' aria-label='menu' onClick={(e) => setState({ show : true })}><MenuIcon/></IconButton>
            <Typography edge='start' className={style.title} color='inherit' variant='h6'>Video Activity Search</Typography>
            <Badge badgeContent={4} color='secondary'></Badge>
        </Toolbar>
      </AppBar>
      <Drawer anchor='right' open={state.show} onClose={(e) => setState({ show : false })}><ImportsView/></Drawer>
    </Grid>
    </React.Fragment>
  )
}