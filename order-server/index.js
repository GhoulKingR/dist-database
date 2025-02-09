import express from "express";
import sqlite3 from "sqlite3";
import cors from "cors";

const app = express();
const db = new sqlite3.Database("grp9order.db");

app.use(cors());
app.use(express.json());

/**
 * @param {Error} text
 */
function log(text) {
	console.error(`${text.name}: ${text.message}`);
}

app.get("/api/orders", function(_req, res) {
	db.all(`SELECT 
				ord_num AS num,
				ord_amount AS amount,
				advance_amount AS advance_amount,
				ord_date AS ord_date,
				cust_code AS cust_code,
				agent_code AS agent_code,
				ord_description as description
			FROM GRP9ORDERS`, function(err, rows) {
		if (err === null) res.send(rows);
		else {
			res.sendStatus(500);
			log(err);
		}
	});
});

app.get("/api/orders/:num", function(req, res) {
	const num = req.params["num"];

	db.get(`SELECT 
				ord_num AS num,
				ord_amount AS amount,
				advance_amount AS advance_amount,
				ord_date AS ord_date,
				cust_code AS cust_code,
				agent_code AS agent_code,
				ord_description as description
			FROM GRP9ORDERS WHERE ord_num = ?`, [num],
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
	db.all(`SELECT * FROM GRP9ORDERS`, function(err, rows) {
		if (err === null)
			return `20${rows.length + 1}`;
		else {
			log(err);
			return null;
		}
	});
}

app.post("/api/orders", function(req, res) {
	const json_data = req.body;

	db.exec(
		"INSERT INTO GRP9ORDERS VALUES (?, ?, ?, ?, ?, ?, ?)",
		[getId(), json_data["amount"], json_data["advance_amount"], json_data["ord_date"], json_data["cust_code"], json_data["agent_code"], json_data["description"]],
		function(err) {
			if (err !== null) {
				res.sendStatus(500);
				log(err);
			} else res.sendStatus(200);
		}
	);
});

app.delete("/api/orders/:num", function(req, res) {
	const num = req.params['num'];

	db.get(`SELECT 
				ord_num AS num,
				ord_amount AS amount,
				advance_amount AS advance_amount,
				ord_date AS ord_date,
				cust_code AS cust_code,
				agent_code AS agent_code,
				ord_description as description
			FROM GRP9ORDERS WHERE ord_num = ?`, [num], function(err, row) {
		if (err === null)
			if (row === undefined) res.sendStatus(404);
			else
				db.exec("DELETE FROM GRP9ORDERS WHERE ord_num = ?", [num], function(err) {
					if (err === null) res.send(row);
					else {
						res.sendStatus(500);
						log(err);
					}
				});
		else {
			res.sendStatus(500);
			log(err);
		}
	});
});

app.put("/api/orders/:num", function(req, res) {
	const num = req.params['num'];
	const data = req.body;

	db.get(`SELECT 
				ord_num AS num,
				ord_amount AS amount,
				advance_amount AS advance_amount,
				ord_date AS ord_date,
				cust_code AS cust_code,
				agent_code AS agent_code,
				ord_description as description
			FROM GRP9ORDERS WHERE ord_num = ?`, [num], function(err, row) {
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
						ORD_AMOUNT = $amount,
						ADVANCE_AMOUNT = $advance_amount,
						ORD_DATE = $ord_date,
						CUST_CODE = $cust_code,
						AGENT_CODE = $agent_code,
						ORD_DESCRIPTION = $description
					 WHERE ord_num = $num`,
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

const port = 8080;
app.listen(port, '0.0.0.0', function() {
    console.log(`Listening on port ${port}`);
});
