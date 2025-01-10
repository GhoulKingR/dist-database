const express = require("express");
const fs = require("fs/promises");
const handlebars = require("handlebars");
const app = express();

app.use(express.static('static'));

app.get("/customer/:code", (req, res) => {
    const code = req.params.code.trim().split("/")[0].trim();
    const customerServerPort = `http://127.0.0.1:8082/api/customers/${code}`;
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
    const customerServerPort = `http://127.0.0.1:8081/api/agents/${code}`;
    fetch(customerServerPort)
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


app.listen(3001, () => {
    console.log("App listening on port 3001...");
});
