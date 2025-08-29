// BYTEME - AI TikTok Analyzer Web App
class BYTEMEAnalyzer {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentAnalysis = null;
    }

    initializeElements() {
        // Input elements
        this.urlInput = document.getElementById('tiktokUrl');
        this.descriptionInput = document.getElementById('videoDescription');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        
        // Section elements
        this.inputSection = document.querySelector('.input-section');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        
        // Loading elements
        this.loadingSteps = document.querySelectorAll('.loading-steps .step');
        
        // Results elements
        this.videoTitle = document.getElementById('videoTitle');
        this.videoDesc = document.getElementById('videoDesc');
        this.averageScore = document.getElementById('averageScore');
        this.tierText = document.getElementById('tierText');
        this.tierBadge = document.getElementById('tierBadge');
        this.adviceContent = document.getElementById('adviceContent');
        
        // Score elements
        this.scoreElements = {
            accuracy: {
                score: document.getElementById('accuracyScore'),
                progress: document.getElementById('accuracyProgress')
            },
            homogeneity: {
                score: document.getElementById('homogeneityScore'),
                progress: document.getElementById('homogeneityProgress')
            },
            comedy: {
                score: document.getElementById('comedyScore'),
                progress: document.getElementById('comedyProgress')
            },
            theatrism: {
                score: document.getElementById('theatrismScore'),
                progress: document.getElementById('theatrismProgress')
            },
            coherence: {
                score: document.getElementById('coherenceScore'),
                progress: document.getElementById('coherenceProgress')
            }
        };
        
        // Buttons
        this.newAnalysisBtn = document.getElementById('newAnalysisBtn');
        this.retryBtn = document.getElementById('retryBtn');
        this.errorMessage = document.getElementById('errorMessage');
    }

    bindEvents() {
        this.analyzeBtn.addEventListener('click', () => this.analyzeVideo());
        this.newAnalysisBtn.addEventListener('click', () => this.resetToInput());
        this.retryBtn.addEventListener('click', () => this.analyzeVideo());
        
        // Enter key support
        this.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.analyzeVideo();
        });
        
        this.descriptionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) this.analyzeVideo();
        });
    }

    async analyzeVideo() {
        const url = this.urlInput.value.trim();
        const description = this.descriptionInput.value.trim();
        
        if (!url) {
            this.showError('Please enter a TikTok URL');
            return;
        }
        
        if (!this.isValidTikTokUrl(url)) {
            this.showError('Please enter a valid TikTok URL');
            return;
        }
        
        this.showLoading();
        this.startLoadingAnimation();
        
        try {
            // Simulate API call to your Python backend
            const result = await this.callAnalysisAPI(url, description);
            this.currentAnalysis = result;
            this.displayResults(result);
        } catch (error) {
            console.error('Analysis failed:', error);
            this.showError(error.message || 'Analysis failed. Please try again.');
        }
    }

    async callAnalysisAPI(url, description) {
        // Make the actual API call to your Python backend
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, description })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Analysis failed');
        }
        
        return await response.json();
    }

    generateMockAnalysis(url, description) {
        // Generate realistic mock data based on your AI model's output format
        const baseScores = {
            accuracy: Math.floor(Math.random() * 4) + 6, // 6-9
            homogeneity: Math.floor(Math.random() * 4) + 5, // 5-8
            comedy: Math.floor(Math.random() * 5) + 4, // 4-8
            theatrism: Math.floor(Math.random() * 4) + 6, // 6-9
            coherence: Math.floor(Math.random() * 3) + 7 // 7-9
        };
        
        // Add some randomization for realism
        const scores = {};
        Object.keys(baseScores).forEach(metric => {
            scores[metric] = Math.max(1, Math.min(10, baseScores[metric] + (Math.random() - 0.5) * 2));
        });
        
        const averageScore = Object.values(scores).reduce((a, b) => a + b, 0) / 5;
        
        return {
            url: url,
            description: description || 'TikTok video analysis',
            scores: scores,
            averageScore: averageScore,
            tier: this.getRewardTier(averageScore),
            advice: this.generateAdvice(scores)
        };
    }

    getRewardTier(averageScore) {
        if (averageScore >= 8) return 'Diamond';
        if (averageScore >= 6) return 'Gold';
        if (averageScore >= 4) return 'Silver';
        return 'Bronze';
    }

    generateAdvice(scores) {
        const advice = [];
        const lowestScore = Math.min(...Object.values(scores));
        const lowestMetric = Object.keys(scores).find(key => scores[key] === lowestScore);
        
        const adviceMap = {
            accuracy: 'Focus on fact-checking and providing accurate information. Consider adding sources or citations.',
            homogeneity: 'Work on creating a more consistent narrative structure. Ensure your content flows logically from start to finish.',
            comedy: 'Try incorporating more humor elements. Consider timing, delivery, and relatable content that resonates with your audience.',
            theatrism: 'Enhance your performance skills. Work on facial expressions, body language, and engaging delivery.',
            coherence: 'Improve the logical flow of your content. Make sure each part connects well with the next.'
        };
        
        advice.push(adviceMap[lowestMetric] || 'Great job overall! Keep creating engaging content.');
        
        if (averageScore < 7) {
            advice.push('Consider spending more time on pre-production planning to improve overall quality.');
        }
        
        return advice.join(' ');
    }

    startLoadingAnimation() {
        let currentStep = 0;
        const stepInterval = setInterval(() => {
            if (currentStep < this.loadingSteps.length) {
                this.loadingSteps[currentStep].classList.add('active');
                currentStep++;
            } else {
                clearInterval(stepInterval);
            }
        }, 800);
    }

    displayResults(result) {
        this.hideAllSections();
        this.resultsSection.classList.remove('hidden');
        
        // Update video info
        this.videoTitle.textContent = 'TikTok Video Analysis';
        this.videoDesc.textContent = result.description;
        
        // Update scores with animation
        Object.keys(this.scoreElements).forEach(metric => {
            const score = Math.round(result.scores[metric]);
            const element = this.scoreElements[metric];
            
            // Animate score
            this.animateNumber(element.score, 0, score, 1000);
            
            // Animate progress bar
            setTimeout(() => {
                element.progress.style.width = `${score * 10}%`;
            }, 200);
        });
        
        // Update average score
        this.animateNumber(this.averageScore, 0, result.averageScore, 1500);
        
        // Update tier
        setTimeout(() => {
            this.tierText.textContent = result.tier;
            this.tierBadge.className = `tier-badge tier-${result.tier.toLowerCase()}`;
        }, 1000);
        
        // Update advice
        setTimeout(() => {
            this.adviceContent.innerHTML = `<p>${result.advice}</p>`;
        }, 1200);
    }

    animateNumber(element, start, end, duration) {
        const startTime = performance.now();
        const difference = end - start;
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = start + (difference * progress);
            element.textContent = current.toFixed(1);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.textContent = end.toFixed(1);
            }
        };
        
        requestAnimationFrame(animate);
    }

    showLoading() {
        this.hideAllSections();
        this.loadingSection.classList.remove('hidden');
        
        // Reset loading steps
        this.loadingSteps.forEach(step => step.classList.remove('active'));
    }

    showError(message) {
        this.hideAllSections();
        this.errorSection.classList.remove('hidden');
        this.errorMessage.textContent = message;
    }

    resetToInput() {
        this.hideAllSections();
        this.inputSection.classList.remove('hidden');
        
        // Clear inputs
        this.urlInput.value = '';
        this.descriptionInput.value = '';
        this.urlInput.focus();
    }

    hideAllSections() {
        this.inputSection.classList.add('hidden');
        this.loadingSection.classList.add('hidden');
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
    }

    isValidTikTokUrl(url) {
        return url.includes('tiktok.com') && url.includes('/video/');
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BYTEMEAnalyzer();
});

// Add some additional CSS for tier badges
const style = document.createElement('style');
style.textContent = `
    .tier-diamond {
        background: linear-gradient(135deg, #b9f2ff 0%, #e3f2fd 100%) !important;
        color: #1976d2 !important;
        border: 2px solid #64b5f6;
    }
    
    .tier-gold {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%) !important;
        color: #f57c00 !important;
        border: 2px solid #ffb74d;
    }
    
    .tier-silver {
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%) !important;
        color: #616161 !important;
        border: 2px solid #bdbdbd;
    }
    
    .tier-bronze {
        background: linear-gradient(135deg, #efebe9 0%, #d7ccc8 100%) !important;
        color: #8d6e63 !important;
        border: 2px solid #a1887f;
    }
`;
document.head.appendChild(style);
