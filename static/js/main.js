// Role selector functionality
document.addEventListener('DOMContentLoaded', function() {
    const roleBtns = document.querySelectorAll('.role-btn');
    const roleInput = document.getElementById('role');
    
    if (roleBtns.length > 0 && roleInput) {
        roleBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                roleBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                roleInput.value = this.getAttribute('data-role');
            });
        });
    }
    
    // Name validation - only letters and spaces
    const nameInput = document.getElementById('nameInput');
    if (nameInput) {
        nameInput.addEventListener('input', function(e) {
            // Remove any non-letter and non-space characters
            this.value = this.value.replace(/[^A-Za-z\s]/g, '');
        });
        
        nameInput.addEventListener('keypress', function(e) {
            // Prevent typing numbers and special characters
            const char = String.fromCharCode(e.which);
            if (!/[A-Za-z\s]/.test(char)) {
                e.preventDefault();
            }
        });
    }
});

// Modal functions
function showJobModal() {
    const modal = document.getElementById('jobModal');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeJobModal() {
    const modal = document.getElementById('jobModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal on outside click
window.addEventListener('click', function(e) {
    const modal = document.getElementById('jobModal');
    if (modal && e.target === modal) {
        closeJobModal();
    }
});


// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('mediaFiles');
    const filePreview = document.getElementById('filePreview');
    const problemForm = document.getElementById('problemForm');
    
    if (uploadArea && fileInput) {
        // Click to upload
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#4f46e5';
            uploadArea.style.background = '#eef2ff';
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = '#d1d5db';
            uploadArea.style.background = 'white';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#d1d5db';
            uploadArea.style.background = 'white';
            
            const files = e.dataTransfer.files;
            handleFiles(files);
        });
        
        // File input change
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
    }
    
    // Handle form submission
    if (problemForm) {
        problemForm.addEventListener('submit', function(e) {
            e.preventDefault();
            analyzeProblems();
        });
    }
});

function handleFiles(files) {
    const filePreview = document.getElementById('filePreview');
    filePreview.innerHTML = '';
    
    Array.from(files).forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            fileItem.appendChild(img);
        } else if (file.type.startsWith('video/')) {
            const video = document.createElement('video');
            video.src = URL.createObjectURL(file);
            video.controls = false;
            fileItem.appendChild(video);
        }
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'file-remove';
        removeBtn.innerHTML = '×';
        removeBtn.onclick = () => fileItem.remove();
        fileItem.appendChild(removeBtn);
        
        filePreview.appendChild(fileItem);
    });
}

function analyzeProblems() {
    const form = document.getElementById('problemForm');
    const description = form.querySelector('[name="problem_description"]').value;
    const category = form.querySelector('[name="category"]').value;
    const urgency = form.querySelector('[name="urgency"]:checked').value;
    
    // Show loading state
    const btn = form.querySelector('.btn-analyze');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    btn.disabled = true;
    
    // Simulate AI analysis (in real app, this would be an API call)
    setTimeout(() => {
        // Detect category from description if not provided
        let detectedCategory = category;
        if (!detectedCategory) {
            const keywords = {
                'Plumbing': ['leak', 'pipe', 'water', 'sink', 'faucet', 'drain', 'toilet'],
                'Electrical': ['wire', 'outlet', 'light', 'switch', 'power', 'electric'],
                'Carpentry': ['wood', 'door', 'cabinet', 'furniture', 'shelf'],
                'Cleaning': ['clean', 'dirt', 'stain', 'mess'],
                'HVAC': ['heat', 'cool', 'air', 'temperature', 'ac', 'furnace'],
                'Painting': ['paint', 'wall', 'color']
            };
            
            for (const [cat, words] of Object.entries(keywords)) {
                if (words.some(word => description.toLowerCase().includes(word))) {
                    detectedCategory = cat;
                    break;
                }
            }
            detectedCategory = detectedCategory || 'General Repair';
        }
        
        // Mock worker recommendations
        const workers = [
            { name: 'Sarah Miller', skills: 'Plumbing Expert', avatar: 'https://picsum.photos/seed/sarah/100', match: 98 },
            { name: 'Marcus Chen', skills: 'Electrical Specialist', avatar: 'https://picsum.photos/seed/marcus/100', match: 95 },
            { name: 'Elena Rodriguez', skills: 'General Repairs', avatar: 'https://picsum.photos/seed/elena/100', match: 92 }
        ];
        
        // Filter workers based on category
        const relevantWorkers = workers.filter(w => 
            w.skills.toLowerCase().includes(detectedCategory.toLowerCase()) || 
            detectedCategory === 'General Repair'
        );
        
        // Show results
        displayResults(description, detectedCategory, relevantWorkers.length > 0 ? relevantWorkers : workers);
        
        // Reset button
        btn.innerHTML = originalText;
        btn.disabled = false;
        
        // Hide form, show results
        form.style.display = 'none';
        document.getElementById('analysisResult').style.display = 'block';
    }, 2000);
}

function displayResults(description, category, workers) {
    document.getElementById('detectedIssue').textContent = 
        `${category} issue: ${description.substring(0, 100)}${description.length > 100 ? '...' : ''}`;
    
    const workersList = document.getElementById('workersList');
    workersList.innerHTML = workers.map(worker => `
        <div class="worker-recommendation">
            <img src="${worker.avatar}" alt="${worker.name}">
            <div class="worker-info">
                <p class="name">${worker.name}</p>
                <p class="skills">${worker.skills}</p>
            </div>
            <div class="match-score">
                <p class="score">${worker.match}%</p>
                <p class="label">Match</p>
            </div>
        </div>
    `).join('');
}

function createJobFromAnalysis() {
    // In real app, this would create a job with the analyzed data
    alert('Job request created! Redirecting to dashboard...');
    window.location.href = '/dashboard/';
}


// Report Issue File Upload
document.addEventListener('DOMContentLoaded', function() {
    const issueUploadArea = document.getElementById('issueUploadArea');
    const issueFileInput = document.getElementById('issueFiles');
    const issueFilePreview = document.getElementById('issueFilePreview');
    
    if (issueUploadArea && issueFileInput) {
        issueUploadArea.addEventListener('click', () => issueFileInput.click());
        
        issueUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            issueUploadArea.style.borderColor = '#4f46e5';
            issueUploadArea.style.background = '#eef2ff';
        });
        
        issueUploadArea.addEventListener('dragleave', () => {
            issueUploadArea.style.borderColor = '#d1d5db';
            issueUploadArea.style.background = 'white';
        });
        
        issueUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            issueUploadArea.style.borderColor = '#d1d5db';
            issueUploadArea.style.background = 'white';
            
            const files = e.dataTransfer.files;
            handleIssueFiles(files);
        });
        
        issueFileInput.addEventListener('change', (e) => {
            handleIssueFiles(e.target.files);
        });
    }
});

function handleIssueFiles(files) {
    const issueFilePreview = document.getElementById('issueFilePreview');
    issueFilePreview.innerHTML = '';
    
    Array.from(files).forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            fileItem.appendChild(img);
        } else if (file.type.startsWith('video/')) {
            const video = document.createElement('video');
            video.src = URL.createObjectURL(file);
            video.controls = false;
            fileItem.appendChild(video);
        }
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'file-remove';
        removeBtn.innerHTML = '×';
        removeBtn.type = 'button';
        removeBtn.onclick = () => fileItem.remove();
        fileItem.appendChild(removeBtn);
        
        issueFilePreview.appendChild(fileItem);
    });
}
