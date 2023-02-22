window.onload = function() {
    const confirmCheck = document.querySelector("#confirm-check");
    const deleteButton = document.querySelector("#delete-button");

    deleteButton.disabled = true;

    confirmCheck.addEventListener("change", () => {
        deleteButton.disabled = !confirmCheck.checked;
    });
};