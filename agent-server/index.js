import express from "express";
import sqlite3 from "sqlite3";
import cors from "cors";

const app = express();
const db = new sqlite3.Database("grp9agents.db");

app.use(cors());
app.use(express.json());

/**
 * @param {Error} text
 */
function log(text) {
	console.error(`${text.name}: ${text.message}`);
}

app.get("/api/agents", function(_req, res) {
	db.all(`SELECT 
				agent_code AS code,
				agent_name AS name,
				working_area AS working_area,
				commission AS commission,
				phone_no AS phone_no,
				country as country
			FROM GRP9AGENTS`, function(err, rows) {
		if (err === null) res.send(rows);
		else {
			res.sendStatus(500);
			log(err);
		}
	});
});

app.get("/api/agents/:code", function(req, res) {
	const code = req.params["code"];

	db.get(`SELECT 
				agent_code AS code,
				agent_name AS name,
				working_area AS working_area,
				commission AS commission,
				phone_no AS phone_no,
				country as country
			FROM GRP9AGENTS WHERE agent_code = ?`, [code],
			function(err, row) {
				if (err === null)
					if (row === undefined) res.sendStatus(404);
					else res.send(row);
				else {
					res.sendStatus(500);
					log(err);
				}
		}
	);
});

function getId() {
	db.all(`SELECT * FROM GRP9AGENTS`, function(err, rows) {
		if (err === null)
			return `A0${rows.length + 1}`;
		else {
			log(err);
			return null;
		}
	});
}

app.post("/api/agents", function(req, res) {
	const json_data = req.body;

	db.exec(
		"INSERT INTO GRP9AGENTS VALUES (?, ?, ?, ?, ?, ?)",
		[getId(), json_data["name"], json_data["working_area"], json_data["commission"], json_data["phone_no"], json_data["country"]],
		function(err) {
			if (err !== null) {
				res.sendStatus(500);
				log(err);
			} else res.sendStatus(200);
		}
	);
});

app.delete("/api/agents/:code", function(req, res) {
	const code = req.params['code'];

	db.get(`SELECT 
				agent_code AS code,
				agent_name AS name,
				working_area AS working_area,
				commission AS commission,
				phone_no AS phone_no,
				country as country
			FROM GRP9AGENTS WHERE agent_code = ?`, [code], function(err, row) {
		if (err === null)
			if (row === undefined) res.sendStatus(404);
			else
				db.exec("DELETE FROM GRP9AGENTS WHERE agent_code = ?", [code],
					function(err) {
						if (err === null) res.send(row);
						else {
							res.sendStatus(500);
							log(err);
						}
					}
				);
		else {
			res.sendStatus(500);
			log(err);
		}
	});
});

app.put("/api/agents/:code", function(req, res) {
	const code = req.params['code'];
	const data = req.body;

	db.get(`SELECT
				agent_code AS code,
				agent_name AS name,
				working_area AS working_area,
				commission AS commission,
				phone_no AS phone_no,
				country as country
			FROM GRP9AGENTS WHERE agent_code = ?`, [code], function(err, row) {
		if (err === null)
			if (row === undefined) res.sendStatus(404);
			else {
				// update the fields to change in row
				// send it back to the database

				for (let key of Object.keys(data)) {
					row[key] = data[key];
				}
				
				db.exec(
					`UPDATE GRP9ORDERS set
						AGENT_NAME = $name,
						WORKING_AREA = $working_area,
						COMMISSION = $commission,
						PHONE_NO = $phone_no,
						COUNTRY = $country
						 WHERE agent_code = $code`,
					row,
					function(err) {
						if (err === null) res.send(row);
						else {
							res.sendStatus(500);
							log(err);
						}
					}
				);
			}
		else {
			res.sendStatus(500);
			log(err);
		}
	});
});

const port = 8081;
app.listen(port, '0.0.0.0', function() {
    console.log(`Listening on port ${port}`);
});
