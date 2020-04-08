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
import TextField       from '@material-ui/core/TextField'
import Snackbar        from '@material-ui/core/Snackbar'
import Fab             from '@material-ui/core/Fab'
import Drawer          from '@material-ui/core/Drawer'

import MenuIcon        from '@material-ui/icons/Menu'
import AddIcon         from '@material-ui/icons/Add'

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
export default function ManagerCard()
{
  const cls = useStyles()
  const [state, setState] = React.useState({
    show  : false,
    video : ''
  })

  const toggleDrawer = (show) => (event) =>
  {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift'))
    {
      return
    }

    setState({ ...state, show : show })
  }

  const onChangeVideo = (e) =>
  {
    setState({ video : e.target.value })
  }

  const onClickQueue = (e) =>
  {
    

  }

  const queueCache = () =>
  {
    if (!this.ready)
    {
      console.log(`client > Queries > queryIndex : Not Ready`)
    }
    else
    {
      this.ready = false

      var chips = this.state.chips
      var terms = this.state.terms
      var knobs = this.state.knobs

      console.log(`client > Queries > queryIndex : callin api_queryIndex : CHIPS = ${JSON.stringify(chips, null, 2)}`)
  
      Session.set('FIRST', false)
      Session.set('TABLE',  null)
      Session.set('ERROR', false)

      Meteor.call('api_queryIndex', { terms : terms, chips : chips, knobs : knobs }, (err, res) =>
      {
        console.log('client > Queries > queryIndex : return api_queryIndex')

        if (err)
        {
            console.log(`client > Queries > queryIndex : ERR = ${err}`)
            Session.set('ERROR', true)
        }

        if (res)
        {
            console.log(`client > Queries > queryIndex : RES = ${JSON.stringify(res, null, 4)}`)
            Session.set('TABLE', res.result)
        }

        this.ready = true
      })
    }
  }

  return (
    <React.Fragment>
    <Grid id='HeadingRoot' className={cls.root}>
      <AppBar position='static' className={cls.bar}>
        <Toolbar>
            <IconButton edge='start' className={cls.tools} color='inherit' aria-label='menu' onClick={toggleDrawer(true)}><MenuIcon/></IconButton>
            <Typography edge='start' className={cls.title} color='inherit' variant='h6'>Video Activity Search</Typography>
            <TextField  edge='end'   className={cls.video} color='secondary' placeholder='VideoID' value={state.video} onChange={(e) => onChangeVideo(e)}/>
            <Tooltip title='Import YouTube Video'>
            <IconButton edge='end'   className={cls.fetch} color='inherit' onClick={(e) => onClickFetch(e)}><Badge badgeContent={4} color='secondary'><AddIcon/></Badge></IconButton>
            </Tooltip>
        </Toolbar>
      </AppBar>
      <Drawer anchor='right' open={state.show} onClose={toggleDrawer(false)}><ImportsView/></Drawer>
    </Grid>
    </React.Fragment>
  )
}

export default GalleryCard = withTracker(() =>
{
  let table = Session.get('TABLE')
  let first = Session.get('FIRST')
  let error = Session.get('ERROR')
  
//console.log(`client > Gallery > trackr : TABLE = ${table}, FIRST = ${first}, ERROR = ${error}`)

  return { table : table, first : first, error : error }
})(GalleryPart)
