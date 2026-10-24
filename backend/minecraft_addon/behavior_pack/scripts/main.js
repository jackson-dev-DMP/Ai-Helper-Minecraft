import { world, system } from "@minecraft/server";
import { http, HttpRequest, HttpHeader } from "@minecraft/server-net";

// Replace this with your actual free cloud backend URL once deployed (e.g., Render/Railway)
const BACKEND_URL = "https://your-backend-app.onrender.com/api/companion/interact";

// Unique session code for your world (change this if you start a new world!)
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
            
            // Get player health component if available
            const healthComponent = player.getComponent("health");
            const currentHealth = healthComponent ? healthComponent.currentValue : 20;

            // 2. Simple radar scan for nearby blocks around the player
            let nearbyBlocks = [];
            const dimension = player.dimension;
            
            // Scan a small 3x3x3 area around the player's feet/head
            for (let dx = -1; dx <= 1; dx++) {
                for (let dy = -1; dy <= 2; dy++) {
                    for (let dz = -1; dz <= 1; dz++) {
                        const checkPos = { x: playerPos.x + dx, y: playerPos.y + dy, z: playerPos.z + dz };
                        try {
                            const block = dimension.getBlock(checkPos);
                            if (block && block.typeId !== "minecraft:air") {
                                // Clean up the name (e.g., "minecraft:diamond_ore" -> "diamond_ore")
                                const blockName = block.typeId.replace("minecraft:", "");
                                if (!nearbyBlocks.includes(blockName)) {
                                    nearbyBlocks.push(blockName);
                                }
                            }
                        } catch (e) {
                            // Ignore out-of-bounds or chunk loading issues
                        }
                    }
                }
            }

            // 3. Scan for nearby entities (mobs/players) in a 6-block radius
            let nearbyMobs = [];
            try {
                const entities = dimension.getEntities({
                    location: player.location,
                    maxDistance: 6,
                    excludeFamilies: ["player"] // Focus on monsters/animals
                });
                
                for (const entity of entities) {
                    const mobName = entity.typeId.replace("minecraft:", "");
                    if (!nearbyMobs.includes(mobName)) {
                        nearbyMobs.push(mobName);
                    }
                }
            } catch (e) {
                // Ignore entity query errors if any
            }

            // 4. Build the rich JSON payload matching our FastAPI backend
            const payload = JSON.stringify({
                session_code: WORLD_SESSION_CODE,
                player_name: player.name,
                action: "world_snapshot",
                message: query,
                environment: {
                    position: playerPos,
                    health: currentHealth,
                    nearby_blocks: nearbyBlocks.slice(0, 10), // Limit list size for speed
                    nearby_mobs: nearbyMobs,
                    inventory: [] // We can expand inventory reading later if needed!
                }
            });

            // 5. Send HTTP POST request to your Python backend
            const request = new HttpRequest(BACKEND_URL);
            request.method = "POST";
            request.body = payload;
            request.headers = [
                new HttpHeader("Content-Type", "application/json")
            ];

            const response = await http.request(request);
            
            if (response.status === 200) {
                const data = JSON.parse(response.body);
                // Print Gemini's tactical response right into the Minecraft chat!
                world.sendMessage(`§a[AI Companion]§r ${data.ai_response}`);
            } else {
                player.sendMessage(`§c[AI Error]§r Server returned status ${response.status}`);
            }

        } catch (error) {
            player.sendMessage(`§c[AI Error]§r Could not reach backend: ${error}`);
        }
    }
});
                            
