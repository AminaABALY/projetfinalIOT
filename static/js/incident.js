<script>
document.getElementById('acquisitionBtn').addEventListener('click', () => {
    const operatorButton = document.querySelector('.operator-choice button.selected');
    if (!operatorButton) {
        alert('Veuillez sélectionner un opérateur.');
        return;
    }

    const operator = operatorButton.textContent;
    const remark = document.getElementById('remark').value.trim();
    const incidentDate = new Date().toISOString();
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/register_incident/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            operator: operator,
            remark: remark,
            incident_date: incidentDate
        })
    }).then(response => {
        if (response.ok) {
            alert("Incident enregistré !");
        } else {
            alert("Erreur lors de l'enregistrement.");
        }
    });
});
</script>
