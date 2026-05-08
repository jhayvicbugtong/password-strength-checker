const passwordInput = document.getElementById("password");
const toggleBtn = document.querySelector(".toggle-password");

const lengthCheck = document.getElementById("lengthCheck");
const upperCheck = document.getElementById("upperCheck");
const numberCheck = document.getElementById("numberCheck");
const symbolCheck = document.getElementById("symbolCheck");

function togglePassword() {
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleBtn.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        toggleBtn.textContent = "Show";
    }
}

function setCheck(element, isValid, validText, invalidText) {
    if (isValid) {
        element.textContent = "✓ " + validText;
        element.classList.add("valid");
    } else {
        element.textContent = "○ " + invalidText;
        element.classList.remove("valid");
    }
}

passwordInput.addEventListener("input", function () {
    const password = passwordInput.value;

    setCheck(
        lengthCheck,
        password.length >= 8,
        "At least 8 characters",
        "At least 8 characters"
    );

    setCheck(
        upperCheck,
        /[A-Z]/.test(password),
        "Uppercase letter",
        "Uppercase letter"
    );

    setCheck(
        numberCheck,
        /[0-9]/.test(password),
        "Number",
        "Number"
    );

    setCheck(
        symbolCheck,
        /[^A-Za-z0-9]/.test(password),
        "Special character",
        "Special character"
    );
});