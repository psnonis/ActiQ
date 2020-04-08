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
  //console.log(`client > Queries > render`)

    return (
      <Container id="QueriesRoot" style={css.root}>
        <QuizBox style={css.box}
                 context={this.props.context}
                 terms={this.state.terms}
                 chips={this.state.chips}                 
                 knobs={this.state.knobs}
                 color={this.state.color}
                 onChangeTerms={this.onChangeTerms}
                 onChangeChips={this.onChangeChips}
                 onClickSTitle={this.onClickSTitle}
                 onClickSearch={this.onClickSearch} />
      </Container>
    )
  }

  constructor (props)
  {
    super(props)

    this.queryIndex    = this.queryIndex.bind(this)

    this.onChangeTerms = this.onChangeTerms.bind(this)    
    this.onChangeChips = this.onChangeChips.bind(this)
    this.onClickSTitle = this.onClickSTitle.bind(this)
    this.onClickSearch = this.onClickSearch.bind(this)

    this.ready = true
    this.state = 
    {
      terms : '',
      chips : [],
      knobs :
      {
          subtitles : false,
          all_terms : true
      },
      color : 'default'
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

      var  chips = this.state.chips
      var  terms = this.state.terms
      var  knobs = this.state.knobs

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

  onClickSearch = (e) =>
  {
    console.log(`client > Queries > onClickSearch`)

    this.queryIndex()
  }

  onClickSTitle = (e) =>
  {
    console.log(`client > Queries > onClickSTitle : KNOBS = ${JSON.stringify(this.state.knobs, null, 2)}`)

    this.setState({ knobs : { ...this.state.knobs, subtitles : !this.state.knobs.subtitles } })
    this.setState({ color : this.state.color == 'secondary' ? 'default' : 'secondary' })

    this.setState({ chips :[] })
    this.setState({ terms :'' })
  }

  onChangeTerms = (e) =>
  {
    console.log(`client > Queries > onChangeTerms : ${JSON.stringify(e.target.value)}`)

    this.setState({ terms : e.target.value })
  }

  onChangeChips = (e, v) =>
  {
    console.log(`client > Queries > onChangeChips : ${JSON.stringify(v)}`)

    this.setState({ chips : v })
  }
}
