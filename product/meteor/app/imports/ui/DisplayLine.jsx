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
import Snackbar        from '@material-ui/core/Snackbar'
import Fab             from '@material-ui/core/Fab'

import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';
import RestoreIcon from '@material-ui/icons/Restore';
import FavoriteIcon from '@material-ui/icons/Favorite';      
import LocationOnIcon from '@material-ui/icons/LocationOn';

import MenuIcon             from '@material-ui/icons/Menu'
import AddIcon              from '@material-ui/icons/Add';
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';

import { makeStyles  } from '@material-ui/core/styles'
import { primary,
         secondary   } from './Themes'

const useStyles = makeStyles(theme => (
{
  root :
  {
    flexGrow        : 1,
    borderRadius    : 4,
    marginTop       : 8,
    backgroundColor : primary
  },
  snackbar :
  {
    [theme.breakpoints.down('xs')] :
    {
      bottom: 90,
    }
  }
}))

export default function DisplayLine()
{
  const cls = useStyles()
  const [value, setValue] = React.useState(0)

  return (
    <BottomNavigation value={value}
                      onChange={(event, newValue) => {setValue(newValue)}}
                      className={cls.root}
                      showLabels>
        <BottomNavigationAction label="Recents"   icon={<RestoreIcon    />} />
        <BottomNavigationAction label="Favorites" icon={<FavoriteIcon   />} />
        <BottomNavigationAction label="Nearby"    icon={<LocationOnIcon />} />
    </BottomNavigation>      
  )
}
