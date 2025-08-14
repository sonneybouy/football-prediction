class FootballPredictor {
    constructor() {
        this.apiBaseUrl = '/api/v1';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadRecentPredictions();
        this.setDefaultDate();
    }

    bindEvents() {
        const form = document.getElementById('predictionForm');
        form.addEventListener('submit', (e) => this.handlePrediction(e));
        
        // Prevent selecting same team for home and away
        const homeSelect = document.getElementById('homeTeam');
        const awaySelect = document.getElementById('awayTeam');
        
        homeSelect.addEventListener('change', () => this.updateTeamOptions());
        awaySelect.addEventListener('change', () => this.updateTeamOptions());
    }

    setDefaultDate() {
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        document.getElementById('matchDate').value = now.toISOString().slice(0, 16);
    }

    updateTeamOptions() {
        const homeTeam = document.getElementById('homeTeam').value;
        const awayTeam = document.getElementById('awayTeam').value;
        
        // Disable selected teams in opposite dropdown
        const homeOptions = document.querySelectorAll('#homeTeam option');
        const awayOptions = document.querySelectorAll('#awayTeam option');
        
        homeOptions.forEach(option => {
            option.disabled = option.value === awayTeam && option.value !== '';
        });
        
        awayOptions.forEach(option => {
            option.disabled = option.value === homeTeam && option.value !== '';
        });
    }

    async handlePrediction(e) {
        e.preventDefault();
        
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const spinner = document.getElementById('loadingSpinner');
        const resultsCard = document.getElementById('resultsCard');
        
        // Show loading state
        submitBtn.disabled = true;
        spinner.classList.remove('d-none');
        resultsCard.classList.add('d-none');
        
        try {
            const formData = new FormData(e.target);
            const prediction = await this.makePrediction({
                home_team: document.getElementById('homeTeam').value,
                away_team: document.getElementById('awayTeam').value,
                match_date: document.getElementById('matchDate').value,
                league: document.getElementById('league').value || null
            });
            
            this.displayResults(prediction);
            this.addToRecentPredictions(prediction);
            
        } catch (error) {
            console.error('Prediction failed:', error);
            this.showError('Failed to get prediction. Please try again.');
        } finally {
            // Hide loading state
            submitBtn.disabled = false;
            spinner.classList.add('d-none');
        }
    }

    async makePrediction(data) {
        const response = await fetch(`${this.apiBaseUrl}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }

    displayResults(prediction) {
        const resultsCard = document.getElementById('resultsCard');
        
        // Update team names and scores
        document.getElementById('homeTeamResult').textContent = prediction.home_team;
        document.getElementById('awayTeamResult').textContent = prediction.away_team;
        document.getElementById('homeScoreResult').textContent = prediction.predicted_score_home.toFixed(1);
        document.getElementById('awayScoreResult').textContent = prediction.predicted_score_away.toFixed(1);
        
        // Update confidence
        document.getElementById('confidenceResult').textContent = Math.round(prediction.confidence * 100);
        
        // Update probability bars
        this.updateProbabilityBar('homeWinBar', 'homeWinProb', prediction.win_probability_home);
        this.updateProbabilityBar('drawBar', 'drawProb', prediction.draw_probability);
        this.updateProbabilityBar('awayWinBar', 'awayWinProb', prediction.win_probability_away);
        
        // Update metadata
        document.getElementById('modelVersion').textContent = prediction.model_version;
        document.getElementById('predictionTime').textContent = new Date(prediction.prediction_timestamp).toLocaleString();
        
        // Show results with animation
        resultsCard.classList.remove('d-none');
        resultsCard.classList.add('fade-in');
        
        // Scroll to results
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    updateProbabilityBar(barId, textId, probability) {
        const percentage = Math.round(probability * 100);
        document.getElementById(barId).style.width = `${percentage}%`;
        document.getElementById(textId).textContent = `${percentage}%`;
    }

    addToRecentPredictions(prediction) {
        const tbody = document.getElementById('recentPredictions');
        
        // Create new row
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${prediction.home_team} vs ${prediction.away_team}</td>
            <td>${prediction.predicted_score_home.toFixed(1)} - ${prediction.predicted_score_away.toFixed(1)}</td>
            <td>${Math.round(prediction.confidence * 100)}%</td>
            <td>${new Date().toLocaleDateString()}</td>
        `;
        
        // Remove "no predictions" message if it exists
        if (tbody.children.length === 1 && tbody.children[0].cells.length === 1) {
            tbody.innerHTML = '';
        }
        
        // Add new row at the top
        tbody.insertBefore(row, tbody.firstChild);
        
        // Keep only last 5 predictions
        while (tbody.children.length > 5) {
            tbody.removeChild(tbody.lastChild);
        }
        
        // Save to localStorage
        this.saveRecentPrediction(prediction);
    }

    saveRecentPrediction(prediction) {
        const saved = JSON.parse(localStorage.getItem('recentPredictions') || '[]');
        saved.unshift({
            ...prediction,
            timestamp: new Date().toISOString()
        });
        
        // Keep only last 10
        localStorage.setItem('recentPredictions', JSON.stringify(saved.slice(0, 10)));
    }

    loadRecentPredictions() {
        const saved = JSON.parse(localStorage.getItem('recentPredictions') || '[]');
        const tbody = document.getElementById('recentPredictions');
        
        if (saved.length === 0) return;
        
        tbody.innerHTML = '';
        saved.slice(0, 5).forEach(prediction => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${prediction.home_team} vs ${prediction.away_team}</td>
                <td>${prediction.predicted_score_home.toFixed(1)} - ${prediction.predicted_score_away.toFixed(1)}</td>
                <td>${Math.round(prediction.confidence * 100)}%</td>
                <td>${new Date(prediction.timestamp).toLocaleDateString()}</td>
            `;
            tbody.appendChild(row);
        });
    }

    showError(message) {
        // Simple error display - could be enhanced with a proper modal or toast
        alert(message);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FootballPredictor();
});