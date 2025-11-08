let selectedFile = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('resumeFile');
const fileInfo = document.getElementById('fileInfo');
const analyzeBtn = document.getElementById('analyzeBtn');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    if (file.type !== 'application/pdf') {
        alert('Please upload a PDF file only');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }

    selectedFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.classList.remove('hidden');
    analyzeBtn.classList.remove('hidden');
    uploadArea.style.display = 'none';
}

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.classList.add('hidden');
    analyzeBtn.classList.add('hidden');
    uploadArea.style.display = 'block';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

async function analyzeResume() {
    if (!selectedFile) {
        alert('Please select a file first');
        return;
    }

    const loading = document.getElementById('loading');
    const originalBtnText = analyzeBtn.innerHTML;
    
    loading.classList.remove('hidden');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span>Processing...</span>';

    try {
        const formData = new FormData();
        formData.append('resume', selectedFile);

        const response = await fetch('/api/parse-resume', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            // Show the actual error message from server
            const errorMsg = result.error || 'Failed to parse resume';
            alert(`Error: ${errorMsg}`);
            loading.classList.add('hidden');
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = originalBtnText;
            return;
        }
        
        // Check if result has error field (even with 200 status)
        if (result.error) {
            alert(`Error: ${result.error}`);
            loading.classList.add('hidden');
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = originalBtnText;
            return;
        }
        
        // Store results and redirect
        sessionStorage.setItem('recommendations', JSON.stringify(result));
        window.location.href = '/results';
    } catch (error) {
        console.error('Error:', error);
        alert(`Error analyzing resume: ${error.message || 'Please try again.'}`);
        loading.classList.add('hidden');
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = originalBtnText;
    }
}

