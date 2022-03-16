// global variable
let temp_page;
let temp_keyword = "";
let fetch_status = false;
let search_input = document.querySelector(".banner__search__input");

// model
async function load_attractions(page, keyword) {
    fetch_status = true;
    let url = "/api/attractions";
    let full_url;
    if (keyword) {
        full_url = url + "?page=" + page + "&keyword=" + keyword;
    } else {
        full_url = url + "?page=" + page;
    }
    let response = await fetch(full_url);
    let json_data = await response.json();
    if (json_data["error"]) {
        render_input_message(keyword);
        temp_page = null;
    } else {
        remove_input_message();
        json_data["data"].forEach((item) => {
            const image = item["images"][0];
            const name = item["name"];
            const mrt = item["mrt"];
            const category = item["category"];
            render_album_item(image, name, mrt, category);
        });
        temp_page = json_data["nextPage"];
    }
}

// view
function render_album_item(image, name, mrt, category) {
    const album = document.querySelector(".album");
    const album__item = document.createElement("div");
    const album__item__image = document.createElement("img");
    const album__item__name = document.createElement("div");
    const album__item__mrt = document.createElement("div");
    const album__item__category = document.createElement("div");
    const name_textNode = document.createTextNode(name);
    const mrt_textNode = document.createTextNode(mrt);
    const category_textNode = document.createTextNode(category);

    album__item.className = "album__item";
    album__item__image.className = "album__item__image";
    album__item__name.className = "album__item__name";
    album__item__mrt.className = "album__item__mrt";
    album__item__category.className = "album__item__category";

    album__item__image.src = image;
    album__item__name.appendChild(name_textNode);
    album__item__mrt.appendChild(mrt_textNode);
    album__item__category.appendChild(category_textNode);

    album__item.appendChild(album__item__image);
    album__item.appendChild(album__item__name);
    album__item.appendChild(album__item__mrt);
    album__item.appendChild(album__item__category);
    album.appendChild(album__item);
}
function render_input_message(keyword) {
    const message = document.querySelector(".banner__search__message");
    message.textContent = "找不到「" + keyword + "」，查無資料。";
}

// controller
function remove_album_items() {
    let album = document.querySelector(".album");
    while (album.hasChildNodes()) {
        album.removeChild(album.firstChild);
    }
}
function remove_input_message() {
    const message = document.querySelector(".banner__search__message");
    message.textContent = "";
}
function render_data_with_scroll(keyword) {
    const callback = (entries) => {
        entries.forEach((e) => {
            if (e.isIntersecting && temp_page && fetch_status == false) {
                load_attractions(temp_page, keyword).then(() => {
                    fetch_status = false;
                });
            }
        });
    };
    const observer = new IntersectionObserver(callback, {
        threshold: 0,
    });
    const target = document.querySelector(".footer");

    observer.observe(target);

    search_input.addEventListener("keyup", () => {
        if (keyword != temp_keyword) {
            observer.unobserve(target);
        }
    });
}

// main execute
load_attractions(0).then(() => {
    fetch_status = false;
    render_data_with_scroll();
});

search_input.addEventListener("keyup", () => {
    let keyword = search_input.value;
    if (keyword.trim() != temp_keyword) {
        temp_keyword = keyword;
        remove_album_items();
        load_attractions(0, keyword).then(() => {
            fetch_status = false;
            render_data_with_scroll(keyword);
        });
    }
});
