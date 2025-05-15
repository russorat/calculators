document.getElementById('calculateBtn').addEventListener('click', async () => {
    const value1 = parseFloat(document.getElementById('value1').value);
    const value2 = parseFloat(document.getElementById('value2').value);

    if (isNaN(value1) || isNaN(value2)) {
        alert('Please enter valid numbers');
        return;
    }

    try {
        // Build URL with query parameters
        const url = `/api/percentage-difference?value1=${encodeURIComponent(value1)}&value2=${encodeURIComponent(value2)}`;
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        const data = await response.json();
        
        document.getElementById('results').style.display = 'block';
        document.getElementById('percentageDiff').textContent = `${data.percentage_difference.toFixed(2)}%`;
        
        // Color the result based on whether it's positive or negative
        document.getElementById('percentageDiff').style.color = 
            data.percentage_difference >= 0 ? 'var(--success-color)' : 'var(--error-color)';
        
    } catch (error) {
        alert('Error calculating percentage difference');
        console.error('Error:', error);
    }
});
