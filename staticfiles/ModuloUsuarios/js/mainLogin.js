function show() {
    let input = document.getElementById("password")
    let show = document.getElementById("show")
    let hide = document.getElementById("hide")
    if (input.type === "password") {
        input.type = "text";
        show.style.display = "none"
        hide.style.display = "block"
    } else {
        input.type = "password";
        show.style.display = "block"
        hide.style.display = "none"
    }
}