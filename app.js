let currentWorkoutId = null; 
let currentExerciseId = null;

function startWorkout() {
    document.getElementById('workout-screen').style.display = 'block';
    document.getElementById('exercise-container').style.display = 'none';
    // Redirect to the "Start Workout" page or section
    fetch('http://127.0.0.1:5000/start-workout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        currentWorkoutId = data.WorkoutID
    })
    .catch(error => console.error('Error', error));
    //window.location.href = 'start-workout.html'; // Or open a form in a modal
}

function goToWorkout() {
    window.location.href = 'workout-entry.html';
}

function loadExercises() {
    fetch('http://127.0.0.1:5000/exercises')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('exercise-select');
            select.innerHTML = '<option value="">Select an Exercise</option>'; // Reset dropdown options

            // Populate dropdown
            data.forEach(exercise => {
                console.log("Loaded Exercise:", exercise); // Log exercise data for debugging
                const option = document.createElement('option');
                option.value = exercise.ExerciseID;
                option.textContent = exercise.Name;
                select.appendChild(option);
            });

            // Event listener to set currentExerciseId when an exercise is selected
            select.addEventListener("change", function() {
                const selectedExerciseId = select.value; // Fetch selected ExerciseID
                console.log("Selected Exercise ID:", selectedExerciseId); // Log to confirm selection
                if (selectedExerciseId) {
                    currentExerciseId = selectedExerciseId;
                    console.log("Current Exercise ID set to:", currentExerciseId); // Check the global variable
                } else {
                    console.error("No ExerciseID found for the selected option.");
                }
            });
        })
        .catch(error => console.error('Error loading exercises:', error));
}

// Show modal for adding new exercise
function showAddExerciseForm() {
    document.getElementById('add-exercise-modal').style.display = 'block';
}

// Hide modal form
function hideAddExerciseForm() {
    document.getElementById('add-exercise-modal').style.display = 'none';
}

// Function to add a new exercise and refresh the dropdown
function addNewExercise() {
    const exerciseName = document.getElementById('exercise-name').value;
    const bodyPart = document.getElementById('body-part').value;
    const equipment = document.getElementById('equipment').value;

    fetch('http://127.0.0.1:5000/add-or-get-exercise', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ Name: exerciseName, Body_Part: bodyPart, Equipment: equipment })
    })
    .then(response => response.json())
    .then(data => {
        currentExerciseId = data.ExerciseID;
        hideAddExerciseForm();
        loadExercises(); // Reload dropdown with new exercise included
    })
    .catch(error => console.error('Error adding exercise:', error));
}

// Load exercises on page load
window.onload = loadExercises;


function submitWorkoutPerformance(reps, setNumber, rir, weight) {
    if (!currentExerciseId) {
        alert("EAT A DICK");
        return;
    }
    fetch('http://127.0.0.1:5000/submit-workout-performance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            WorkoutID: currentWorkoutId,
            UserID: 1,  // Replace with actual UserID if available
            ExerciseID: currentExerciseId,
            Reps: reps,
            Set_Number: setNumber,
            RIR: rir,
            Weight: weight  // Include weight in the payload
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error("Error:", error));
}



function viewPreviousWorkouts() {
    // Redirect to the "Previous Workouts" page
    window.location.href = 'previous-workouts.html';
}

function viewExerciseList() {
    // Redirect to the "Exercise List" page
    window.location.href = 'exercise-list.html';
}
