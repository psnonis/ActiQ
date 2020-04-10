import React            from 'react'

import Paper            from '@material-ui/core/Paper'
import Grid             from '@material-ui/core/Grid'
import Toolbar          from '@material-ui/core/Toolbar'
import IconButton       from '@material-ui/core/IconButton'
import Table            from '@material-ui/core/Table'
import TableBody        from '@material-ui/core/TableBody'
import TableCell        from '@material-ui/core/TableCell'
import TableHead        from '@material-ui/core/TableHead'
import TableRow         from '@material-ui/core/TableRow'
import TextField        from '@material-ui/core/TextField'
import CircularProgress from '@material-ui/core/CircularProgress'

import AddIcon          from '@material-ui/icons/Add'

import { Session     }  from 'meteor/session'
import { makeStyles  }  from '@material-ui/core/styles'
import { withTracker }  from 'meteor/react-meteor-data'

import { primary,
         secondary   } from './Themes'
import { Divider     } from '@material-ui/core'

const useStyles = makeStyles(theme => (
{
  card :
  {
    maxWidth : 345,
    padding  : theme.spacing(1),
  },
}))

const css =
{
  root :
  {
    width           : '100%',
    marginTop       : 8,
    borderRadius    : 4,
  },

  tools :
  {
    background : 'red'
  },

  table :
  {
  },
}

class ImportsPart extends React.Component
{
  constructor(props)
  {
    super(props)

    console.log(`client > Imports > constr : ${JSON.stringify(this.props)}`)

    this.queueCache = this.queueCache.bind(this)

    this.ready = true
    this.state = 
    {
      video : '',
    }    
  }

  queueCache = (video) =>
  {
    if (!this.ready)
    {
      console.log(`client > Imports > queueCache : Not Ready`)
    }
    else
    {
      this.ready = false

      var  video = 'MF-1m3A8snY' // this.state.video
      var  stime = 0
      var  etime = 600

      console.log(`client > Imports > queueCache : callin api_queueCache : VIDEO = ${video}`)
  
      Session.set('CACHE', [])

      Meteor.call('api_queueCache', { video : video, stime : stime, etime : etime }, (err, res) =>
      {
        console.log('client > Imports > queueCache : return api_queueCache')

        if (err)
        {
            console.log(`client > Imports > queueCache : ERR = ${err}`)
            Session.set('ERROR', true)
        }

        if (res)
        {
            console.log(`client > Imports > queueCache : RES = ${JSON.stringify(res, null, 4)}`)
        }

        this.ready = true
      })
    }

  }
 
  render = () =>
  {
    const cache = this.props.cache
    const video = this.state.video

    console.log(`client > Imports > render : CACHE = ${JSON.stringify(cache, null, 4)}`)

    return (
      <React.Fragment>
        <Toolbar className={css.tools}>
            <TextField  edge='end' className={css.video} color='secondary' placeholder='VideoID' value={video} onChange={(e) => this.setState({ video : e.target.value })}/>
            <IconButton edge='end' className={css.fetch} color='inherit' onClick={(e) => this.queueCache(video)}><AddIcon/></IconButton>
        </Toolbar>
        <Divider/>
        <Paper style={css.root} elevation={3}>
          <Table style={css.table} size='small'>
            <TableHead>
              <TableRow>
                <TableCell>VideoID</TableCell>
                <TableCell>Stage</TableCell>
                <TableCell align='right'>Progress</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {cache.map(video => (
                <TableRow key={video.id}>
                  <TableCell              >{video.id}</TableCell>
                  <TableCell              >{video.stage}</TableCell>
                  <TableCell align='right'><CircularProgress /></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
        </React.Fragment>
    )
  }
}

export default ImportsCard = withTracker(() =>
{
  let cache = Session.get('CACHE')
  
  console.log(`client > Imports > trackr : CACHE = ${cache}`)

  return { cache : [{id : 'YgVHI0nrfA4', stage : 'predict-sf', progress : 58.0}] }

})(ImportsPart)

