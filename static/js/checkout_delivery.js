const countryDropdown = document.getElementById("id_country");
const deliveryOptionNone = document.getElementById("delivery-option-none")
const deliveryOptionIE = document.getElementById("delivery-option-ie")
const deliveryOptionEU = document.getElementById("delivery-option-eu")

function updateDeliveryOptions(country) {
    if (!country) {
        deliveryOptionNone.style.display = "block";
        deliveryOptionIE.style.display = "none";
        deliveryOptionEU.style.display = "none";
    }
    else if (country == "IE") {
        deliveryOptionNone.style.display = "none";
        deliveryOptionIE.style.display = "block";
        deliveryOptionEU.style.display = "none";
    } else {
        deliveryOptionNone.style.display = "none";
        deliveryOptionIE.style.display = "none";
        deliveryOptionEU.style.display = "block";
    }
}

updateDeliveryOptions(countryDropdown.value);

countryDropdown.addEventListener("change", function() {
    updateDeliveryOptions(countryDropdown.value);
});