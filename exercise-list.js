document.addEventListener('DOMContentLoaded', function () {
    fetch('http://127.0.0.1:5000/exercises')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#exercise-table tbody');
            data.forEach(exercise => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${exercise.Name}</td>
                    <td>${exercise.Body_Part}</td>
                    <td>${exercise.Equipment}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching exercise data:', error));
});