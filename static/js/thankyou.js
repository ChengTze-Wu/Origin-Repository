async function get_data_from_api(url) {
    const resp = await fetch(url, {
        method: "GET",
    });
    const message = await resp.json();
    return message;
}

async function renderOrderInfo() {
    const thankyou = document.querySelector("#thankyou");
    const orderNumber = document.createElement("span", "#orderNumber");
    const title = document.createElement("h3");
    const order_msg = document.createElement("p");
    const thankyou_msg = document.createElement("p");

    const url = window.location.href;
    const url_orderNumber = url.substring(url.indexOf("=") + 1);

    const resp = await get_data_from_api("/api/order/" + url_orderNumber);

    orderNumber.textContent = url_orderNumber;
    orderNumber.className = "orderNumber";

    if (resp["error"]) {
        title.textContent = "提醒您。";
        thankyou_msg.textContent = "您尚" + resp["message"];
        thankyou.appendChild(title);
        thankyou.appendChild(thankyou_msg);
    } else {
        if (resp["data"]) {
            if (resp["data"]["status"] == 1) {
                title.textContent = "感謝您完成付款。";
                order_msg.textContent = "您的訂單編號為 ";
                thankyou_msg.textContent = "期待您，未來再次使用台北一日遊。";
                order_msg.appendChild(orderNumber);
                thankyou.appendChild(title);
                thankyou.appendChild(order_msg);
                thankyou.appendChild(thankyou_msg);
            } else if (resp["data"]["status"] == 0) {
                title.textContent = "提醒您。您尚未完成付款。";
                order_msg.textContent = "訂單編號 ";
                orderNumber.className = "orderNumber-nonpay";
                order_msg.appendChild(orderNumber);
                thankyou.appendChild(title);
                thankyou.appendChild(order_msg);
            }
        } else {
            title.textContent = "提醒您。找不到此筆訂單。";
            thankyou.appendChild(title);
        }
    }
}

renderOrderInfo();
