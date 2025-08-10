// Funciones para el sistema de postulaciones y calificaciones

// Función para aplicar a una vacante
function aplicarVacante(vacanteId) {
    // Verificar si el usuario está logueado
    if (typeof userLoggedIn !== 'undefined' && userLoggedIn) {
        // Crear formulario para enviar la postulación
        const formData = new FormData();
        formData.append('vacante_id', vacanteId);
        
        // Enviar la postulación
        fetch('/aplicar_vacante', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('¡Postulación enviada exitosamente!', 'success');
                // Deshabilitar el botón
                const boton = document.querySelector(`[data-vacante-id="${vacanteId}"] .btn-apply`);
                if (boton) {
                    boton.textContent = 'Postulado';
                    boton.disabled = true;
                    boton.style.backgroundColor = '#6c757d';
                }
            } else {
                showNotification('Error: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error al enviar la postulación', 'error');
        });
    } else {
        // Redirigir al login si no está logueado
        window.location.href = '/login';
    }
}

// Función para calificar una vacante
function calificarVacante(vacanteId, rating) {
    if (typeof userLoggedIn !== 'undefined' && userLoggedIn) {
        // Enviar calificación
        fetch('/calificar_vacante', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                vacante_id: vacanteId,
                calificacion: rating
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar estrellas visualmente
                const stars = document.querySelectorAll(`[data-vacante-id="${vacanteId}"] .star`);
                stars.forEach((star, index) => {
                    if (index < rating) {
                        star.classList.add('active');
                    } else {
                        star.classList.remove('active');
                    }
                });
                showNotification('¡Calificación enviada!', 'success');
            } else {
                showNotification('Error: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error al enviar la calificación', 'error');
        });
    } else {
        showNotification('Debes iniciar sesión para calificar', 'warning');
    }
}

// Función para cancelar una postulación
function cancelarPostulacion(postulacionId) {
    if (confirm('¿Estás seguro de que quieres cancelar esta postulación?')) {
        const formData = new FormData();
        formData.append('postulacion_id', postulacionId);
        
        fetch('/cancelar_postulacion', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Postulación cancelada exitosamente', 'success');
                // Recargar la página para mostrar el estado actualizado
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                showNotification('Error: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error al cancelar la postulación', 'error');
        });
    }
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    // Agregar estilos
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : type === 'warning' ? '#ffc107' : '#17a2b8'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Función para inicializar estrellas de calificación
function initializeRatingStars() {
    const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('mouseenter', function() {
            const rating = this.dataset.rating;
            const parentStars = this.parentElement.children;
            for (let i = 0; i < parentStars.length; i++) {
                if (i < rating) {
                    parentStars[i].classList.add('hover');
                } else {
                    parentStars[i].classList.remove('hover');
                }
            }
        });

        star.addEventListener('mouseleave', function() {
            const parentStars = this.parentElement.children;
            for (let i = 0; i < parentStars.length; i++) {
                parentStars[i].classList.remove('hover');
            }
        });
    });
}

// Función para filtrar postulaciones por estado
function filterPostulaciones(status) {
    const cards = document.querySelectorAll('.postulacion-card');
    
    cards.forEach(card => {
        if (status === 'todos' || card.dataset.status === status) {
            card.style.display = 'block';
            card.style.animation = 'slideInUp 0.3s ease-out';
        } else {
            card.style.display = 'none';
        }
    });
}

// Función para buscar postulaciones
function searchPostulaciones(searchTerm) {
    const cards = document.querySelectorAll('.postulacion-card');
    
    cards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const empresa = card.querySelector('.empresa-nombre').textContent.toLowerCase();
        
        if (title.includes(searchTerm.toLowerCase()) || empresa.includes(searchTerm.toLowerCase())) {
            card.style.display = 'block';
            card.style.animation = 'slideInUp 0.3s ease-out';
        } else {
            card.style.display = 'none';
        }
    });
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar estrellas de calificación
    initializeRatingStars();
    
    // Configurar filtros de postulaciones
    const statusFilter = document.getElementById('status-filter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            filterPostulaciones(this.value);
        });
    }
    
    // Configurar búsqueda de postulaciones
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            searchPostulaciones(this.value);
        });
    }
    
    // Configurar botón de búsqueda
    const searchBtn = document.getElementById('search-btn');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const searchTerm = document.getElementById('search-input').value;
            searchPostulaciones(searchTerm);
        });
    }
});

// Agregar estilos CSS para las notificaciones
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
        padding: 0;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background-color 0.2s ease;
    }
    
    .notification-close:hover {
        background: rgba(255,255,255,0.2);
    }
    
    .notification-message {
        flex: 1;
        font-weight: 500;
    }
`;

document.head.appendChild(notificationStyles); 