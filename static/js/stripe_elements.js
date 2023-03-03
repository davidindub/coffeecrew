// Following documentation from https://stripe.com/docs/js/


let stripePublicKey = document.querySelector("#id_stripe_public_key").textContent.slice(1,-1);
let clientSecret = document.querySelector("#id_client_secret").textContent.slice(1,-1);

let userEmail = document.querySelector("#user_email").textContent.slice(1,-1);

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
  
let elements = stripe.elements({clientSecret: `${clientSecret}`, appearance});

const paymentElementOptions = {
    layout: "tabs",
    defaultValues: {
        billingDetails: {
          email: userEmail,
        },
      },
  };

const paymentElement = elements.create("payment", paymentElementOptions);

paymentElement.mount("#payment-element");

async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
  
    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        // Make sure to change this to your payment completion page
        return_url: "https://8000-davidindub-coffeecrew-xg0tkqn403e.ws-eu89.gitpod.io/checkout/payment",
        receipt_email: emailAddress,
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
  
    const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
  
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