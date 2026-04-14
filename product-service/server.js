const express = require('express');
const app = express();

// =========================
// LOAD CONTROL (YOUR ORIGINAL)
// =========================
let currentRequests = 0;
const MAX_REQUESTS = 100;  // limit concurrent load

// =========================
// CHAOS CONFIG (UPDATED)
// =========================
 CHAOS_ENABLED = false;   // 🔥 now dynamic (IMPORTANT)
const FAILURE_RATE = 0.2;   // 20% failures
const LATENCY_RATE = 0.3;   // 30% slow responses

// =========================
// PRODUCTS API
// =========================
app.get('/products', async (req, res) => {

    // 🔥 LOAD SHEDDING (your original)
    if (currentRequests >= MAX_REQUESTS) {
        console.log("[LOAD] Overload - request rejected");
        return res.status(503).json({ error: "Server overloaded" });
    }

    currentRequests++;

    try {

        // =========================
        // CHAOS ENGINEERING (ADDED)
        // =========================
        if (CHAOS_ENABLED) {

            const rand = Math.random();

            // 🔴 RANDOM FAILURE
            if (rand < FAILURE_RATE) {
                console.log("[CHAOS] Simulated failure");
                return res.status(503).json({ error: "Simulated failure" });
            }

            // 🟡 LATENCY SPIKE
            let delay = 700;

            if (rand < FAILURE_RATE + LATENCY_RATE) {
                delay = 2500;
                console.log("[CHAOS] Latency spike");
            }

            await new Promise(resolve => setTimeout(resolve, delay));

        } else {
            // normal behavior
            await new Promise(resolve => setTimeout(resolve, 700));
        }

        // =========================
        // RESPONSE
        // =========================
        res.json([
            { id: 1, name: "Laptop" },
            { id: 2, name: "Phone" }
        ]);

    } finally {
        currentRequests--;
    }
});

// =========================
// 🔥 STEP 2: CHAOS CONTROL API
// =========================
app.post('/toggle-chaos', express.json(), (req, res) => {

    const { enabled } = req.body;

    CHAOS_ENABLED = enabled;

    console.log("[CONTROL] Chaos set to:", CHAOS_ENABLED);

    res.json({
        chaos: CHAOS_ENABLED
    });
});

// =========================
// HEALTH CHECK (OPTIONAL)
// =========================
app.get('/health', (req, res) => {
    res.json({
        status: "ok",
        currentRequests,
        maxCapacity: MAX_REQUESTS,
        chaos: CHAOS_ENABLED
    });
});

// =========================
// START SERVER
// =========================
app.listen(4002, () => {
    console.log("Product service running on 4002");
});