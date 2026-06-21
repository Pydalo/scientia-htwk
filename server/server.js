import Fastify from "fastify";
import fastifyStatic from "@fastify/static";
import path from "path";
import { fileURLToPath } from "url";
import config from "./config.js";
import { spawn } from "child_process";

function startPython() {
    const py = spawn(
        "..\\scientia\\.venv\\Scripts\\python.exe",
        ["..\\scientia\\backend.py"],
        {
            cwd: "..\\scientia",
            shell: true
        }
    );

    /*
    LINUX::
        const py = spawn(
        "../scientia/.venv/bin/python",
        ["../scientia/backend.py"],
        {
            cwd: "../scientia"
        }
        );
    */

    py.stdout.on("data", (data) => {
        console.log(`[PYTHON] ${data.toString()}`);
    });

    py.stderr.on("data", (data) => {
        console.error(`[PYTHON ERROR] ${data.toString()}`);
    });

    py.on("close", (code) => {
        console.log(`[PYTHON EXIT] Code ${code}`);
    });
}

startPython();

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
    const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            messages: request.body.messages
        })
    });

    if (!response.ok) {
        const err = await response.text();
        reply.code(500).send(err);
        return;
    }

    reply.header("Content-Type", "text/plain");
    reply.header("Transfer-Encoding", "chunked");

    return reply.send(response.body);
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