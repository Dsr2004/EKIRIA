function show(id) {
    let input = document.getElementById("password"+id)
    let show = document.getElementById("show"+id)
    let hide = document.getElementById("hide"+id)
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