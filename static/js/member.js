// export to base
// var
const nav__sign = document.querySelector(".nav__sign");
const modal__box = document.querySelector(".modal__box");
const remind = document.querySelector(".remind");
const message = document.querySelector(".message");
// model
async function get_data_from_api(url) {
    const response = await fetch(url, {
        method: "GET",
    });
    const message = await response.json();
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
async function patch_data_to_api(url, data) {
    const resp = await fetch(url, {
        method: "PATCH",
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
function render_nav__sign(text) {
    nav__sign.textContent = text;
}
function render_remind_signin() {
    const remind_node = document.createElement("p");
    const remind_span_node = document.createElement("span");
    remind_node.textContent = "已經有帳戶了?";
    remind_node.className = "remind";
    remind_span_node.textContent = "點此登入";
    remind_span_node.className = "remind_signin_link";
    remind_node.appendChild(remind_span_node);
    modal__box.appendChild(remind_node);
}
function render_remind_signup() {
    const remind_node = document.createElement("p");
    const remind_span_node = document.createElement("span");
    remind_node.textContent = "還沒有帳戶?";
    remind_node.className = "remind";
    remind_span_node.textContent = "點此註冊";
    remind_span_node.className = "remind_signup_link";
    remind_node.appendChild(remind_span_node);
    modal__box.appendChild(remind_node);
}
function remove_remind() {
    const remind = document.querySelector(".remind");
    modal__box.removeChild(remind);
}
function render_message(m) {
    const message_node = document.createElement("p");
    message_node.className = "message";
    message_node.textContent = m;
    modal__box.appendChild(message_node);
}
function remove_modal_message() {
    if (message) {
        modal__box.removeChild(message);
    }
}
function render_signin_placeholder() {
    const inputs = document.querySelectorAll(".signin__input");
    inputs[0].placeholder = "輸入電子信箱";
    inputs[1].placeholder = "輸入密碼";
}
function render_signup_placeholder() {
    const inputs = document.querySelectorAll(".signup__input");
    inputs[0].placeholder = "輸入姓名";
    inputs[1].placeholder = "輸入電子信箱";
    inputs[2].placeholder = "輸入密碼";
}
// controller
function check_current_user() {
    get_data_from_api("/api/user").then((message) => {
        if (message["data"]) {
            render_nav__sign("登出系統");
            check_reservation_signin();
        } else {
            render_nav__sign("登入/註冊");
            check_reservation_unsignin();
        }
    });
}
function check_reservation_signin() {
    const nav__reserve = document.querySelector(".nav__reserve");
    nav__reserve.onclick = () => {
        location.href = "/booking";
    };
}
function check_reservation_unsignin() {
    const nav__reserve = document.querySelector(".nav__reserve");
    nav__reserve.onclick = () => {
        open_modal_for_reserve();
    };
}
function open_modal_for_reserve() {
    const modal = document.querySelector(".modal");
    modal.dataset.active = "true";
    switch_sign("signin");
}
function switch_sign(which) {
    const signin_content = document.querySelector(".signin");
    const signup_content = document.querySelector(".signup");
    if (which == "signin") {
        signin_content.dataset.active = "true";
        signup_content.dataset.active = "";
        render_signin_placeholder();
        render_remind_signup();
        click_to_signup();
        signin();
    } else if (which == "signup") {
        signup_content.dataset.active = "true";
        signin_content.dataset.active = "";
        render_signup_placeholder();
        render_remind_signin();
        click_to_signin();
        signup();
    }
}
function click_to_signin() {
    const remind_signin = document.querySelector(".remind_signin_link");
    remind_signin.addEventListener("click", () => {
        remove_modal_message();
        remove_remind();
        switch_sign("signin");
    });
}
function click_to_signup() {
    const remind_signup = document.querySelector(".remind_signup_link");
    remind_signup.addEventListener("click", () => {
        remove_modal_message();
        remove_remind();
        switch_sign("signup");
    });
}
function open_modal() {
    const nav__sign = document.querySelector(".nav__sign");
    const modal = document.querySelector(".modal");
    nav__sign.addEventListener("click", () => {
        if (nav__sign.textContent == "登入/註冊") {
            modal.dataset.active = "true";
            switch_sign("signin");
        } else {
            signout();
        }
    });
}
function close_modal() {
    const modal = document.querySelector(".modal");
    const close = document.querySelector(".close");
    close.addEventListener("click", () => {
        remove_remind();
        remove_modal_message();
        modal.dataset.active = "";
    });
    window.addEventListener("click", (e) => {
        if (e.target == modal) {
            remove_remind();
            remove_modal_message();
            modal.dataset.active = "";
        }
    });
}
function signin() {
    const inputs = document.querySelectorAll(".signin__input");
    const submit = document.querySelector(".signin__button");
    submit.addEventListener("click", () => {
        email = inputs[0];
        password = inputs[1];
        if (email.validity.valid && password.validity.valid) {
            patch_data_to_api("/api/user", {
                email: email.value,
                password: password.value,
            }).then((message) => {
                email.placeholder = "輸入電子信箱";
                password.placeholder = "輸入密碼";
                remove_modal_message();
                if (message["ok"]) {
                    location.reload();
                } else {
                    render_message(message["message"]);
                }
            });
        } else if (!email.validity.valid) {
            email.placeholder = email.validationMessage;
        } else if (!password.validity.valid) {
            password.placeholder = password.validationMessage;
        }
        email.value = null;
        password.value = null;
    });
}
function signup() {
    const inputs = document.querySelectorAll(".signup__input");
    const submit = document.querySelector(".signup__button");
    submit.addEventListener("click", () => {
        text = inputs[0];
        email = inputs[1];
        password = inputs[2];
        if (
            text.validity.valid &&
            email.validity.valid &&
            password.validity.valid
        ) {
            post_data_to_api("/api/user", {
                name: text.value,
                email: email.value,
                password: password.value,
            }).then((message) => {
                text.placeholder = "輸入姓名";
                email.placeholder = "輸入電子信箱";
                password.placeholder = "輸入密碼";
                remove_modal_message();
                if (message["ok"]) {
                    location.reload();
                } else {
                    render_message(message["message"]);
                }
            });
        } else if (!text.validity.valid) {
            text.placeholder = text.validationMessage;
        } else if (!email.validity.valid) {
            email.placeholder = email.validationMessage;
        } else if (!password.validity.valid) {
            password.placeholder = password.validationMessage;
        }
        text.value = null;
        email.value = null;
        password.value = null;
    });
}
function signout() {
    delete_data_in_api("/api/user").then(() => {
        location.reload();
    });
}
// main
window.onload = check_current_user();
open_modal();
close_modal();
