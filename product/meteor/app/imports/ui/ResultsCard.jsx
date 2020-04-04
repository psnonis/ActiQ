import React           from 'react'
import Say             from 'react-say'


import Card            from '@material-ui/core/Card'
import CardActionArea  from '@material-ui/core/CardActionArea'
import CardActions     from '@material-ui/core/CardActions'
import CardContent     from '@material-ui/core/CardContent'
import CardMedia       from '@material-ui/core/CardMedia'
import Button          from '@material-ui/core/Button'
import Typography      from '@material-ui/core/Typography'

import Paper           from '@material-ui/core/Paper'
import Grid            from '@material-ui/core/Grid'

import Table          from '@material-ui/core/Table'
import TableBody      from '@material-ui/core/TableBody'
import TableCell      from '@material-ui/core/TableCell'
import TableHead      from '@material-ui/core/TableHead'
import TableRow       from '@material-ui/core/TableRow'

import { Session     } from 'meteor/session'
import { makeStyles  } from '@material-ui/core/styles'
import { withTracker } from 'meteor/react-meteor-data'

import { primary,
         secondary   } from './Themes'

const useStyles = makeStyles(theme => (
{
  card :
  {
    maxWidth: 345,
    padding: theme.spacing(1),
  },
}))

const css =
{
  root :
  {
    width           : '100%',
    marginTop       : 8,
    borderRadius    : 4,
//  backgroundColor : secondary
  },

  tab :
  {
  },

  gif :
  {
  },
}

function speak(text)
{
  var msg = new SpeechSynthesisUtterance(text)
  window.speechSynthesis.speak(msg)
}

class ResultsPart extends React.Component
{
  constructor(props)
  {
    super(props)

    console.log(`client > Results > constr : ${JSON.stringify(this.props)}`)
  }

  render = () =>
  {
    console.log(`client > Results > render`)

  //const results = this.props.context.results // this does not work
  //const results = Session.get('RESULTS')     // this does not work without withTracker
    const results = this.props.results
    const first   = this.props.first

    console.log(`client > Results > render : Answers = ${JSON.stringify(results, null, 4)}`)

    if (results && results.clips)
    {
      return (
        <Paper style={css.root}>
          <Table style={css.tab}>
            <TableHead>
              <TableRow>
                <TableCell>Rank </TableCell>
                <TableCell>Video</TableCell>
                <TableCell>Start</TableCell>
                <TableCell>End  </TableCell>
                <TableCell>Model</TableCell>
                <TableCell>Terms</TableCell>
                <TableCell align="right">Probability</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {results.clips.map(hit => (
                <TableRow key={hit.rank}>
                  <TableCell              >{hit.rank }</TableCell>
                  <TableCell              >{hit.video}</TableCell>
                  <TableCell              >{hit.start}</TableCell>
                  <TableCell              >{hit.end  }</TableCell>
                  <TableCell              >{hit.model}</TableCell>
                  <TableCell              >{hit.terms}</TableCell>
                  <TableCell align="right">{`${(hit.probability * 100).toFixed(2)} %`}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )
    }
    else
    {
      if (first)
      {
        return (
          <Paper style={css.root}>
            <Grid container item justify="center" style={css.roo}>
              <iframe src="circle.html" height={261} frameBorder="0" />
            </Grid>
            <Say speak={`please make an activity query`} />
          </Paper>
        )
      }
      else
      {
        return (
          <Paper style={css.root}>
            <Grid container item justify="center" style={css.root}>
              <img style={css.gif} src="tiki.gif" height={261} />
            </Grid>
            <Say speak={`searching...`} />
          </Paper>
        )
      }
    }
  }
}

export default ResultsCard = withTracker(() =>
{
  let results = Session.get('RESULTS')
  let first   = Session.get('FIRST'  )
  
  console.log(`client > Results > trackr : RESULTS = ${results}, FIRST = ${first}`)

  return { results : results, first : first }

})(ResultsPart)