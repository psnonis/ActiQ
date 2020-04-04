import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'

import InquirePage from './InquirePage'
import ImportsPage from './ImportsPage'
import MissingPage from './MissingPage'

const Router = () => (
    <BrowserRouter>
        <Switch>
            <Route exact path='/'        component={InquirePage}/>
            <Route exact path='/import/' component={ImportsPage}/>
            <Route                       component={MissingPage}/>
        </Switch>
    </BrowserRouter>
)

export default Router