import { Mongo  } from 'meteor/mongo'
import { Meteor } from 'meteor/meteor'

export const Queue = new Mongo.Collection('queue')

if (Meteor.isServer)
{
    Queue.remove({})
}
