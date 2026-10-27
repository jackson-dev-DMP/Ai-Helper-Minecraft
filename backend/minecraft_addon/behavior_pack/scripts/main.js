import { world, system } from "@minecraft/server";
import { http, HttpRequest, HttpHeader } from "@minecraft/server-net";

const BACKEND_URL = "https://your-backend-app.onrender.com/api/companion/interact";
const WORLD_SESSION_CODE = "WORLD_FRANCE_01"; 

// 1. Spawn the Allay placeholder companion when you enter the world
world.afterEvents.playerSpawn.subscribe((event) => {
    if (!event.initialSpawn) return; // Run only once per session join
    
    const player = event.player;
    const dimension = player.dimension;

    try {
        const spawnPos = { 
            x: player.location.x + 1, 
            y: player.location.y + 1, 
            z: player.location.z + 1 
        };
        
        // Spawn the Allay in its signature blue!
        const companion = dimension.spawnEntity("minecraft:allay", spawnPos);
        companion.nameTag = "§bGemini (AI Companion)";
        
        player.sendMessage("§b[AI Companion]§r Your blue Allay companion has manifested!");
    } catch (error) {
        player.sendMessage("§c[AI Error]§r Could not spawn Allay entity.");
    }
});

// 2. Listen to chat commands, scan environment, and talk to Gemini
world.afterEvents.chatSend.subscribe(async (event) => {
    const player = event.sender;
    const message = event.message;

    if (message.startsWith("!ai ")) {
        const query = message.replace("!ai ", "").trim();
        player.sendMessage(`§b[Gemini Allay]§r Scanning blocks and thinking...`);

        try {
            // Gather player coordinates & stats
            const loc = player.location;
            const playerPos = {
                x: Math.floor(loc.x),
                y: Math.floor(loc.y),
                z: Math.floor(loc.z)
            };
            
            const healthComponent = player.getComponent("health");
            const currentHealth = healthComponent ? healthComponent.currentValue : 20;

            // Radar scan for nearby blocks (helping you find what to mine/break)
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

            // Scan for nearby mobs/threats
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

            // Build payload for backend
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

            // Send request to Render backend
            const request = new HttpRequest(BACKEND_URL);
            request.method = "POST";
            request.body = payload;
            request.headers = [
                new HttpHeader("Content-Type", "application/json")
            ];

            const response = await http.request(request);
            
            if (response.status === 200) {
                const data = JSON.parse(response.body);
                // Print Gemini's response in chat
                world.sendMessage(`§a[AI Companion]§r ${data.ai_response}`);
            } else {
                player.sendMessage(`§c[AI Error]§r Server returned status ${response.status}`);
            }

        } catch (error) {
            player.sendMessage(`§c[AI Error]§r Could not reach backend: ${error}`);
        }
    }
});
