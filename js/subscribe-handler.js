/**
 * FitCafe Subscription Handler
 * Intercepts form submission and handles redirect
 */

(function() {
    'use strict';
    
    // Wait for DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    function init() {
        // Find all opt-in forms
        const forms = document.querySelectorAll('.optin-form');
        
        forms.forEach(function(form) {
            // Only process forms pointing to listmonk
            if (form.action.includes('listmonk')) {
                form.addEventListener('submit', handleSubmit);
            }
        });
    }
    
    function handleSubmit(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        
        // Get values
        const name = formData.get('name');
        const email = formData.get('email');
        const listId = formData.get('l');
        
        // Show loading state
        const button = form.querySelector('button[type="submit"]');
        const originalText = button.textContent;
        button.textContent = 'Subscribing...';
        button.disabled = true;
        
        // Submit to Listmonk
        fetch('https://listmonk.thequietself.com/subscription/form', {
            method: 'POST',
            mode: 'no-cors', // Important: allows cross-origin without CORS errors
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'l': listId,
                'name': name,
                'email': email
            })
        }).then(function() {
            // Success - redirect to thank you page
            window.location.href = 'https://fitcafecoffee.com?subscribed=true';
        }).catch(function(error) {
            // Even if there's an error, redirect (no-cors mode may cause false errors)
            console.log('Subscription submitted (or network error - redirecting anyway)');
            window.location.href = 'https://fitcafecoffee.com?subscribed=true';
        });
    }
})();
