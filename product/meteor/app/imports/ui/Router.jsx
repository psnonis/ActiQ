import React       from 'react'

import PrimaryPage from './PrimaryPage'
import MissingPage from './MissingPage'

import { BrowserRouter,
         Route,
         Switch        } from 'react-router-dom'

const Router = () => (
    <BrowserRouter>
        <Switch>
            <Route exact path='/'        component={PrimaryPage}/>
            <Route                       component={MissingPage}/>
        </Switch>
    </BrowserRouter>
)

export default Router