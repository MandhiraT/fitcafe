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
// Opt-in Form Handler — Listmonk Subscription
(function() {
    function initOptinForm() {
        var form = document.getElementById('fitcafe-optin-form');
        if (!form) return;
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            var name = document.getElementById('optin-name').value.trim();
            var email = document.getElementById('optin-email').value.trim();
            var btn = form.querySelector('button[type="submit"]');
            
            btn.textContent = 'Sending...';
            btn.disabled = true;
            
            // Listmonk public subscription form
            // List UUID: a2795f04-b3f6-42a1-8380-b3b2460c15f9 (FitCafe Subscribers)
            var formData = new URLSearchParams();
            formData.append('l', 'a2795f04-b3f6-42a1-8380-b3b2460c15f9');
            formData.append('email', email);
            formData.append('name', name);
            
            fetch('https://listmonk.thequietself.com/subscription/form', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData.toString()
            })
            .then(function(response) {
                form.style.display = 'none';
                document.getElementById('optin-success').style.display = 'block';
                window.scrollTo({ top: document.getElementById('optin-success').offsetTop - 100, behavior: 'smooth' });
            })
            .catch(function(error) {
                console.error('Subscription error:', error);
                btn.textContent = 'Send Me the Free Guide →';
                btn.disabled = false;
                // Fallback: still show success (don't block UX)
                form.style.display = 'none';
                document.getElementById('optin-success').style.display = 'block';
            });
        });
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initOptinForm);
    } else {
        initOptinForm();
    }
})();
