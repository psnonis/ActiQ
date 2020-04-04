import { withTracker } from 'meteor/react-meteor-data'
import { Captures    } from '/imports/api/captures'

import React           from 'react'

import Container       from '@material-ui/core/Container'
import Paper           from '@material-ui/core/Paper'
import Grid            from '@material-ui/core/Grid'
import GridList        from '@material-ui/core/GridList'
import GridListTile    from '@material-ui/core/GridListTile'
import GridListTileBar from '@material-ui/core/GridListTileBar'
import ListSubheader   from '@material-ui/core/ListSubheader'
import IconButton      from '@material-ui/core/IconButton'
import StarBorderIcon  from '@material-ui/icons/StarBorder'

import { makeStyles }  from '@material-ui/core/styles'
import { primary,
         secondary  }  from './Themes'

const css =
{
  top :
  {
    width      : '100%',
    marginTop  : 8,
    overflowX  : 'auto',
    background : secondary
  },

  root :
  {
    display        : 'flex',
    flexWrap       : 'wrap',
    justifyContent : 'space-around',
    overflow       : 'hidden',
    background     : 'transparent'
  },

  list :
  {
    flexWrap   : 'nowrap',
    transform  : 'translateZ(0)',
    background : 'transparent'
  },

  title :
  {
    color : 'white',
  },

  icon :
  {
    color : 'white'
  },

  tube :
  {
    border : 0
  }
}

class GalleryPart extends React.Component
{
  constructor(props)
  {
    super(props)

    console.log(`client > Results > constr : ${JSON.stringify(this.props)}`)
  }

  getYTLink = (hit) =>
  {
    console.log(hit)

    var link = `https://www.youtube.com/embed/${hit.video}`
    var trim = `start=${hit.start}&end=${hit.end}`
    var opts = 'enablejsapi=1&origin=http://actiq.biz&rel=0&modestbranding=1&autohide=1&showinfo=0&controls=0&autoplay=1&playsinline=1&iv_load_policy=3'
    var more = `cc_load_policy=1`

    return `${link}?${trim}&${opts}&${more}`
  }

  render = () =>
  {
    const results = this.props.results
    const first   = this.props.first

    console.log(`client > Gallery > render : RESULTS = ${JSON.stringify(results)}`)

    if (results && results.clips)
    {
      return (
        <Paper style={css.top}>
          <Grid style={css.root}>
            <GridList style={css.list} cols={2.5}>
              {results.clips.map(hit => (
                <GridListTile key={hit.rank} style={{width:640, height:360, padding:0}}>
                  <iframe style={css.tube} type="text/html" width="640" height="360" allow="autoplay" frameBorder="0"
                          src={this.getYTLink(hit)}></iframe>
                  <GridListTileBar style={css.title} titlePosition="top" title={hit.terms} subtitle={hit.query} actionIcon={<IconButton style={css.icon}></IconButton>} />
                </GridListTile>
              ))}
            </GridList>
          </Grid>
        </Paper>
      )
    }
    else
    {
      if (first)
      {
        return (
          <Paper style={css.roo}>
          </Paper>
        )
      }
      else
      {
        return (
          <Paper style={css.roo}>
          </Paper>
        )
      }
    }
  }
}

export default GalleryCard = withTracker(() =>
{
  let results = Session.get('RESULTS')
  let first   = Session.get('FIRST'  )
  
  console.log(`client > Gallery > trackr : RESULTS = ${results}, FIRST = ${first}`)

  return { results : results, first : first }
})(GalleryPart)
