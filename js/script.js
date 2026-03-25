// FitCafe Sales Page - JavaScript
// This file contains minimal JavaScript for the sales page

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links (if needed)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add any future interactive elements here
    // For now, this is a static sales page with minimal JS requirements
    
    // Example: Track CTA clicks (placeholder for analytics)
    const ctaButtons = document.querySelectorAll('.cta-button');
    ctaButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Placeholder for analytics tracking
            // gtag('event', 'click', { event_category: 'CTA', event_label: 'Try FitCafe' });
            console.log('CTA clicked - replace with actual affiliate link');
        });
    });
});