document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("#logout-button").addEventListener("click", function () {
        document.querySelector(".popup").classList.add("active");
    });

    document.querySelector(".popup .close-btn").addEventListener("click", function () {
        document.querySelector(".popup").classList.remove("active");
    });
    document.querySelector(".popup .modal-options #no-button").addEventListener("click", function () {
        document.querySelector(".popup").classList.remove("active");
    });
});
