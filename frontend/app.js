// DOM elements
const loadingOverlay = document.getElementById('loading-overlay');
const toastContainer = document.getElementById('toast-container');

// Tab navigation
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

// Forms
const scriptForm = document.getElementById('script-form');
const voiceForm = document.getElementById('voice-form');
const videoForm = document.getElementById('video-form');

// Output elements
const scriptOutput = document.getElementById('output');
const voiceOutput = document.getElementById('voice-output');
const videoOutput = document.getElementById('video-output');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    initializeForms();
    initializeActionButtons();
});

// Tab navigation functionality
function initializeTabs() {
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.dataset.tab;
            
            // Update active tab button
            tabButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
            });
            button.classList.add('active');
            button.setAttribute('aria-selected', 'true');
            
            // Update active tab content
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
}

// Form initialization
function initializeForms() {
    // Script form
    if (scriptForm) {
        scriptForm.addEventListener('submit', handleScriptSubmit);
        
        // Clear form button
        const clearButton = document.getElementById('clear-form');
        if (clearButton) {
            clearButton.addEventListener('click', () => {
                scriptForm.reset();
                scriptOutput.textContent = '';
                showToast('Form cleared', 'info');
            });
        }
    }

    // Voice form
    if (voiceForm) {
        voiceForm.addEventListener('submit', handleVoiceSubmit);
    }

    // Video form
    if (videoForm) {
        videoForm.addEventListener('submit', handleVideoSubmit);
    }
}

// Action buttons initialization
function initializeActionButtons() {
    // Copy script button
    const copyScriptBtn = document.getElementById('copy-script');
    if (copyScriptBtn) {
        copyScriptBtn.addEventListener('click', () => {
            copyToClipboard(scriptOutput.textContent, 'Script copied to clipboard!');
        });
    }

    // Download script button
    const downloadScriptBtn = document.getElementById('download-script');
    if (downloadScriptBtn) {
        downloadScriptBtn.addEventListener('click', () => {
            downloadText(scriptOutput.textContent, 'script.txt', 'Script downloaded!');
        });
    }

    // Play voice button
    const playVoiceBtn = document.getElementById('play-voice');
    if (playVoiceBtn) {
        playVoiceBtn.addEventListener('click', () => {
            // Implementation for playing voice
            showToast('Voice playback feature coming soon!', 'info');
        });
    }

    // Download voice button
    const downloadVoiceBtn = document.getElementById('download-voice');
    if (downloadVoiceBtn) {
        downloadVoiceBtn.addEventListener('click', () => {
            showToast('Voice download feature coming soon!', 'info');
        });
    }

    // Preview video button
    const previewVideoBtn = document.getElementById('preview-video');
    if (previewVideoBtn) {
        previewVideoBtn.addEventListener('click', () => {
            showToast('Video preview feature coming soon!', 'info');
        });
    }

    // Download video button
    const downloadVideoBtn = document.getElementById('download-video');
    if (downloadVideoBtn) {
        downloadVideoBtn.addEventListener('click', () => {
            showToast('Video download feature coming soon!', 'info');
        });
    }
}

// Script form submission
async function handleScriptSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(scriptForm);
    const topic = formData.get('topic').trim();
    const length = formData.get('length');
    const style = formData.get('style');

    if (!topic) {
        showToast('Please enter a video topic', 'error');
        return;
    }

    showLoading(true);
    scriptOutput.textContent = '⏳ Generating script… please wait';

    try {
        const response = await fetch("/generate_script/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, length, style }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Unknown error occurred");
        }

        const data = await response.json();
        scriptOutput.textContent = `✅ Script saved to: ${data.script_path}\n\nLoading content...`;

        // Fetch generated script content
        try {
            const scriptRes = await fetch(data.script_path);
            if (scriptRes.ok) {
                const text = await scriptRes.text();
                scriptOutput.textContent = text;
                showToast('Script generated successfully!', 'success');
            } else {
                scriptOutput.textContent += "\n⚠️ Could not load script content.";
                showToast('Script generated but content could not be loaded', 'info');
            }
        } catch (scriptError) {
            scriptOutput.textContent += `\n⚠️ Could not load script content: ${scriptError.message}`;
            showToast('Script generated but content could not be loaded', 'info');
        }

    } catch (error) {
        scriptOutput.textContent = `❌ Error: ${error.message}`;
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Voice form submission
async function handleVoiceSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(voiceForm);
    const text = formData.get('voice-text').trim();
    const voiceType = formData.get('voice-type');
    const voiceSpeed = formData.get('voice-speed');

    if (!text) {
        showToast('Please enter text to convert', 'error');
        return;
    }

    if (text.length > 5000) {
        showToast('Text is too long (max 5000 characters)', 'error');
        return;
    }

    showLoading(true);
    voiceOutput.textContent = '⏳ Generating voice… please wait';

    try {
        const response = await fetch("/generate_voice/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, voice_type: voiceType, speed: voiceSpeed }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Unknown error occurred");
        }

        const data = await response.json();
        voiceOutput.textContent = `✅ Voice generated successfully!\n\nFile: ${data.voice_path}\nDuration: ${data.duration || 'Unknown'}`;
        showToast('Voice generated successfully!', 'success');

    } catch (error) {
        voiceOutput.textContent = `❌ Error: ${error.message}`;
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Video form submission
async function handleVideoSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(videoForm);
    const scriptFile = formData.get('video-script');
    const videoStyle = formData.get('video-style');
    const videoResolution = formData.get('video-resolution');

    if (!scriptFile || scriptFile.size === 0) {
        showToast('Please select a script file', 'error');
        return;
    }

    showLoading(true);
    videoOutput.textContent = '⏳ Creating video… please wait';

    try {
        const formDataToSend = new FormData();
        formDataToSend.append('script_file', scriptFile);
        formDataToSend.append('style', videoStyle);
        formDataToSend.append('resolution', videoResolution);

        const response = await fetch("/create_video/", {
            method: "POST",
            body: formDataToSend,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Unknown error occurred");
        }

        const data = await response.json();
        videoOutput.textContent = `✅ Video created successfully!\n\nFile: ${data.video_path}\nDuration: ${data.duration || 'Unknown'}\nSize: ${data.size || 'Unknown'}`;
        showToast('Video created successfully!', 'success');

    } catch (error) {
        videoOutput.textContent = `❌ Error: ${error.message}`;
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Utility functions
function showLoading(show) {
    if (show) {
        loadingOverlay.classList.add('active');
    } else {
        loadingOverlay.classList.remove('active');
    }
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function copyToClipboard(text, successMessage) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(successMessage, 'success');
        }).catch(() => {
            showToast('Failed to copy to clipboard', 'error');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast(successMessage, 'success');
        } catch (err) {
            showToast('Failed to copy to clipboard', 'error');
        }
        document.body.removeChild(textArea);
    }
}

function downloadText(content, filename, successMessage) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    showToast(successMessage, 'success');
}

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#ff4444';
            isValid = false;
        } else {
            field.style.borderColor = 'rgba(0, 255, 255, 0.3)';
        }
    });
    
    return isValid;
}

// Add form validation to all forms
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        if (!validateForm(form)) {
            e.preventDefault();
            showToast('Please fill in all required fields', 'error');
        }
    });
});
