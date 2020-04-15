import { Meteor }      from 'meteor/meteor'

import React           from 'react'
import PropTypes       from 'prop-types'

import { withStyles }  from '@material-ui/core/styles'
import AppBar          from '@material-ui/core/AppBar'
import Toolbar         from '@material-ui/core/Toolbar'
import Typography      from '@material-ui/core/Typography'
import Button          from '@material-ui/core/Button'
import IconButton      from '@material-ui/core/IconButton'

import TextField from '@material-ui/core/TextField'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import DialogContentText from '@material-ui/core/DialogContentText'
import DialogTitle from '@material-ui/core/DialogTitle'

import PersonIcon from '@material-ui/icons/Person'
import Avatar from '@material-ui/core/Avatar'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListItemAvatar from '@material-ui/core/ListItemAvatar'
import ListItemText from '@material-ui/core/ListItemText'

import GitHubIcon      from '@material-ui/icons/GitHub'
import LibraryBooksIcon from '@material-ui/icons/LibraryBooks'
import RecentActorsIcon from '@material-ui/icons/RecentActors'

const styles =
{
    root :
    {
      flexGrow     : 1,
      borderRadius : 4,
      marginTop    : 8,      
    },

    bar :
    {
        borderRadius : 4,
    },

    grow :
    {
      flexGrow : 1,
    },
  }
 
  function DisplayLine(props)
  {
    const { classes } = props
    
    const [info, setInfo] = React.useState(false)

    const show = (state) => {setInfo(state)}
    const info_c = () => {setInfo(false)}

    return (
        <div className={classes.root}>
          <AppBar className={classes.bar} position='static'>
            <Toolbar>
              <IconButton className={classes.grow} color='inherit' onClick={e => {show(true)}}>
                <RecentActorsIcon/>
              </IconButton>
              <IconButton className={classes.grow} color='inherit' onClick={e => {window.open('https://github.com/psnonis/ActiQ')}}>
                <GitHubIcon/>
              </IconButton>
              <IconButton className={classes.grow} color='inherit' onClick={e => {window.open('https://docs.google.com/presentation/d/16wY1BWNKs8n2tiggHMR0kiOwXq4y-T_o6tc7OFJxyqk')}}>
                <LibraryBooksIcon/>
              </IconButton>
            </Toolbar>
          </AppBar>
          <Dialog open={info} onClose={() => show(false)} aria-labelledby='form-dialog-title'>
            <DialogTitle id='form-dialog-title'>Meet the ActiQ Team Members</DialogTitle>
            <List>
              {[{name : 'Connor Stern',    profile : 'cs.png'},
                {name : 'Pri Nonis',       profile : 'pn.png'},
                {name : 'Vinicio De Sola', profile : 'vs.png'}].map((who) => (
              <ListItem button key={who.name}>
                <ListItemAvatar>
                  <Avatar className={classes.avatar} src={who.profile}>
                    <PersonIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText primary={who.name} />
              </ListItem>
            ))}
            </List>
            <DialogActions>
              <Button onClick={() => show(false)} color='primary'>
                OK
              </Button>
            </DialogActions>
          </Dialog>

          {/* <Dialog open={open} onClose={handleClickClose} aria-labelledby='form-dialog-title'>
            <DialogTitle id='form-dialog-title'>Subscribe</DialogTitle>
            <DialogContent>
              <DialogContentText>
                To subscribe to this website, please enter your email address here. We will send updates
                occasionally.
              </DialogContentText>
              <TextField
                autoFocus
                margin='dense'
                id='name'
                label='Email Address'
                type='email'
                fullWidth
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClickClose} color='primary'>
                Cancel
              </Button>
              <Button onClick={handleClickClose} color='primary'>
                Subscribe
              </Button>
            </DialogActions>
          </Dialog>           */}
        </div>
    )
  }
  
  DisplayLine.propTypes =
  {
    classes : PropTypes.object.isRequired,
  }
  
  export default withStyles(styles)(DisplayLine)
