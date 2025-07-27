// Script para mejorar la interactividad de la navbar
document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los enlaces de navegación
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Agregar efecto de hover mejorado
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            // Agregar clase de hover para efectos adicionales
            this.classList.add('nav-hover');
        });
        
        link.addEventListener('mouseleave', function() {
            // Remover clase de hover
            this.classList.remove('nav-hover');
        });
        
        // Efecto de click
        link.addEventListener('click', function() {
            // Agregar efecto de ripple
            const ripple = document.createElement('div');
            ripple.classList.add('nav-ripple');
            this.appendChild(ripple);
            
            // Remover ripple después de la animación
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Detectar la página actual y marcar como activa
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Efecto de scroll para la navbar
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scroll hacia abajo - ocultar navbar
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scroll hacia arriba - mostrar navbar
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
});

// Agregar estilos CSS dinámicos para efectos adicionales
const style = document.createElement('style');
style.textContent = `
    .nav-hover {
        transform: translateY(-2px);
    }
    
    .nav-ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(59, 130, 246, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .navbar {
        transition: transform 0.3s ease;
    }
`;
document.head.appendChild(style); 