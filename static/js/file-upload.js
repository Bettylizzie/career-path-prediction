document.addEventListener('DOMContentLoaded', function() {
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('file-upload');
    
    if (uploadBox && fileInput) {
        // Handle file selection
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                uploadBox.innerHTML = `
                    <i class="fas fa-file-alt"></i>
                    <h3>${this.files.length} file(s) selected</h3>
                    <p>Ready to upload</p>
                `;
            }
        });
        
        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadBox.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadBox.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadBox.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            uploadBox.classList.add('highlight');
        }
        
        function unhighlight() {
            uploadBox.classList.remove('highlight');
        }
        
        uploadBox.addEventListener('drop', function(e) {
            fileInput.files = e.dataTransfer.files;
            if (fileInput.files.length > 0) {
                this.innerHTML = `
                    <i class="fas fa-file-alt"></i>
                    <h3>${fileInput.files.length} file(s) dropped</h3>
                    <p>Ready to upload</p>
                `;
            }
        });
    }
});