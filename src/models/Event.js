const mongoose = require('mongoose');

const eventSchema = new mongoose.Schema({
    eventId: {
        type: String,
        required: true,
    },
    title: {
        type: String,
        required: true,
    },
    owner: {
        type: String,
        required: true,
    },
    meetingDuration: {
        type: String,
        required: true,
    },
    description: {
        type: String,
        required: false,
    },
    preferedDates: {
        type: Array,
        required: true,
        validate: {
            validator: function(arr) {
                return arr.length > 0;
            },
            message: 'Array cannot be empty'
        }
    },
    timezone: {
        type: String,
        required: true,
    },
    startTime: {
        type: Date,
        required: true,
    },
    endTime: {
        type: Date,
        required: true,
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
    updatedAt: {
        type: Date,
        default: Date.now,
    },
});

eventSchema.pre('save', function(next) {
    this.updatedAt = Date.now();
    next();
});

const Event = mongoose.model('Event', eventSchema);

module.exports = Event;