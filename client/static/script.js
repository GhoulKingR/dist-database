(() => {
    const orderServerServer = "http://127.0.0.1:8080/api/orders";
    const agentServerPort = "http://127.0.0.1:8081";

    const table = document.querySelector("table");

    // fetch all orders
    fetch(orderServerServer)
        .then(res => res.json())
        .then(res => {
            for (let order of res) {
                const tr = document.createElement("tr");

                const num = document.createElement("td");
                num.innerText = order["num"];
                tr.appendChild(num);

                const amount = document.createElement("td");
                amount.innerText = order["amount"];
                tr.appendChild(amount);

                const advance_amount = document.createElement("td");
                advance_amount.innerText = order["advance_amount"];
                tr.appendChild(advance_amount);

                const ord_date = document.createElement("td");
                ord_date.innerText = order["ord_date"];
                tr.appendChild(ord_date);

                const cust_code = document.createElement("td");
                const cust_page = document.createElement("a");
                cust_page.setAttribute("href", `/customer/${order["cust_code"]}`);
                cust_page.innerText = order["cust_code"];
                cust_code.appendChild(cust_page);
                tr.appendChild(cust_code);

                const agent_code = document.createElement("td");
                const agent_page = document.createElement("a");
                agent_page.setAttribute("href", `/agent/${order["agent_code"]}`);
                agent_page.innerText = order["agent_code"];
                agent_code.appendChild(agent_page);
                tr.appendChild(agent_code);

                const description = document.createElement("td");
                description.innerText = order["description"];
                tr.appendChild(description);

                table.appendChild(tr);
            }
        });
})();

/**
 * Ideas for what to build with the database hasn't come to mind yet
 * Current ideas so far are:
 * - A table where users can get information about customers their orders and agents assigned to their orders.
 * - A client where the main focus is the orders. Users can see which customer and agent an order belongs to.
 */
