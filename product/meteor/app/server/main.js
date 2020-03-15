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
        { _id : '158.175.150.58', pythia : true, speech : true },
    ]

    if (type == 'pythia')
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
    api_queryIndex_fake : async function (params)
    {
        console.log('server > main > api_queryIndex_fake called')
        console.log(`params > ${JSON.stringify(params, null, 4)}`)

        if (params.query)
        {
            Captures.remove({})

            var result = params.query == 'swimming at beach' ? r1 :
                         params.query == 'playing billiards' ? r2 :
                         params.query == 'taking a bath'     ? r3 : r4

            await new Promise(resolve => setTimeout(resolve, 1000))
    
            console.log(`result > ${JSON.stringify(result, null, 4)}`)
    
            result.clips.forEach( clip =>
            {
                Captures.insert(clip)
            })

            return result
    
            /*
            var uri       = GetAPIEndpoint('pythia', 'getAnswers')

            let response  = await superagent.post(uri)
            .query({ question : params.query})

            Captures.update({ _id : params.user }, { $set : { question : params.query, answer : response.body.image.answer, picture : params.image, createdAt : new Date() } }, { upsert : true })

            console.log(`server > main > api_queryIndex_fake return : ${JSON.stringify(response.body, null, 2)}`)

            return response.body
            */
        }

        throw new Meteor.Error(501, 'Error 501 : Invalid API Params', 'Invalid API Params')
    },

    api_getAnswers_group : async function (params) // Need To Write This Function
    {
        console.log('server > main > api_getAnswers_group called')
      //console.log(params)

        if (params.query)
        {
            var uri       = GetAPIEndpoint('pythia', 'getAnswers')

            console.log(`server > main > api_getAnswers_group return : ${response.text}`)

            return response.body
        }

        throw new Meteor.Error(501, 'Error 501 : Invalid API Params', 'Invalid API Params')
    },

    api_getInterpretation : async function (params)
    {
        console.log('server > main > api_askQuestion called')
      //console.log(params)

        var uri       = GetAPIEndpoint('speech', 'interpret') // TODO: rename interpret to speech and getInterpretation
        var sample    = '../../../../../public/sample_audio.wav' // The Birch Canoe
        var temporary = 'audio.wav'
               
        let stringLength = params.audio.length
        let newString    = params.audio.slice(22, stringLength) // Remove 'data:audio/wav;base64,'
        var audio        = Buffer.from(newString, 'base64') // CONFIRMED WORKING

        writeFileSync(temporary, audio) // save audio to file

        var sampleAudio = readFileSync(sample)
        console.log(sampleAudio)

        var writtenAudio = readFileSync(temporary)
        console.log(writtenAudio)

        // let response  = await superagent.post(url)
        // .attach('audio',  sample)

        let response = await superagent.post(uri)
        .attach('audio',  temporary)
      
        console.log(`server > main > api_askQuestion return : ${response.text}`)

        return response.body
    }
})
