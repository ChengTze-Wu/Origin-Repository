// model
async function get_attraction_by_path(path) {
    const response = await fetch("/api" + path);
    const json_data = await response.json();
    return json_data.data;
}
// view
function render_price(choose_price) {
    const price = document.querySelector(".price");
    price.textContent = choose_price;
}
function render_images_on_carousel(images) {
    const slides = document.querySelector(".slides");
    const circles = document.querySelector(".circles");
    images.forEach((image) => {
        // slide
        const slide = document.createElement("li");
        const img = document.createElement("img");
        slide.className = "slide";
        img.className = "slide__image";
        img.src = image;
        slide.appendChild(img);
        slides.appendChild(slide);
        // circle
        const circle = document.createElement("li");
        circle.className = "circle";
        circles.appendChild(circle);
    });
    // first slide
    const first_slide = slides.querySelector(".slide");
    first_slide.classList.add("active");
    // first circle
    const first_circle = circles.querySelector(".circle");
    const circle_active = document.createElement("div");
    circle_active.className = "circle-active";
    first_circle.appendChild(circle_active);
}
function render_attraction_on_page(
    name,
    category,
    description,
    address,
    transport,
    mrt
) {
    const attraction__title = document.querySelector(".attraction__title");
    const attraction__category = document.querySelector(
        ".attraction__category"
    );
    const attraction__mrt = document.querySelector(".attraction__mrt");
    const attraction__description = document.querySelector(
        ".attraction__description"
    );
    const attraction__address = document.querySelector(".attraction__address");
    const attraction__transport = document.querySelector(
        ".attraction__transport"
    );
    attraction__title.textContent = name;
    attraction__category.textContent = category;
    attraction__mrt.textContent = mrt;
    attraction__description.textContent = description;
    attraction__address.textContent = address;
    attraction__transport.textContent = transport;
}
// controller
function choose_time() {
    const inputs = document.querySelectorAll(".input__time");
    inputs.forEach((input) => {
        input.addEventListener("click", () => {
            render_price(input.value);
        });
    });
}
function hit_button() {
    const buttons = document.querySelectorAll(".carousel__button");
    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            // slide
            const shift = button.classList.contains("next") ? 1 : -1;
            const slides = document.querySelector(".slides");
            const current_slide = slides.querySelector(".active");
            // circle
            const circles = document.querySelector(".circles");
            const circle_active = document.querySelector(".circle-active");

            let current_index = [...slides.children].indexOf(current_slide);
            let next_index = current_index + shift;

            if (next_index < 0) {
                next_index = slides.children.length - 1;
            } else if (next_index >= slides.children.length) {
                next_index = 0;
            }

            slides.children[next_index].classList.add("active");
            current_slide.classList.remove("active");

            circles.children[current_index].removeChild(circle_active);
            circles.children[next_index].appendChild(circle_active);
        });
    });
}
function get_path() {
    const pathname = location.pathname;
    return pathname;
}
function init_load() {
    const path = get_path();
    get_attraction_by_path(path).then((data) => {
        const name = data.name;
        const category = data.category;
        const description = data.description;
        const address = data.address;
        const transport = data.transport;
        const mrt = data.mrt;
        const images = data.images;

        render_attraction_on_page(
            name,
            category,
            description,
            address,
            transport,
            mrt
        );

        render_images_on_carousel(images);

        hit_button();
    });
}
// execute
init_load();
choose_time();
