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

morning = 'JH3iid1bZ1Q'
evening = 'btTKApmxrtk'

r1  = { query : 'swimming at beach',
        clips : [
            { rank : 1, video : morning, start : 223, end : 227, model : 'mp-baseline', terms : 'swimming, beach, kids', probability : 0.97 },
            { rank : 2, video : morning, start : 144, end : 150, model : 'mp-baseline', terms : 'swimming, beach, girl', probability : 0.94 }
        ]
    }

r2  = { query : 'playing billiards',
        clips : [
                    { rank : 1, video : morning, start :   0, end : 30, model : 'mp-baseline', terms : 'swimming, beach, kids', probability : 0.97 },
                    { rank : 2, video : morning, start :  40, end : 35, model : 'mp-baseline', terms : 'swimming, beach, girl', probability : 0.94 },
                    { rank : 3, video : morning, start :  55, end : 75, model : 'mp-baseline', terms : 'swimming, rocks, kids', probability : 0.92 }
                ]
    }

r3  = { query : 'taking a bath',
        clips : [
                    { rank : 1, video : morning, start : 0, end : 30, model : 'mp-baseline', terms : 'swimming, beach, kids', probability : 0.9 },
                    { rank : 2, video : morning, start : 0, end : 30, model : 'mp-baseline', terms : 'swimming, beach, kids', probability : 0.9 }
                ]
    }

r4  = { query : 'snorkeling underwater',
        clips : [
                    { rank : 1, video : evening, start : 0, end : 30, model : 'mp-baseline', terms : 'underwater, snorkle, child', probability : 0.9 }
                ]
    }

fake = [r1, r2, r3, r4]

Meteor.methods(
{
    api_queryFakes : async function (params)
    {
        console.log('server > main > api_queryFakes called')
        console.log(`params > ${JSON.stringify(params, null, 4)}`)

        if (params.terms)
        {
            Captures.remove({})

            var result = params.terms == 'swimming at beach' ? r1 :
                         params.terms == 'playing billiards' ? r2 :
                         params.terms == 'taking a bath'     ? r3 : r4

            await new Promise(resolve => setTimeout(resolve, 1000))
    
            console.log(`result > ${JSON.stringify(result, null, 4)}`)
    
            result.clips.forEach( clip =>
            {
                Captures.insert(clip)
            })

            return result
        }

        throw new Meteor.Error(501, 'Error 501 : Invalid API Params', 'Invalid API Params')
    },

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
                     knobs : params.knobs })

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
