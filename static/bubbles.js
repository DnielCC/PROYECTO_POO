// Script para generar burbujas animadas
document.addEventListener('DOMContentLoaded', function() {
    const leftPanel = document.querySelector('.left-panel');
    
    if (!leftPanel) return;
    
    // Función para crear una burbuja
    function createBubble() {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        
        // Posición aleatoria horizontal
        const left = Math.random() * 100;
        bubble.style.left = left + '%';
        
        // Tamaño aleatorio
        const size = Math.random() * 8 + 4; // Entre 4px y 12px
        bubble.style.width = size + 'px';
        bubble.style.height = size + 'px';
        
        // Duración de animación aleatoria
        const duration = Math.random() * 10 + 15; // Entre 15s y 25s
        bubble.style.animationDuration = duration + 's';
        
        // Delay aleatorio
        const delay = Math.random() * 5;
        bubble.style.animationDelay = delay + 's';
        
        // Opacidad aleatoria
        const opacity = Math.random() * 0.1 + 0.05; // Entre 0.05 y 0.15
        bubble.style.opacity = opacity;
        
        leftPanel.appendChild(bubble);
        
        // Remover la burbuja después de la animación
        setTimeout(() => {
            if (bubble.parentNode) {
                bubble.parentNode.removeChild(bubble);
            }
        }, (duration + delay) * 1000);
    }
    
    // Crear burbujas iniciales
    for (let i = 0; i < 15; i++) {
        setTimeout(() => {
            createBubble();
        }, i * 1000); // Una burbuja cada segundo
    }
    
    // Continuar creando burbujas
    setInterval(() => {
        createBubble();
    }, 2000); // Nueva burbuja cada 2 segundos
});

// Función para pausar/reanudar animaciones en dispositivos que prefieren menos movimiento
if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    function handleMotionPreference(e) {
        const bubbles = document.querySelectorAll('.bubble');
        bubbles.forEach(bubble => {
            if (e.matches) {
                bubble.style.animationPlayState = 'paused';
            } else {
                bubble.style.animationPlayState = 'running';
            }
        });
    }
    
    mediaQuery.addListener(handleMotionPreference);
    handleMotionPreference(mediaQuery);
} 