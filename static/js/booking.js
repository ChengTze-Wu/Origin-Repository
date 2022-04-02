// var
const attraction_image = document.querySelector("#attraction_image");
const attraction_name = document.querySelector("#attraction_name");
const booking_date = document.querySelector("#booking_date");
const booking_time = document.querySelector("#booking_time");
const booking_price = document.querySelectorAll("#booking_price");
const attraction_address = document.querySelector("#attraction_address");
const user_name = document.querySelector("#user_name");
const booked = document.querySelector(".booked");
const unbook = document.querySelector(".unbook");
const footer = document.querySelector(".footer");
// model
async function get_data_from_api(url) {
    const resp = await fetch(url, {
        method: "GET",
    });
    const message = await resp.json();
    return message;
}
async function post_data_to_api(url, data) {
    const resp = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: new Headers({ "Content-Type": "application/json" }),
    });
    const message = await resp.json();
    return message;
}
async function delete_data_in_api(url) {
    const resp = await fetch(url, {
        method: "DELETE",
    });
    const message = await resp.json();
    return message;
}
// view
function render_booking_data(ai, an, bd, bt, bp, aa) {
    attraction_image.src = ai;
    attraction_name.textContent = an;
    booking_date.textContent = bd;
    booking_time.textContent = bt;
    booking_price.forEach((b) => {
        b.textContent = bp;
    });
    attraction_address.textContent = aa;
}
function render_login_user_name(un) {
    user_name.textContent = un;
}
// controller
async function login_user_name() {
    const resp = await get_data_from_api("/api/user");
    if (resp["data"]) {
        render_login_user_name(resp["data"]["name"]);
    } else {
        location.href = "/";
    }
}
async function booking() {
    const resp = await get_data_from_api("/api/booking");
    const data = resp["data"];
    if (data) {
        unbook.dataset.active = "";
        booked.dataset.active = "true";
        footer.dataset.active = "true";
        const data_image = data["attraction"]["image"];
        const data_name = data["attraction"]["name"];
        const data_address = data["attraction"]["address"];
        const data_date = data["date"];
        const data_time = data["time"];
        const data_price = data["price"];
        let data_time_message;
        if (data_time == "afternoon") {
            data_time_message = "下午 4 點到晚上 9 點";
        } else {
            data_time_message = "早上 9 點到下午 4 點";
        }
        render_booking_data(
            data_image,
            data_name,
            data_date,
            data_time_message,
            data_price,
            data_address
        );
    } else {
        booked.dataset.active = "";
        unbook.dataset.active = "true";
        footer.dataset.active = "";
    }
}
function delete_booking() {
    const delete_btn = document.querySelector(".delete");
    delete_btn.addEventListener("click", () => {
        delete_data_in_api("/api/booking").then((m) => {
            console.log(m);
            location.reload();
        });
    });
}
function init_loading() {
    login_user_name();
    booking();
    delete_booking();
}
// main exe
init_loading();
