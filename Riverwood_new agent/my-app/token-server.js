const http = require('http');
const { AccessToken } = require('livekit-server-sdk');

const LIVEKIT_API_KEY = 'APILdkCtHXUaFPs';
const LIVEKIT_API_SECRET = 'VfJFmskbAB25Kz2MhOMb5hjTlEsevvNLnLNfbKtbqXYB';

const server = http.createServer((req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (req.url.startsWith('/token')) {
        const url = new URL(req.url, `http://${req.headers.host}`);
        const roomName = url.searchParams.get('room') || 'default-room';
        const participantName = url.searchParams.get('name') || 'user-' + Math.random().toString(36).substring(7);

        // Create access token
        const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
            identity: participantName,
        });

        at.addGrant({
            room: roomName,
            roomJoin: true,
            canPublish: true,
            canSubscribe: true,
        });

        const token = at.toJwt();

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ token, room: roomName }));
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Token server running on http://localhost:${PORT}`);
    console.log(`Get a token: http://localhost:${PORT}/token?room=test-room`);
});

