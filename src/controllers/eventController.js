const Event = require('../models/Event');
const { v4: uuidv4 } = require('uuid');

// Create a new event
exports.createEvent = async (req, res) => {
    try {
        const event = new Event({...req.body, eventId: uuidv4()});
        await event.save();
        res.status(201).send(event);
    } catch (error) {
        res.status(400).send(error);
    }
};

// recomendations
exports.recommendations = async (req, res) => {
    try {
        const htmlContent = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Express HTML</title>
        </head>
        <body>
            <h1>Welcome to BRICK HACK 11</h1>
            <p>This is an HTML response.</p>
        </body>
        </html>
    `;
    res.send(htmlContent);
    } catch (error) {
        res.status(500).send(error);
    }
};

// uploadCal
exports.uploadCal = async (req, res) => {
    // update the logic here
};

// manualSel
exports.manualSel = async (req, res) => {
    // update the logic here
};

// upvote
exports.upvote = async (req, res) => {
    // update the logic here
};

// finalizeTime
exports.finalizeTime = async (req, res) => {
    // update the logic here
};
