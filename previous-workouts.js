document.addEventListener('DOMContentLoaded', function () {
    fetch('http://127.0.0.1:5000/workoutperformance')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#performance-table tbody');
            data.forEach(performance => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${performance.Name}</td>
                    <td>${performance.Equipment}</td>
                    <td>${performance.Weight}</td>
                    <td>${performance.Reps}</td>
                    <td>${performance.RIR}</td>
                    <td>${performance.Set_Number}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching exercise data:', error));
});