// var
const attraction_image = document.querySelector("#attraction_image");
const attraction_name = document.querySelector("#attraction_name");
const booking_date = document.querySelector("#booking_date");
const booking_time = document.querySelector("#booking_time");
const booking_price = document.querySelectorAll("#booking_price");
const attraction_address = document.querySelector("#attraction_address");
const submitButton = document.querySelector("#submit-button");
const user_name = document.querySelector("#user_name");
const booked = document.querySelector(".booked");
const unbook = document.querySelector(".unbook");
const footer = document.querySelector(".footer");

let d_attraction_id;
let d_attraction_name;
let d_attraction_image;
let d_attraction_address;
let d_booking_date;
let d_booking_time;
let d_booking_price;
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
function initInputInfo(n, e) {
  const name = document.querySelector("#name");
  const email = document.querySelector("#email");
  name.value = n;
  email.value = e;
}
async function login_user_name() {
  const resp = await get_data_from_api("/api/user");
  if (resp["data"]) {
    const data = resp["data"];
    render_login_user_name(data["name"]);
    initInputInfo(data["name"], data["email"]);
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
    d_attraction_image = data["attraction"]["image"];
    d_attraction_name = data["attraction"]["name"];
    d_attraction_address = data["attraction"]["address"];
    d_booking_date = data["date"];
    d_booking_time = data["time"];
    d_booking_price = data["price"];
    let data_time_message;
    if (d_booking_time == "afternoon") {
      data_time_message = "下午 4 點到晚上 9 點";
    } else {
      data_time_message = "早上 9 點到下午 4 點";
    }
    render_booking_data(
      d_attraction_image,
      d_attraction_name,
      d_booking_date,
      data_time_message,
      d_booking_price,
      d_attraction_address
    );
    // store attraction id
    d_attraction_id = data["attraction"]["id"];
  } else {
    booked.dataset.active = "";
    unbook.dataset.active = "true";
    footer.dataset.active = "";
  }
}
function delete_booking() {
  const delete_btn = document.querySelector(".delete");
  delete_btn.addEventListener("click", () => {
    delete_data_in_api("/api/booking").then(() => {
      location.reload();
    });
  });
}
function orderObject() {
  const name = document.querySelector("#name");
  const email = document.querySelector("#email");
  const phone = document.querySelector("#phone");
  return {
    price: d_booking_price,
    trip: {
      attraction: {
        id: d_attraction_id,
        name: d_attraction_name,
        address: d_attraction_address,
        image: d_attraction_image,
      },
      date: d_booking_date,
      time: d_booking_time,
    },
    contact: {
      name: name.value,
      email: email.value,
      phone: phone.value,
    },
  };
}
// TapPay
function TapPay() {
  const APP_KEY =
    "app_icwdks3d58xoYoJtjzjOB8HUFTsvLbZfXfYWPrgndGj3onnAb9Sm74xA0YfZ";

  TPDirect.setupSDK(123945, APP_KEY, "sandbox");

  TPDirect.card.setup({
    fields: {
      number: {
        element: "#card-number",
        placeholder: "**** **** **** ****",
      },
      expirationDate: {
        element: "#card-expiration-date",
        placeholder: "MM / YY",
      },
      ccv: {
        element: "#card-ccv",
        placeholder: "ccv",
      },
    },
    styles: {
      // Style all elements
      input: {
        color: "gray",
      },
      // Styling ccv field
      "input.ccv": {
        "font-size": "16px",
      },
      // Styling expiration-date field
      "input.expiration-date": {
        "font-size": "16px",
      },
      // Styling card-number field
      "input.card-number": {
        "font-size": "16px",
      },
      // style focus state
      ":focus": {
        color: "black",
      },
      // style valid state
      ".valid": {
        color: "green",
      },
      // style invalid state
      ".invalid": {
        color: "red",
      },
    },
  });

  TPDirect.card.onUpdate(function (update) {
    if (update.canGetPrime) {
      submitButton.removeAttribute("disabled");
    } else {
      submitButton.setAttribute("disabled", true);
    }
  });

  submitButton.addEventListener("click", (event) => {
    event.preventDefault();
    TPDirect.card.getPrime((result) => {
      if (result.status !== 0) {
        return;
      } else {
        post_data_to_api("/api/orders", {
          prime: result.card.prime,
          order: orderObject(),
        }).then((m) => {
          location.href = "/thankyou" + "?number=" + m["data"]["number"];
        });
      }
    });
  });
}

async function main_exe() {
  login_user_name();
  await booking();
  delete_booking();
  TapPay();
}

// main exe
main_exe();
