document.addEventListener('DOMContentLoaded', function() {
    const HIDE_DELAY_MS = 5000; 

    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            
            alert.style.transition = 'opacity 1s ease-out';
            alert.style.opacity = '0';
            
            setTimeout(function() {
                alert.remove();
            }, 1000); 
        });
    }, HIDE_DELAY_MS); 
});