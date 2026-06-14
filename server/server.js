import Fastify from "fastify";
import fastifyStatic from "@fastify/static";
import path from "path";
import { fileURLToPath } from "url";
import config from "./config.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const fastify = Fastify({
    logger: true
});

fastify.register(fastifyStatic, {
    root: path.join(__dirname, "public"),
    prefix: "/", 
});

fastify.post("/chat", async (request, reply) => {
    const response = await fetch(
        "http://localhost:5000/chat",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: request.body.messages 
            })
        }
    );

    return await response.json();
});

const start = async () => {
    try {
        await fastify.listen({
            port: config.port,
            host: config.host
        });

        console.log("Server läuft auf Port 3000");
    } catch (err) {
        fastify.log.error(err);
        process.exit(1);
    }
};

start();