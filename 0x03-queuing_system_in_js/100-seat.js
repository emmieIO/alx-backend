const express = require('express');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');

const app = express();
const client = redis.createClient();
const queue = kue.createQueue();

const reserveSeat = async (number) => {
    const setAsync = promisify(client.set).bind(client);
    await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
    const getAsync = promisify(client.get).bind(client);
    const availableSeats = await getAsync('available_seats');
    return parseInt(availableSeats);
};

app.get('/available_seats', async (req, res) => {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', async (req, res) => {
    const reservationEnabled = await getCurrentAvailableSeats() > 0;
    if (!reservationEnabled) {
        res.json({ status: 'Reservation are blocked' });
        return;
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            res.json({ status: 'Reservation failed' });
        } else {
            res.json({ status: 'Reservation in process' });
        }
    });

    job.on('complete', (result) => {
        console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (errorMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
});

app.get('/process', async (req, res) => {
    res.json({ status: 'Queue processing' });

    const availableSeats = await getCurrentAvailableSeats();
    await reserveSeat(availableSeats - 1);

    if (availableSeats === 1) {
        await reserveSeat(0);
        reservationEnabled = false;
    }

    if (availableSeats >= 1) {
        queue.process('reserve_seat', async (job, done) => {
            try {
                // Perform seat reservation logic here
                done();
            } catch (error) {
                done(new Error('Reservation failed'));
            }
        });
    } else {
        queue.process('reserve_seat', async (job, done) => {
            done(new Error('Not enough seats available'));
        });
    }
});

app.listen(1245, () => {
    console.log('Server listening on port 1245');
});