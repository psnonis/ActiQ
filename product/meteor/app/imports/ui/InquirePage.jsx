import React       from 'react'

import HeadingMenu from './HeadingMenu'
import QueriesCard from './QueriesCard'
import ResultsCard from './ResultsCard'
import GalleryCard from './GalleryCard'

import Container   from '@material-ui/core/Container'

const styling =
{
  roo :
  {
    padding : 0
  }
}

const context =
{
}

const InquirePage = () =>
(
  <Container       id="InquireRoot"   style={styling.roo}>
      <HeadingMenu id="HeadingMenu" context={context}/>
      <QueriesCard id="QueriesCard" context={context}/>
      <ResultsCard id="ResultsCard" context={context}/>
      <GalleryCard id="GalleryCard" context={context}/>
  </Container>
)

export default InquirePage
