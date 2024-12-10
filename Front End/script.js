document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('vqa-form');
    const resultContainer = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    const fileInput = document.getElementById('file-upload');
    const queryInput = document.getElementById('query');
    const clearButton = document.getElementById('clear-button');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); 

        if (!fileInput.files.length) {
            alert("Please select an image file.");
            return;
        }

        if (!queryInput.value.trim()) {
            alert("Please enter a question.");
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('query', queryInput.value);

        try {
            const response = await fetch('http://127.0.0.1:8000/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Failed to generate report');

            const result = await response.json();
            resultText.value = result.answer || result.error || 'No valid response received.';
        } catch (error) {
            resultText.value = `Error: ${error.message}`;
        }
    });

    window.simulateResponse = function () {
        const response = "This is the response body containing health information.";
        resultText.value = response;
        resultContainer.classList.remove('d-none');
    };


    clearButton.addEventListener('click', () => {
        fileInput.value = '';
        queryInput.value = '';
        resultContainer.classList.add('d-none');
        resultText.value = '';
    });
});
