import { Meteor        } from 'meteor/meteor'
import { writeFileSync,
         readFileSync  } from 'fs'
import   superagent      from 'superagent'
import { Captures      } from '/imports/api/captures'

Meteor.startup(() =>
{
    console.log('server > main > startup')
})

GetAPIEndpoint = (type, resource) =>
{
    const servers =
    [
        { _id : '169.60.164.52', engine : true },
    ]

    if (type == 'engine')
    {
        var server  = servers[0]._id
        var port    = '5000'

        return `http://${server}:${port}/api/${resource}`
    }
    else
    {
        var server  = servers[0]._id
        var port    = '5001'

        return `http://${server}:${port}/api/${resource}`
    }
}

Meteor.methods(
{
    api_queryIndex : async function (params)
    {
        console.log('server > main > api_queryIndex called')
        console.log(`params > ${JSON.stringify(params, null, 4)}`)

        if (params.terms)
        {
            Captures.remove({})

            var uri       = GetAPIEndpoint('engine', 'queryIndex')

            let response  = await superagent.post(uri)
            .query({ terms : params.terms,
                     knobs : JSON.stringify(params.knobs) })

            console.log(`server > main > api_queryIndex return : ${JSON.stringify(response.body, null, 2)}`)

            return response.body
        }

        throw new Meteor.Error(501, 'Error 501 : Invalid API Params', 'Invalid API Params')
    },

    api_queueCache : async function (params)
    {
        console.log('server > main > api_queueCache called')
        console.log(`params > ${JSON.stringify(params, null, 4)}`)

        if (params.video)
        {
            var uri       = GetAPIEndpoint('engine', 'queueCache')

            let response  = await superagent.post(uri)
            .query({ video : params.video, 
                     stime : params.stime,
                     etime : params.etime })

            console.log(`server > main > api_queueCache return : ${JSON.stringify(response.body, null, 2)}`)

            return response.body
        }

        throw new Meteor.Error(501, 'Error 501 : Invalid API Params', 'Invalid API Params')
    },    
})
