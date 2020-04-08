import React          from 'react';

import Paper          from '@material-ui/core/Paper'
import InputBase      from '@material-ui/core/InputBase'
import Divider        from '@material-ui/core/Divider'
import IconButton     from '@material-ui/core/IconButton'
import Tooltip        from '@material-ui/core/Tooltip'

import TextField      from '@material-ui/core/TextField'
import Autocomplete   from '@material-ui/lab/Autocomplete';

import YouTubeIcon       from '@material-ui/icons/YouTube'
import SearchIcon        from '@material-ui/icons/Search'
import ClosedCaptionIcon from '@material-ui/icons/ClosedCaption';

import { makeStyles } from '@material-ui/core/styles'
import { primary,
         secondary  } from './Themes'
import { labels     } from './Assets'

const useStyles = makeStyles(
{
  root :
  {
    display         : 'flex',
    width           : '100%',
    marginTop       : 8,
    alignItems      : 'center',
  },

  aut :
  {
    marginLeft : 8,
    flex : 1
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

  tag :
  {
  }
})

export default function QuizBox(props, hey) {

//console.log(`client > QuizBox : props = ${JSON.stringify(props, null, 2)} : ${JSON.stringify(hey)}`)

  const cls = useStyles()
  const sub = props.knobs.subtitles

  if (sub)
  {
    return (
      <Paper className={cls.root}>
          <Tooltip title='Options'><IconButton className={cls.opt} onClick={(e) => props.onClickOpt(e)}><YouTubeIcon/></IconButton></Tooltip>
          <Tooltip title='Search Terms'>
            <InputBase className={cls.txt}
                       onChange={(e) => props.onChangeTerms(e)}
                       placeholder='Activity Search Term(s)'
                       value={props.terms} />
          </Tooltip>
          <Tooltip title='Include Subtitles'><IconButton className={cls.sub} onClick={(e) => props.onClickSTitle(e)} color={props.color}><ClosedCaptionIcon/></IconButton></Tooltip>
          <Divider className={cls.sep}/>
          <Tooltip title='Perform Search'   ><IconButton className={cls.ask} onClick={(e) => props.onClickSearch(e)}><SearchIcon/></IconButton></Tooltip>
      </Paper>
    )
  }
  else
  {
    return (
      <Paper className={cls.root}>
          <Tooltip title='Options'><IconButton className={cls.opt} onClick={(e) => props.onClickOpt(e)}><YouTubeIcon/></IconButton></Tooltip>
          <Tooltip title='Search Terms'>
            <Autocomplete className={cls.aut}
                          multiple autoSelect
                          onChange={(e, v) => props.onChangeChips(e, v)}
                          options={labels}
                          getOptionLabel={(option) => option.label}
                          groupBy={(option) => option.model}
                          renderInput={(params) => (
                          <TextField className={cls.tag} {...params} placeholder='Activity Search Chip(s)'/>)}
                          value={props.chips} />
          </Tooltip>
          <Tooltip title='Include Subtitles'><IconButton className={cls.sub} onClick={(e) => props.onClickSTitle(e)} color={props.color}><ClosedCaptionIcon/></IconButton></Tooltip>
          <Divider className={cls.sep}/>
          <Tooltip title='Perform Search'   ><IconButton className={cls.ask} onClick={(e) => props.onClickSearch(e)}><SearchIcon/></IconButton></Tooltip>
      </Paper>
    )
  }
}
