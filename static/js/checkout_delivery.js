const countryDropdown = document.querySelector("#id_country");
const deliveryOptionNone = document.querySelector("#delivery-option-none");
const deliveryOptionIE = document.querySelector("#delivery-option-ie");
const deliveryOptionEU = document.querySelector("#delivery-option-eu");
const fullName = document.querySelector("#fullName").textContent.slice(1, -1);
const addressLine1 = document.querySelector("#addressLine1").textContent.slice(1, -1);
const addressLine2 = document.querySelector("#addressLine2").textContent.slice(1, -1);
const addressCity = document.querySelector("#addressCity").textContent.slice(1, -1);
const addressPostcode = document.querySelector("#addressPostcode").textContent.slice(1, -1);
const addressCountry = document.querySelector("#addressCountry").textContent.slice(1, -1);

function updateDeliveryOptions(country) {
    if (!country) {
        deliveryOptionNone.style.display = "block";
        deliveryOptionIE.style.display = "none";
        deliveryOptionEU.style.display = "none";
    } else if (country == "IE") {
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

countryDropdown.addEventListener("change", function () {
    updateDeliveryOptions(countryDropdown.value);
});


// Add event listener to checkbox
const checkbox = document.getElementById("use_default_delivery_address");
checkbox.addEventListener("change", function () {
    // If checkbox is checked, use default shipping address
    if (this.checked) {
        document.querySelector("#id_full_name").value = fullName;
        document.querySelector("#id_address_line_1").value = addressLine1;
        document.querySelector("#id_address_line_2").value = addressLine2;
        document.querySelector("#id_city").value = addressCity;
        document.querySelector("#id_postcode").value = addressPostcode;
        document.querySelector("#id_country").value = addressCity;

        for (let option of document.querySelector("#id_country").options)
        {
        if (option.value === addressCountry)
        {
            option.selected = true;
            console.log(addressCountry);
            updateDeliveryOptions(addressCountry);
            return;
        }
        }
    }
    // If checkbox is unchecked clear the form
    else {
        document.querySelector("#id_full_name").value = null;
        document.querySelector("#id_address_line_1").value = null;
        document.querySelector("#id_address_line_2").value = null;
        document.querySelector("#id_city").value = null;
        document.querySelector("#id_postcode").value = null;
        document.querySelector("#id_country").value = null;
        updateDeliveryOptions("");
    }
});