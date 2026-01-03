/**
 * Edit Book - Gerenciamento de Progresso de Leitura
 * Sincronização entre campos de páginas, slider e percentual
 */

class BookProgressManager {
    constructor() {
        this.totalPagesInput = document.getElementById('total_pages');
        this.currentPageInput = document.getElementById('current_page');
        this.pagesSlider = document.getElementById('pagesSlider');
        this.percentDisplay = document.getElementById('percentDisplay');
        this.progressPreview = document.getElementById('progressPreview');
        
        this.isUpdating = false;
        
        this.init();
    }
    
    init() {
        this.attachEventListeners();
    }
    
    /**
     * Atualiza todos os elementos visuais de progresso
     */
    updateProgress() {
        if (this.isUpdating) return;
        this.isUpdating = true;
        
        const total = parseInt(this.totalPagesInput.value) || 1;
        const current = parseInt(this.currentPageInput.value) || 0;
        const percent = ((current / total) * 100).toFixed(2);
        
        this.percentDisplay.textContent = percent + '%';
        if (this.progressPreview) {
            this.progressPreview.style.width = percent + '%';
        }
        this.currentPageInput.max = total;
        this.pagesSlider.max = total;
        
        setTimeout(() => this.isUpdating = false, 50);
    }
    
    /**
     * Torna o display de percentual editável via input inline
     */
    makePercentEditable() {
        const currentValue = parseFloat(this.percentDisplay.textContent) || 0;
        const total = parseInt(this.totalPagesInput.value) || 1;
        
        // Criar input temporário
        const input = document.createElement('input');
        input.type = 'number';
        input.min = '0';
        input.max = '100';
        input.step = '0.1';
        input.value = currentValue.toFixed(2);
        input.style.cssText = 'width: 80px; text-align: center; font-size: 1rem; font-weight: bold; border: 2px solid #667eea; border-radius: 4px; padding: 4px;';
        
        // Substituir o span pelo input
        this.percentDisplay.style.display = 'none';
        this.percentDisplay.parentNode.insertBefore(input, this.percentDisplay);
        input.focus();
        input.select();
        
        let inputUpdating = false;
        
        // Ao digitar, atualizar páginas
        input.addEventListener('input', () => {
            if (inputUpdating) return;
            inputUpdating = true;
            
            const percentage = parseFloat(input.value) || 0;
            const pages = Math.round((percentage / 100) * total);
            
            this.currentPageInput.value = pages;
            this.pagesSlider.value = pages;
            
            if (this.progressPreview) {
                this.progressPreview.style.width = Math.min(Math.max(percentage, 0), 100) + '%';
            }
            
            setTimeout(() => inputUpdating = false, 50);
        });
        
        // Ao perder foco ou pressionar Enter, voltar para span
        const finishEdit = () => {
            const finalValue = parseFloat(input.value) || 0;
            this.percentDisplay.textContent = Math.min(Math.max(finalValue, 0), 100).toFixed(2) + '%';
            input.remove();
            this.percentDisplay.style.display = 'inline';
        };
        
        input.addEventListener('blur', finishEdit);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                finishEdit();
            }
        });
    }
    
    /**
     * Anexa todos os event listeners necessários
     */
    attachEventListeners() {
        // Atualizar quando total de páginas mudar
        this.totalPagesInput.addEventListener('change', () => this.updateProgress());
        
        // Sincronizar campo de páginas com slider
        this.currentPageInput.addEventListener('input', () => {
            this.pagesSlider.value = this.currentPageInput.value;
            this.updateProgress();
        });
        
        // Sincronizar slider com campo de páginas e atualizar preview em tempo real
        this.pagesSlider.addEventListener('input', () => {
            this.currentPageInput.value = this.pagesSlider.value;
            
            // Atualizar preview imediatamente enquanto arrasta
            const total = parseInt(this.totalPagesInput.value) || 1;
            const current = parseInt(this.pagesSlider.value) || 0;
            const percent = ((current / total) * 100).toFixed(2);
            
            this.percentDisplay.textContent = percent + '%';
            
            if (this.progressPreview) {
                this.progressPreview.style.width = percent + '%';
            }
        });
        
        // Tornar percentual clicável
        this.percentDisplay.addEventListener('click', () => this.makePercentEditable());
        
        // Efeito hover no percentual
        this.percentDisplay.addEventListener('mouseleave', () => {
            this.percentDisplay.style.backgroundColor = 'transparent';
            this.percentDisplay.style.transform = 'scale(1)';
        });
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new BookProgressManager();
});
