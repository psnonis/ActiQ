import React          from 'react';

import Paper          from '@material-ui/core/Paper'
import InputBase      from '@material-ui/core/InputBase'
import Divider        from '@material-ui/core/Divider'
import IconButton     from '@material-ui/core/IconButton'
//import ToggleButton   from '@material-ui/lab/ToggleButton'

import YouTubeIcon       from '@material-ui/icons/YouTube'
import SearchIcon        from '@material-ui/icons/Search'
import ClosedCaptionIcon from '@material-ui/icons/ClosedCaption';


import { makeStyles } from '@material-ui/core/styles'
import { primary,
         secondary   } from './Themes'

const useStyles = makeStyles(
{
  root :
  {
    display         : 'flex',
    width           : '100%',
    marginTop       : 8,
    alignItems      : 'center',
//  backgroundColor : secondary,
  },

  txt :
  {
    marginLeft : 8,
    flex       : 1,
  },

  opt :
  {
    color           : primary
  },

  sub :
  {
//    color           : primary
  },
  
  ask :
  {
    color           : primary,
    fontSize        : 'large'
  },  

  sep :
  {
    width  : 1,
    height : 28,
    margin : 4,
  },
})

export default function QuizBox(props, hey) {

  console.log(`client > QuizBox : props = ${JSON.stringify(props, null, 2)} : ${JSON.stringify(hey)}`)

  const cls = useStyles()

  return (
    <Paper        className={cls.root}>
      <IconButton className={cls.opt}  onClick={(e) => props.onClickOpt(e)}><YouTubeIcon      /></IconButton>
      <InputBase  className={cls.txt} onChange={(e) => props.onTypeText(e)} placeholder={props.place} value={props.terms} />
      <IconButton className={cls.sub}  onClick={(e) => props.onClickSub(e)} color={props.color}><ClosedCaptionIcon/></IconButton>
      <Divider    className={cls.sep} />
      <IconButton className={cls.ask}  onClick={(e) => props.onClickAsk(e)}><SearchIcon       /></IconButton>
    </Paper>
  )
}