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
  root :
  {
    padding    : 0,
//  marginTop  : 8,
    background : 'transparent',
  },

  box :
  {
    marginTop   : 8,
  }
}

export default class QueriesCard extends React.Component
{
  render = () =>
  {
    console.log(`client > Queries > render`)

    return (
      <Container id="QueriesRoot" style={css.root}>
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
      question : 'swimming at beach'
    }
  }

  queryIndex = () =>
  {
    if (!this.ready)
    {
      console.log(`client > Queries > queryIndex : Not Ready`)
    }
    else
    {
      this.ready = false

      console.log(`client > Queries > queryIndex`)

      var   question = this.state.question

      console.log('client > Queries > queryIndex : callin api_queryIndex_fake')
  
      Session.set(  'FIRST', false)
      Session.set('RESULTS',  null)

      Meteor.call('api_queryIndex_fake', { query : question }, (err, res) =>
      {
        console.log('client > Queries > queryIndex : return api_queryIndex_fake')

        if (err) console.log(`ERR => ${err}`)
        if (res) console.log(`RES => ${JSON.stringify(res, null, 4)}`)

        Session.set('RESULTS', res ? res : null)

        this.ready = true
      })
    }
  }

  onClickAsk = (e) =>
  {
    console.log(`client > Queries > onClickAsk`)

    this.queryIndex()
  }

  onTypeText = (e) =>
  {
    console.log(`client > Queries > onTypeText`)

    this.setState({ question : e.target.value })
  }
}
