const { body, validationResult } = require('express-validator');


const validateEvent = [
    body('title').notEmpty().withMessage('Event name is required'),
    (req, res, next) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        next();
    }
];

module.exports = {
    validateEvent
};