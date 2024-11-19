// Theme Toggle
function changeTheme() {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
}

// Modal Open/Close
function createAccount() {
    document.getElementById('signUpModal').style.display = 'block';
}

function logIn() {
    document.getElementById('logInModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Sign-Up Logic
async function submitSignUp() {
    const name = document.getElementById('signUpUsername').value;

    const response = await fetch('http://localhost:5000/sign-up', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ Name: name })
    });

    const result = await response.json();
    alert(result.message);
    closeModal('signUpModal');
}

// Log-In Logic
async function submitLogIn() {
    const name = document.getElementById('logInUsername').value;

    const response = await fetch('http://localhost:5000/log-in', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ Name: name })
    });

    const result = await response.json();
    if (response.ok) {
        alert(result.message);
    } else {
        alert("Login failed");
    }
    closeModal('logInModal');
}

// Close Modals if clicked outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}
