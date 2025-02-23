const express = require('express');
const router = express.Router();
const eventController = require('../controllers/eventController');
const auth = require('../middleware/auth');
const { validateEvent } = require('../middleware/validate');


router.get('/home', eventController.home); //done
router.post('/create', auth, validateEvent, eventController.createEvent); //done
router.post('/uploadCal', auth, eventController.uploadCal); //done
router.post('/manualSel', auth, eventController.manualSel);
router.get('/recommendations', auth, eventController.recommendations); //done
router.post('/upvote', auth, eventController.upvote); //done
router.post('/creatorDecisition', auth, eventController.creatorDecisition); //done

module.exports = router;