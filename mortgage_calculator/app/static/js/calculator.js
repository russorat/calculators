// Move all the JavaScript functions here
// (formatDate, formatDateLong, fireConfetti, setupConfettiTrigger, etc.)

function formatDate(date) {
    return date.toISOString().split('T')[0];  // For table dates: yyyy-MM-dd
}

function formatDateLong(date) {
    return new Intl.DateTimeFormat('en-US', { 
        year: 'numeric', 
        month: 'long'
    }).format(date);  // For summary section: "March 2024"
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function fireConfetti() {
    const duration = 4000;
    const animationEnd = Date.now() + duration;
    const defaults = { 
        startVelocity: 20,
        spread: 360,
        ticks: 100,
        zIndex: 100,
        scalar: 2.0,
        shapes: ['square', 'circle'],
        gravity: 0.8,
    };

    function randomInRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    const interval = setInterval(function() {
        const timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) {
            return clearInterval(interval);
        }

        const particleCount = 100;

        confetti({
            ...defaults,
            particleCount: particleCount,
            origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
            colors: ['#4CAF50', '#FFC107', '#2196F3', '#E91E63', '#9C27B0', '#FFEB3B', '#FF9800'],
        });
        confetti({
            ...defaults,
            particleCount: particleCount,
            origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
            colors: ['#4CAF50', '#FFC107', '#2196F3', '#E91E63', '#9C27B0', '#FFEB3B', '#FF9800'],
        });
        confetti({
            ...defaults,
            particleCount: Math.floor(particleCount / 2),
            origin: { x: randomInRange(0.4, 0.6), y: Math.random() - 0.2 },
            colors: ['#4CAF50', '#FFC107', '#2196F3', '#E91E63', '#9C27B0', '#FFEB3B', '#FF9800'],
        });

    }, 250);
}

function setupConfettiTrigger() {
    const lastRow = document.querySelector('#scheduleBody tr:last-child');
    if (!lastRow) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                fireConfetti();
                observer.disconnect();
            }
        });
    }, {
        threshold: 0.5
    });

    observer.observe(lastRow);
}

function calculatePaymentDates(paymentSchedule, numPayments) {
    const dates = [];
    const startDate = new Date();
    let currentDate = new Date(startDate);

    // Set to the first day of the month for consistency
    currentDate.setDate(1);

    for (let i = 0; i < numPayments; i++) {
        if (paymentSchedule === 'monthly') {
            currentDate = new Date(currentDate.setMonth(currentDate.getMonth() + 1));
        } else {
            currentDate = new Date(currentDate.setDate(currentDate.getDate() + 14));
        }
        dates.push(new Date(currentDate));
    }

    return dates;
}

function getPayoffDateMessage(finalDate) {
    const now = new Date();
    const years = finalDate.getFullYear() - now.getFullYear();
    const months = finalDate.getMonth() - now.getMonth();
    const totalMonths = years * 12 + months;
    
    let message = `Expected Payoff Date: <strong>${formatDateLong(finalDate)}</strong> (${formatDate(finalDate)})`;
    message += `<br>`;
    
    if (totalMonths > 0) {
        const yearsRemaining = Math.floor(totalMonths / 12);
        const monthsRemaining = totalMonths % 12;
        message += `(`;
        if (yearsRemaining > 0) {
            message += `${yearsRemaining} year${yearsRemaining > 1 ? 's' : ''}`;
            if (monthsRemaining > 0) message += ` and `;
        }
        if (monthsRemaining > 0) {
            message += `${monthsRemaining} month${monthsRemaining > 1 ? 's' : ''}`;
        }
        message += ` from now)`;
    }
    
    return message;
}

async function calculateComparison(principal, rate, years, selectedSchedule) {
    // Calculate both payment schedules
    const schedules = ['monthly', 'biweekly'];
    const results = {};

    for (const schedule of schedules) {
        const response = await fetch(
            `/calculate_mortgage?principal=${principal}&rate=${rate}&years=${years}&paymentSchedule=${schedule}`
        );
        const data = await response.json();
        results[schedule] = data.loan_summary;
    }

    // Create comparison HTML
    const comparisonHtml = `
        <div class="comparison">
            <h3>Payment Schedule Comparison</h3>
            
            <div class="payment-option ${selectedSchedule === 'monthly' ? 'selected' : ''}">
                <div class="label">Monthly Payments</div>
                <div>
                    <div>Payment: ${formatCurrency(results.monthly.periodic_payment)}</div>
                    <div>Total Interest: ${formatCurrency(results.monthly.total_interest)}</div>
                    <div>Total Amount: ${formatCurrency(results.monthly.total_amount_paid)}</div>
                </div>
            </div>

            <div class="comparison-arrow">↓</div>

            <div class="payment-option ${selectedSchedule === 'biweekly' ? 'selected' : ''}">
                <div class="label">Bi-weekly Payments</div>
                <div>
                    <div>Payment: ${formatCurrency(results.biweekly.periodic_payment)}</div>
                    <div>Total Interest: ${formatCurrency(results.biweekly.total_interest)}</div>
                    <div>Total Amount: ${formatCurrency(results.biweekly.total_amount_paid)}</div>
                </div>
            </div>

            ${calculateSavings(results.monthly, results.biweekly)}
        </div>
    `;

    return comparisonHtml;
}

