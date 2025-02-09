const express = require("express");
const fs = require("fs/promises");
const handlebars = require("handlebars");
const app = express();

const {
	customerServer,
	agentServer,
} = require("./servers.config.js");

app.use(express.static('static'));

app.get("/customer/:code", (req, res) => {
    const code = req.params.code.trim().split("/")[0].trim();
    const customerServerPort = `${customerServer}/api/customers/${code}`;
    fetch(customerServerPort)
        .then(response => response.json())
        .then(data => {
            fs.readFile("templates/customers.html")
                .then(buffer => {
                    const source = buffer.toString();
                    const template = handlebars.compile(source);
                    const result = template(data);
                    res.send(result);
                })
                .catch(err => {
                    console.error(err);
                    res.sendStatus(500).send("Internal Server Error");
                });
        })
        .catch(err => {
            console.error(err);
            res.sendStatus(500).send("Internal Server Error");
        });
});

app.get("/agent/:code", (req, res) => {
    const code = req.params.code.trim().split("/")[0].trim();
    const agentServerPort = `${agentServer}/api/agents/${code}`;
    fetch(agentServerPort)
        .then(response => response.json())
        .then(data => {
            fs.readFile("templates/agents.html")
                .then(buffer => {
                    const source = buffer.toString();
                    const template = handlebars.compile(source);
                    const result = template(data);
                    res.send(result);
                })
                .catch(err => {
                    console.error(err);
                    res.sendStatus(500).send("Internal Server Error");
                });
        })
        .catch(err => {
            console.error(err);
            res.sendStatus(500).send("Internal Server Error");
        });
});


app.listen(3001, '0.0.0.0', () => {
    console.log("App listening on port 3001...");
});
