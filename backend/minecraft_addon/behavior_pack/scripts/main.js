import { world, system } from "@minecraft/server";

// Listen to player chat messages
world.afterEvents.chatSend.subscribe((event) => {
    const player = event.sender;
    const message = event.message;

    // If you type "!ai [your command]" in game
    if (message.startsWith("!ai ")) {
        const query = message.replace("!ai ", "").trim();
        
        player.sendMessage(`§b[AI Companion]§r Thinking about: "${query}"...`);

        // Log the event so Minecraft records it / we can send it to our server
        console.warn(`[AI_LOG] Player: ${player.name} | Action: chat_command | Message: ${query}`);
        
        // TODO: In the next step, we will hook this up to fetch data 
        // from your deployed Python backend URL!
    }
});