function calculateSavings(monthly, biweekly) {
    const interestSavings = monthly.total_interest - biweekly.total_interest;
    const timeSavings = calculateTimeSavings(monthly, biweekly);
    
    return `
        <div style="margin-top: 20px;">
            <div class="savings ${interestSavings > 0 ? 'positive' : 'negative'}">
                ${interestSavings > 0 
                    ? `✓ By choosing bi-weekly payments, you'll save <strong>${formatCurrency(interestSavings)}</strong> in interest!`
                    : `⚠ Monthly payments would save you ${formatCurrency(-interestSavings)} in interest.`
                }
            </div>
            <div style="margin-top: 10px;">
                <div class="savings ${interestSavings > 0 ? 'positive' : 'negative'}">
                    ${timeSavings}
                </div>
            </div>
        </div>
    `;
}

function calculateTimeSavings(monthly, biweekly) {
    const monthlyMonths = monthly.loan_term_years * 12;
    const biweeklyMonths = Math.ceil(biweekly.number_of_payments / 2);
    const monthsDiff = monthlyMonths - biweeklyMonths;
    
    if (monthsDiff > 0) {
        const years = Math.floor(monthsDiff / 12);
        const months = monthsDiff % 12;
        let savings = "You'll pay off your loan <strong>";
        if (years > 0) savings += ` ${years} year${years > 1 ? 's' : ''}`;
        if (months > 0) savings += ` ${months} month${months > 1 ? 's' : ''}`;
        savings += "</strong> sooner with bi-weekly payments!";
        return savings;
    }
    return '';
}

function downloadResults() {
    // Get the table data
    const table = document.querySelector('table');
    const rows = table.querySelectorAll('tr');
    
    // Create CSV content
    let csvContent = '';
    
    // Get headers
    const headers = [];
    rows[0].querySelectorAll('th').forEach(header => {
        headers.push(header.innerText);
    });
    csvContent += headers.join(',') + '\n';
    
    // Get data rows
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.querySelectorAll('td');
        const rowData = [];
        cells.forEach(cell => {
            // Remove any commas from numbers and wrap text in quotes
            let cellText = cell.innerText.replace(/,/g, '');
            // If the cell contains a dollar sign, remove it and any spaces
            if (cellText.includes('$')) {
                cellText = cellText.replace('$', '').trim();
            }
            rowData.push(`"${cellText}"`);
        });
        csvContent += rowData.join(',') + '\n';
    }
    
    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    // Get current date for filename
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0];
    
    // Create filename with loan amount and date
    const loanAmount = document.getElementById('principal').value;
    const formattedLoanAmount = new Intl.NumberFormat('en-US', {
        style: 'decimal',
        maximumFractionDigits: 0
    }).format(loanAmount);
    
    const filename = `mortgage_schedule_${formattedLoanAmount}_${dateStr}.csv`;
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

async function calculateMortgage() {
    const principal = document.getElementById('principal').value;
    const rate = document.getElementById('rate').value;
    const years = document.getElementById('years').value;

    const errorDiv = document.getElementById('error');
    const resultsDiv = document.getElementById('results');
    const downloadButtonContainer = document.getElementById('downloadButtonContainer');

    try {
        const response = await fetch(`/calculate_mortgage?principal=${principal}&rate=${rate}&years=${years}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to calculate mortgage');
        }

        // Calculate payment dates
        const paymentDates = calculatePaymentDates(
            'monthly', // hardcode to monthly
            data.loan_summary.number_of_payments
        );
        const finalPaymentDate = paymentDates[paymentDates.length - 1];

        // Display results
        errorDiv.classList.add('hidden');
        resultsDiv.classList.remove('hidden');
        downloadButtonContainer.classList.remove('hidden');

        // Update summary
        const summary = document.getElementById('summary');
        summary.innerHTML = `
            <h3>Loan Summary</h3>
            <p>Loan Amount: ${formatCurrency(data.loan_summary.loan_amount)}</p>
            <p>Annual Interest Rate: ${data.loan_summary.annual_interest_rate}%</p>
            <p>Loan Term: ${data.loan_summary.loan_term_years} years</p>
            <p>Monthly Payment: ${formatCurrency(data.loan_summary.periodic_payment)}</p>
            <p>Number of Payments: ${data.loan_summary.number_of_payments}</p>
            <p>Total Interest: ${formatCurrency(data.loan_summary.total_interest)}</p>
            <p>Total Amount Paid: ${formatCurrency(data.loan_summary.total_amount_paid)}</p>
            <div class="payoff-date">
                ${getPayoffDateMessage(finalPaymentDate)}
            </div>
        `;

        // Add comparison section
        const comparisonHtml = await calculateComparison(principal, rate, years, 'monthly');
        summary.innerHTML += comparisonHtml;

        // Update schedule
        const scheduleBody = document.getElementById('scheduleBody');
        scheduleBody.innerHTML = data.amortization_schedule.map((payment, index) => `
            <tr>
                <td>${payment.payment_number}</td>
                <td>${formatDate(paymentDates[index])}</td>
                <td>${formatCurrency(payment.payment_amount)}</td>
                <td>${formatCurrency(payment.principal_payment)}</td>
                <td>${formatCurrency(payment.interest_payment)}</td>
                <td>${formatCurrency(payment.remaining_balance)}</td>
            </tr>
        `).join('');

        // Setup the confetti trigger after the table is populated
        setupConfettiTrigger();

    } catch (error) {
        errorDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        downloadButtonContainer.classList.add('hidden');
        errorDiv.textContent = error.message;
    }
}

// Initialize date handling for the payment dates
document.addEventListener('DOMContentLoaded', function() {
    const tableHeaders = document.querySelector('thead tr');
    if (tableHeaders) {
        tableHeaders.innerHTML = `
            <th>Payment #</th>
            <th>Payment Date</th>
            <th>Payment Amount</th>
            <th>Principal</th>
            <th>Interest</th>
            <th>Remaining Balance</th>
        `;
    }
});

// ... rest of your JavaScript functions ...
