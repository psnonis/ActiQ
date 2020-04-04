import React       from 'react'

import HeadingMenu from './HeadingMenu'
import AuditorCard from './AuditorCard'
import GalleryCard from './GalleryCard'

import Container   from '@material-ui/core/Container'

const styling =
{
  root :
  {
    padding : 0
  }
}

const context =
{
  first   : true,
  results : null
}

const ImportsPage = () =>
(
  <Container       id="ImportsRoot"   style={styling.root}>
      <HeadingMenu id="HeadingMenu" context={context}/>
      <AuditorCard id="AuditorCard" context={context}/>
      <GalleryCard id="GalleryCard" context={context}/>
  </Container>
)

export default ImportsPage
