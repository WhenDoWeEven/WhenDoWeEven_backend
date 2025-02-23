const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

// Function to handle user login
exports.login = async (req, res) => {
    try {
        const { username, password } = req.body;
        user_db = await User.findOne({ username });
        
        if (!user_db) {
            const hashedPassword = await bcrypt.hash(password, 10);
            
            const user = new User({
                username,
                password: hashedPassword
            });
            
            user_db = await user.save();
            const token = jwt.sign({ userId: user_db._id }, process.env.JWT_SECRET);
            res.status(201).json({ user_db, token });
            return;
        }

        const isMatch = await bcrypt.compare(password, user_db.password);
    
        if (!isMatch) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        
        
        const token = jwt.sign({ userId: user_db._id }, process.env.JWT_SECRET);
        res.json({ user_db, token });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};
