document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const uploadTab = document.querySelector('[data-tab="upload"]');
    const cameraTab = document.querySelector('[data-tab="camera"]');
    const uploadTabContent = document.getElementById('upload-tab');
    const cameraTabContent = document.getElementById('camera-tab');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const startCameraBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-btn');
    const retryBtn = document.getElementById('retry-btn');
    const videoElement = document.getElementById('camera-feed');
    const canvasElement = document.getElementById('camera-canvas');
    const resultsContainer = document.getElementById('results');
    const analyzedImage = document.getElementById('analyzed-image');
    const genderResult = document.getElementById('gender-result');
    const confidenceValue = document.getElementById('confidence-value');
    const featuresDetected = document.getElementById('features-detected');

    // Tab Switching
    uploadTab.addEventListener('click', () => switchTab('upload'));
    cameraTab.addEventListener('click', () => switchTab('camera'));

    function switchTab(tabName) {
        // Update active tab
        uploadTab.classList.remove('active');
        cameraTab.classList.remove('active');
        uploadTabContent.classList.remove('active');
        cameraTabContent.classList.remove('active');

        if (tabName === 'upload') {
            uploadTab.classList.add('active');
            uploadTabContent.classList.add('active');
            stopCamera(); // Ensure camera is stopped when switching tabs
        } else {
            cameraTab.classList.add('active');
            cameraTabContent.classList.add('active');
        }
    }

    // File Upload Handling
    browseBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and Drop Handling
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('highlight');
    }

    function unhighlight() {
        dropZone.classList.remove('highlight');
    }

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            handleFiles(files);
        }
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        if (files.length) {
            handleFiles(files);
        }
    }

    function handleFiles(files) {
        const file = files[0];
        if (file.type.match('image.*')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                analyzeImage(e.target.result);
            };
            reader.readAsDataURL(file);
        } else {
            alert('Please select an image file (JPEG, PNG)');
        }
    }

    // Camera Handling
    startCameraBtn.addEventListener('click', startCamera);
    captureBtn.addEventListener('click', captureImage);
    retryBtn.addEventListener('click', resetCameraFlow);

    let stream = null;

    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                },
                audio: false
            });
            videoElement.srcObject = stream;
            startCameraBtn.disabled = true;
            captureBtn.disabled = false;
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Could not access the camera. Please ensure you have granted camera permissions.');
        }
    }

    function captureImage() {
        // Set canvas dimensions to match video
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        
        // Draw video frame to canvas
        const context = canvasElement.getContext('2d');
        context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
        
        // Stop camera
        stopCamera();
        
        // Get image data and analyze
        const imageData = canvasElement.toDataURL('image/jpeg');
        analyzeImage(imageData);
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            videoElement.srcObject = null;
            stream = null;
        }
        startCameraBtn.disabled = false;
        captureBtn.disabled = true;
    }

    function resetCameraFlow() {
        stopCamera();
        resultsContainer.style.display = 'none';
        canvasElement.style.display = 'none';
        videoElement.style.display = 'block';
        retryBtn.disabled = true;
    }

    // Image Analysis (Simulated - replace with actual API call)
    function analyzeImage(imageData) {
        // Show loading state
        resultsContainer.style.display = 'block';
        resultsContainer.innerHTML = `
            <div class="loading" style="padding: 20px; text-align: center;">
                <div class="spinner"></div>
                <p>Analyzing image...</p>
            </div>
        `;

        // Hide video/camera elements
        videoElement.style.display = 'none';
        canvasElement.style.display = 'none';
        retryBtn.disabled = false;

        // Simulate API processing delay
        setTimeout(() => {
            // This is simulated data - in a real app you'd call your gender detection API
            const isMale = Math.random() > 0.5;
            const confidence = (Math.random() * 20 + 80).toFixed(1); // Random confidence 80-100%
            const features = isMale 
                ? ['Square jawline', 'Prominent brow ridge', 'Thicker eyebrows']
                : ['Rounder face shape', 'Softer jawline', 'Higher cheekbones'];

            // Display results
            analyzedImage.src = imageData;
            genderResult.textContent = isMale ? 'Male' : 'Female';
            genderResult.className = 'gender-display ' + (isMale ? 'male' : 'female');
            confidenceValue.textContent = confidence;
            
            // Update features list
            featuresDetected.innerHTML = '';
            features.forEach(feature => {
                const li = document.createElement('li');
                li.textContent = feature;
                featuresDetected.appendChild(li);
            });

            // Show full results
            resultsContainer.innerHTML = `
                <div class="result-header">
                    <h3>Analysis Results</h3>
                    <div class="confidence-badge">
                        <span id="confidence-value">${confidence}%</span> Confidence
                    </div>
                </div>
                <div class="result-content">
                    <div class="gender-display ${isMale ? 'male' : 'female'}">
                        <span id="gender-result">${isMale ? 'Male' : 'Female'}</span>
                    </div>
                    <div class="image-preview">
                        <img id="analyzed-image" src="${imageData}" alt="Analyzed Image">
                    </div>
                    <div class="features-list">
                        <h4>Key Features Detected:</h4>
                        <ul id="features-detected">
                            ${features.map(f => `<li>${f}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;
        }, 2000);
    }

    // Initialize with upload tab active
    switchTab('upload');
});