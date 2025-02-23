const Event = require('../models/Event');
const { v4: uuidv4 } = require('uuid');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');



// Configure multer for file upload
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        const uploadDir = 'uploads/';
        // Create uploads directory if it doesn't exist
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir);
        }
        cb(null, uploadDir);
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const fileFilter = (req, file, cb) => {
    const allowedTypes = ['.ics', '.icl', '.ifb', '.ical'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowedTypes.includes(ext)) {
        cb(null, true);
    } else {
        cb(new Error('Invalid file type. Only calendar files (ICS, ICL, IFB, ICAL) are allowed.'));
    }
};

const upload = multer({ 
    storage: storage,
    fileFilter: fileFilter
});



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

// home
exports.home = async (req, res) => {
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
    // ics,icl,ifb,ical
    try {
        upload.single('calendarFile')(req, res, async function (err) {
            if (err) {
                return res.status(400).json({ error: err.message });
            }

            if (!req.file) {
                return res.status(400).json({ error: 'No file uploaded' });
            }

            // Parse the calendar file
            const filename = req.file.filename;
            console.log(filename);

            exec(`python scripts/parse_cal.py ${filename}`, (error, stdout, stderr) => {
                if (error) {
                    console.error(`exec error: ${error}`);
                    return res.status(500).json({ error: 'Error executing Python script' });
                }
                if (stderr) {
                    console.error(`stderr: ${stderr}`);
                    return res.status(500).json({ error: 'Error in Python script' });
                }
                console.log(`stdout: ${stdout}`);
                res.status(200).json({ message: 'File processed successfully', output: stdout });
            });
        });
        // res.status(200).json({ message: 'File uploaded successfully'});
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
    
};

// manualSel
exports.manualSel = async (req, res) => {
    // update the logic here
};

// recommendations
exports.recommendations = async (req, res) => {
    try {
        const eventId = req.query.eventId;
        const event = await Event.findOne({ eventId: eventId });

        if (!event) {
            return res.status(404).json({ error: 'Event not found' });
        }

        res.status(200).json({ recommendations: event.recommendations });
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
};

// upvote
exports.upvote = async (req, res) => {
    try {
        const { eventId, recommendationId } = req.body;
        const userId = req.user._id;
        const event = await Event.findOne({ eventId: eventId });

        if (!event) {
            return res.status(404).json({ error: 'Event not found' });
        }

        const recommendation = event.recommendations.find(rec => rec.id == recommendationId);

        if (!recommendation) {
            return res.status(404).json({ error: 'Recommendation not found' });
        }

        recommendation.upvoteCount = (recommendation.upvoteCount || 0) + 1;
        recommendation.upvoteList.push(userId);
        updatedEvent = new Event(event);
        await updatedEvent.save()

        res.status(200).json({ recommendations: updatedEvent.recommendations });
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
};

// finalizeTime
exports.finalizeTime = async (req, res) => {
    // update the logic here
};
