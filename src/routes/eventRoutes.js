const express = require('express');
const router = express.Router();
const eventController = require('../controllers/eventController');
const auth = require('../middleware/auth');
const { validateEvent } = require('../middleware/validate');


router.post('/create', validateEvent, eventController.createEvent);
router.post('/uploadCal', auth, eventController.uploadCal);
router.post('/manualSel', auth, eventController.manualSel);
router.get('/recommendations', eventController.recommendations);
router.post('/upvote', auth, eventController.upvote);
router.post('/finalizeTime', auth, eventController.finalizeTime);

module.exports = router;