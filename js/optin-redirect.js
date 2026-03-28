/**
 * FitCafe Opt-in Form Redirect Handler
 * Redirects users back to fitcafecoffee.com after successful subscription
 */

(function() {
    'use strict';
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    function init() {
        // Check if we're on Listmonk subscription success page
        const isListmonkSuccess = document.body.textContent.includes('Subscribed successfully') ||
                                  document.title.includes('Subscribed') ||
                                  document.querySelector('.success') ||
                                  document.querySelector('.message-success');
        
        if (isListmonkSuccess) {
            // Show redirecting message
            showRedirectMessage();
            
            // Redirect after 2 seconds
            setTimeout(function() {
                window.location.href = 'https://fitcafecoffee.com?subscribed=true';
            }, 2000);
        }
    }
    
    function showRedirectMessage() {
        // Create redirect message overlay
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(192, 86, 33, 0.95);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            font-family: 'Inter', sans-serif;
        `;
        
        overlay.innerHTML = `
            <div style="text-align: center; max-width: 500px; padding: 20px;">
                <div style="font-size: 48px; margin-bottom: 20px;">✅</div>
                <h1 style="font-size: 32px; margin-bottom: 15px; font-weight: 700;">Subscribed Successfully!</h1>
                <p style="font-size: 18px; margin-bottom: 30px; opacity: 0.9;">Thank you for subscribing to FitCafe.</p>
                <p style="font-size: 16px; opacity: 0.8;">Redirecting you back to FitCafe Coffee...</p>
                <div style="margin-top: 30px;">
                    <div style="width: 50px; height: 50px; border: 5px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
                </div>
            </div>
            <style>
                @keyframes spin {
                    to { transform: rotate(360deg); }
                }
            </style>
        `;
        
        document.body.appendChild(overlay);
        
        // Also update the original page title
        document.title = 'Subscribed Successfully - FitCafe';
    }
})();
