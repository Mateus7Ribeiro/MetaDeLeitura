document.addEventListener('DOMContentLoaded', function() {
    console.log('Script carregado com sucesso');
});

// Função para atualizar progresso via AJAX
async function updateProgress(bookId, currentPage) {
    try {
        const response = await fetch(`/api/book/${bookId}/update-progress`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                current_page: currentPage
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Progresso atualizado:', data);
            // Recarregar a página para exibir atualizações
            location.reload();
        } else {
            console.error('Erro ao atualizar progresso');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
    }
}

// Formatadores de data
function formatDate(dateString) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
}

// Validação de formulário
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = 'var(--danger-color)';
            isValid = false;
        } else {
            input.style.borderColor = '';
        }
    });
    
    return isValid;
}
