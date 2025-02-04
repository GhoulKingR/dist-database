import express from "express";
import sqlite3 from "sqlite3";
import cors from "cors";

const app = express();
const db = new sqlite3.Database("grp9customer.db");

app.use(cors());
app.use(express.json());

/**
 * @param {Error} text
 */
function log(text) {
	console.error(`${text.name}: ${text.message}`);
}

app.get("/api/customers", function(_req, res) {
	db.all(`SELECT 
				cust_code AS code,
				cust_name AS name,
				cust_city AS city,
				working_area AS working_area,
				cust_country AS country,
				grade AS grade,
				opening_amt AS opening_amt,
				receive_amt AS receive_amt,
				payment_amt AS payment_amt,
				outstanding_amt AS outstanding_amt,
				phone_no AS phone_no,
				agent_code AS agent_code
			FROM GRP9CUSTOMER`, function(err, rows) {
		if (err === null) res.send(rows);
		else {
			res.sendStatus(500);
			log(err);
		}
	});
});

app.get("/api/customers/:code", function(req, res) {
	const code = req.params["code"];

	db.get(`SELECT 
				cust_code AS code,
				cust_name AS name,
				cust_city AS city,
				working_area AS working_area,
				cust_country AS country,
				grade AS grade,
				opening_amt AS opening_amt,
				receive_amt AS receive_amt,
				payment_amt AS payment_amt,
				outstanding_amt AS outstanding_amt,
				phone_no AS phone_no,
				agent_code AS agent_code
			FROM GRP9CUSTOMER WHERE cust_code = ?`, [code],
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

/**
 * @returns {string | null}
 */
function getId() {
	db.all(`SELECT * FROM GRP9CUSTOMER`, function(err, rows) {
		if (err === null)
			return `C0${rows.length + 1}`;
		else {
			log(err);
			return null;
		}
	});
}

app.post("/api/customers", function(req, res) {
	const json_data = req.body;

	db.exec(
		"INSERT INTO GRP9CUSTOMER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
		[
            getId(), json_data["name"], json_data["city"], json_data["working_area"],
            json_data["country"], json_data["grade"], json_data["opening_amt"], json_data["receive_amt"],
            json_data["payment_amt"], json_data["outstanding_amt"], json_data["phone_no"], json_data["agent_code"]
		],
		function(err) {
			if (err !== null) {
				res.sendStatus(500);
				log(err);
			} else res.sendStatus(200);
		}
	);
});

app.delete("/api/customers/:code", function(req, res) {
	const code = req.params['code'];

	db.get(`SELECT 
				cust_code AS code,
				cust_name AS name,
				cust_city AS city,
				working_area AS working_area,
				cust_country AS country,
				grade AS grade,
				opening_amt AS opening_amt,
				receive_amt AS receive_amt,
				payment_amt AS payment_amt,
				outstanding_amt AS outstanding_amt,
				phone_no AS phone_no,
				agent_code AS agent_code
			FROM GRP9CUSTOMER WHERE cust_code = ?`, [code], function(err, row) {
		if (err === null)
			if (row === undefined) res.sendStatus(404);
			else
				db.exec("DELETE FROM GRP9CUSTOMER WHERE cust_code = ?", [code], function(err) {
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

app.put("/api/customers/:code", function(req, res) {
	const code = req.params['code'];
	const data = req.body;

	db.get(`SELECT 
				cust_code AS code,
				cust_name AS name,
				cust_city AS city,
				working_area AS working_area,
				cust_country AS country,
				grade AS grade,
				opening_amt AS opening_amt,
				receive_amt AS receive_amt,
				payment_amt AS payment_amt,
				outstanding_amt AS outstanding_amt,
				phone_no AS phone_no,
				agent_code AS agent_code
			FROM GRP9CUSTOMER WHERE cust_code = ?`, [code], function(err, row) {
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
						CUST_NAME = $name,
						CUST_CITY = $city,
						WORKING_AREA = $working_area,
						CUST_COUNTRY = $country,
						GRADE = $grade,
						OPENING_AMT = $opening_amt,
						RECEIVE_AMT = $receive_amt,
						PAYMENT_AMT = $payment_amt,
						OUTSTANDING_AMT = $outstanding_amt,
						PHONE_NO = $phone_no,
						AGENT_CODE = $agent_code
					 WHERE cust_code = $code`,
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

const port = 8082;
app.listen(port, function() {
    console.log(`Listening on port ${port}`);
});
