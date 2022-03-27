// model
async function get_user() {
    response = await fetch("/api/user", {
        method: "GET",
    });
    message = await response.json();
    return message;
}
async function post_user(n, e, p) {
    response = await fetch("/api/user", {
        method: "POST",
        body: JSON.stringify({ name: n, email: e, password: p }),
        headers: new Headers({ "Content-Type": "application/json" }),
    });
    message = await response.json();
    return message;
}
async function patch_user(e, p) {
    response = await fetch("/api/user", {
        method: "PATCH",
        body: JSON.stringify({ email: e, password: p }),
        headers: new Headers({ "Content-Type": "application/json" }),
    });
    message = await response.json();
    return message;
}
async function delete_user() {
    response = await fetch("/api/user", {
        method: "DELETE",
    });
    message = await response.json();
    return message;
}
// view
function render_nav__sign(text) {
    const sign = document.querySelector(".nav__sign");
    sign.textContent = text;
}
function render_remind_signin() {
    const modal__box = document.querySelector(".modal__box");
    const remind = document.createElement("p");
    const remind_span = document.createElement("span");
    remind.textContent = "已經有帳戶了?";
    remind.className = "remind";
    remind_span.textContent = "點此登入";
    remind_span.className = "remind_signin_link";
    remind.appendChild(remind_span);
    modal__box.appendChild(remind);
}
function render_remind_signup() {
    const modal__box = document.querySelector(".modal__box");
    const remind = document.createElement("p");
    const remind_span = document.createElement("span");
    remind.textContent = "還沒有帳戶?";
    remind.className = "remind";
    remind_span.textContent = "點此註冊";
    remind_span.className = "remind_signup_link";
    remind.appendChild(remind_span);
    modal__box.appendChild(remind);
}
function remove_remind() {
    const modal__box = document.querySelector(".modal__box");
    const remind = document.querySelector(".remind");
    modal__box.removeChild(remind);
}
function render_message(m) {
    const modal__box = document.querySelector(".modal__box");
    const message = document.createElement("p");
    message.className = "message";
    message.textContent = m;
    modal__box.appendChild(message);
}
function remove_modal_message() {
    const modal__box = document.querySelector(".modal__box");
    const message = document.querySelector(".message");
    if (message) {
        modal__box.removeChild(message);
    }
}
// controller
function check_current_user() {
    get_user().then((message) => {
        if (message["data"]) {
            render_nav__sign("登出系統");
        } else {
            render_nav__sign("登入/註冊");
        }
    });
}
function switch_sign(which) {
    const signin_content = document.querySelector(".signin");
    const signup_content = document.querySelector(".signup");
    if (which == "signin") {
        signin_content.dataset.active = "true";
        signup_content.dataset.active = "";
        render_remind_signup();
        click_to_signup();
        signin();
    } else if (which == "signup") {
        signup_content.dataset.active = "true";
        signin_content.dataset.active = "";
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
            patch_user(email.value, password.value).then((message) => {
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
            post_user(text.value, email.value, password.value).then(
                (message) => {
                    remove_modal_message();
                    if (message["ok"]) {
                        location.reload();
                    } else {
                        render_message(message["message"]);
                    }
                }
            );
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
    delete_user().then(() => {
        location.reload();
    });
}
// main
window.onload = check_current_user();
open_modal();
close_modal();
