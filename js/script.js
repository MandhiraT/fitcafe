// FitCafe Sales Page - JavaScript
// Minimal script for basic functionality and future analytics

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // CTA button click tracking (placeholder for analytics)
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('click', function() {
            // Analytics tracking code can be added here
            console.log('CTA clicked - ready for affiliate link integration');
        });
    }

    // Mobile menu toggle (if needed in future)
    // Currently not implemented as this is a single-page sales site

    // Lazy loading for images (when product images are added)
    const imageObserver = new IntersectionObserver((entries, imgObserver) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const lazyImage = entry.target;
                lazyImage.src = lazyImage.dataset.src;
                lazyImage.classList.remove('lazy');
                imgObserver.unobserve(lazyImage);
            }
        });
    });

    const lazyImages = document.querySelectorAll('img.lazy');
    lazyImages.forEach((lazyImage) => {
        imageObserver.observe(lazyImage);
    });
});