document.addEventListener('DOMContentLoaded', () => {
    // Intersection Observer for Entrance Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('opacity-100', 'translate-y-0');
                entry.target.classList.remove('opacity-0', 'translate-y-8');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => {
        el.classList.add('opacity-0', 'translate-y-8', 'transition-all', 'duration-700', 'ease-out');
        observer.observe(el);
    });

    // Media Filter Logic
    const filterButtons = document.querySelectorAll('[data-filter]');
    const mediaItems = document.querySelectorAll('.media-item');

    if (filterButtons.length > 0 && mediaItems.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const filterValue = btn.getAttribute('data-filter');
                
                // Update active state on buttons
                filterButtons.forEach(b => {
                    b.classList.remove('bg-deep-navy', 'text-white');
                    b.classList.add('bg-surface-bright', 'text-deep-navy');
                });
                btn.classList.add('bg-deep-navy', 'text-white');
                btn.classList.remove('bg-surface-bright', 'text-deep-navy');

                // Filter items
                mediaItems.forEach(item => {
                    if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }
});
