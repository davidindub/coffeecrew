/* jshint esversion: 11 */
// Following documentation from https://stripe.com/docs/js/


const stripePublicKey = document.querySelector("#id_stripe_public_key").textContent.slice(1, -1);
const clientSecret = document.querySelector("#id_client_secret").textContent.slice(1, -1);

const stripeReturnURL = document.querySelector("#stripeReturnURL").textContent.slice(1, -1);
const userEmail = document.querySelector("#user_email").textContent.slice(1, -1);
const fullName = document.querySelector("#fullName").textContent.slice(1, -1);
const addressLine1 = document.querySelector("#addressLine1").textContent.slice(1, -1);
const addressLine2 = document.querySelector("#addressLine2").textContent.slice(1, -1);
const addressCity = document.querySelector("#addressCity").textContent.slice(1, -1);
const addressPostcode = document.querySelector("#addressPostcode").textContent.slice(1, -1);
const addressCountry = document.querySelector("#addressCountry").textContent.slice(1, -1);

const stripe = Stripe(stripePublicKey);

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);

const appearance = {
  theme: "stripe",
  variables: {
    colorPrimary: "#0f4a3b",
    colorText: "#0f4a3b",
  },
};

let elements = stripe.elements({
  clientSecret: `${clientSecret}`,
  appearance
});

// Passing in the email is required for this integration. The other fields are optional.
// This is useful if you want to prefill consumer information to ease consumer experience.
const paymentElement = elements.create('payment', {
  defaultValues: {
    billingDetails: {
      email: userEmail,
      name: fullName,
    },
  },
});

// Mount the Elements to their corresponding DOM node
paymentElement.mount("#payment-element");

const addressElement = elements.create("address", {
  mode: "billing",
  defaultValues: {
    name: fullName,
    address: {
      line1: addressLine1,
      line2: addressLine2,
      city: addressCity,
      postal_code: addressPostcode,
      country: addressCountry,
    },
  },
});
addressElement.mount("#address-element");

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);

  const {
    error
  } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      return_url: stripeReturnURL,
      receipt_email: userEmail,
    },
  });

  // This point will only be reached if there is an immediate error when
  // confirming the payment. Otherwise, your customer will be redirected to
  // your `return_url`. For some payment methods like iDEAL, your customer will
  // be redirected to an intermediate site first to authorize the payment, then
  // redirected to the `return_url`.
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred.");
  }

  setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );

  if (!clientSecret) {
    return;
  }

  const {
    paymentIntent
  } = await stripe.retrievePaymentIntent(clientSecret);

  switch (paymentIntent.status) {
    case "succeeded":
      showMessage("Payment succeeded!");
      break;
    case "processing":
      showMessage("Your payment is processing.");
      break;
    case "requires_payment_method":
      showMessage("Your payment was not successful, please try again.");
      break;
    default:
      showMessage("Something went wrong.");
      break;
  }
}

// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageText.textContent = "";
  }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}