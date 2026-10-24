import { world, system } from "@minecraft/server";
import { http, HttpRequest, HttpHeader } from "@minecraft/server-net";

// REPLACE this with your deployed Render backend URL
const BACKEND_URL = "https://your-backend-app.onrender.com/api/companion/interact";

// Unique session code for your world
const WORLD_SESSION_CODE = "WORLD_FRANCE_01"; 

world.afterEvents.chatSend.subscribe(async (event) => {
    const player = event.sender;
    const message = event.message;

    if (message.startsWith("!ai ")) {
        const query = message.replace("!ai ", "").trim();
        player.sendMessage(`§b[AI Companion]§r Scanning environment & asking Gemini...`);

        try {
            // 1. Gather player coordinates & stats
            const loc = player.location;
            const playerPos = {
                x: Math.floor(loc.x),
                y: Math.floor(loc.y),
                z: Math.floor(loc.z)
            };
            
            const healthComponent = player.getComponent("health");
            const currentHealth = healthComponent ? healthComponent.currentValue : 20;

            // 2. Radar scan for nearby blocks
            let nearbyBlocks = [];
            const dimension = player.dimension;
            
            for (let dx = -1; dx <= 1; dx++) {
                for (let dy = -1; dy <= 2; dy++) {
                    for (let dz = -1; dz <= 1; dz++) {
                        const checkPos = { x: playerPos.x + dx, y: playerPos.y + dy, z: playerPos.z + dz };
                        try {
                            const block = dimension.getBlock(checkPos);
                            if (block && block.typeId !== "minecraft:air") {
                                const blockName = block.typeId.replace("minecraft:", "");
                                if (!nearbyBlocks.includes(blockName)) {
                                    nearbyBlocks.push(blockName);
                                }
                            }
                        } catch (e) {}
                    }
                }
            }

            // 3. Scan for nearby mobs
            let nearbyMobs = [];
            try {
                const entities = dimension.getEntities({
                    location: player.location,
                    maxDistance: 6,
                    excludeFamilies: ["player"]
                });
                
                for (const entity of entities) {
                    const mobName = entity.typeId.replace("minecraft:", "");
                    if (!nearbyMobs.includes(mobName)) {
                        nearbyMobs.push(mobName);
                    }
                }
            } catch (e) {}

            // 4. Build JSON payload
            const payload = JSON.stringify({
                session_code: WORLD_SESSION_CODE,
                player_name: player.name,
                action: "world_snapshot",
                message: query,
                environment: {
                    position: playerPos,
                    health: currentHealth,
                    nearby_blocks: nearbyBlocks.slice(0, 10),
                    nearby_mobs: nearbyMobs,
                    inventory: []
                }
            });

            // 5. Send HTTP POST request
            const request = new HttpRequest(BACKEND_URL);
            request.method = "POST";
            request.body = payload;
            request.headers = [
                new HttpHeader("Content-Type", "application/json")
            ];

            const response = await http.request(request);
            
            if (response.status === 200) {
                const data = JSON.parse(response.body);
                world.sendMessage(`§a[AI Companion]§r ${data.ai_response}`);
            } else {
                player.sendMessage(`§c[AI Error]§r Server returned status ${response.status}`);
            }

        } catch (error) {
            player.sendMessage(`§c[AI Error]§r Could not reach backend: ${error}`);
        }
    }
});
        
