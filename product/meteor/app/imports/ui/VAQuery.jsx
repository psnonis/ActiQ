import React           from 'react'

import Container       from '@material-ui/core/Container'
import Paper           from '@material-ui/core/Paper'
import Grid            from '@material-ui/core/Grid'
import Box             from '@material-ui/core/Box'

import QuizBox         from './QuizBox'

import { makeStyles  } from '@material-ui/core/styles'
import { primary,
         secondary   } from './Themes'

const styles = makeStyles(theme => (
{
  container :
  {
    display  : 'flex',
    flexWrap : 'wrap',
  },
  textField :
  {
    marginLeft  : theme.spacing(1),
    marginRight : theme.spacing(1),
  },
  dense :
  {
    marginTop : theme.spacing(2),
  },
  menu :
  {
    width : 200,
  },
}))

const css =
{
  roo :
  {
    padding    : 0,
//  marginTop  : 8,
    background : 'transparent',
  },

  pac :
  {
    display    : 'flex',
    width      : '100%',
    marginTop  : 8,
    alignItems : 'center',
    background : 'magenta',
  },

  cam :
  {
    display      : 'flex',
    background   : 'black',
    width        : '100%',
    borderRadius : 4
  },

  pam :
  {
    display    : 'flex',
    width      : '100%',
    marginTop  : 8,
    alignItems : 'center',
    background : 'magenta',

/*  width      : '100%',
    marginTop  : 8,
    overflowX  : 'auto',
    background : 'magenta'
*/    
  },

  mic :
  {
    display      : 'block',
    width        : '100%',
    background   : primary,
    borderRadius : 4
  },

  box :
  {
    marginTop   : 8,
  }
}

export default class VAQuery extends React.Component
{
  render = () =>
  {
    console.log(`client > VAQuery > render`)

    return (
      <Container style={css.roo}>
        <Paper style={css.pac}>
          
        </Paper>
        <Paper style={css.pam}>
          
        </Paper>
        <QuizBox style={css.box}
                  context={this.props.context}
                  question={this.state.question}
                  onTypeText={this.onTypeText}
                  onClickAsk={this.onClickAsk} />
      </Container>
    )
  }

  constructor (props)
  {
    super(props)

    this.queryIndex = this.queryIndex.bind(this)
    this.onClickAsk = this.onClickAsk.bind(this)

    this.ready = true
    this.state = 
    {
      question : 'swimming at beach',
      record   : false,
      vidCon   :
      {
        facingMode : 'environment',
        height     : 240,
        width      : 360,
      }
    }
  }

  setRef = (webcam) =>
  {
    this.webcam = webcam
  }

  queryIndex = () =>
  {
    if (!this.ready)
    {
      console.log(`client > VAQuery > queryIndex : Not Ready`)
    }
    else
    {
      this.ready = false

      console.log(`client > VAQuery > queryIndex`)

      var   question = this.state.question

      console.log('client > VAQuery > queryIndex : callin api_queryIndex_fake')
  
      Session.set(  'FIRST', false)
      Session.set('RESULTS',  null)

      Meteor.call('api_queryIndex_fake', { query : question }, (err, res) =>
      {
        console.log('client > VAQuery > queryIndex : return api_queryIndex_fake')

        if (err) console.log(`ERR => ${err}`)
        if (res) console.log(`RES => ${JSON.stringify(res, null, 4)}`)

        Session.set('RESULTS', res ? res : null)

        this.ready = true
      })
    }
  }

  onClickAsk = (e) =>
  {
    console.log(`client > VAQuery > onClickAsk`)

    this.queryIndex()
  }

  onTypeText = (e) =>
  {
    console.log(`client > VAQuery > onTypeText`)

    this.setState({ question : e.target.value })
  }
}
