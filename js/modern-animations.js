/**
 * FitCafe Modern Design - Scroll Animations & Interactions
 */

document.addEventListener('DOMContentLoaded', function() {
  
  // 1. Navbar scroll effect
  const navbar = document.querySelector('.navbar');
  
  if (navbar) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }
  
  // 2. Section fade-in on scroll
  const sections = document.querySelectorAll('section');
  
  const sectionObserver = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });
  
  sections.forEach(section => {
    sectionObserver.observe(section);
  });
  
  // 3. Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const target = document.querySelector(targetId);
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // 4. Button hover effect enhancement
  document.querySelectorAll('.cta-button, button[type="submit"]').forEach(button => {
    button.addEventListener('mouseenter', function(e) {
      const rect = button.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      button.style.setProperty('--hover-x', x + 'px');
      button.style.setProperty('--hover-y', y + 'px');
    });
  });
  
  // 5. Parallax effect for hero image
  const heroImage = document.querySelector('#headline .product-hero-image');
  
  if (heroImage) {
    window.addEventListener('scroll', function() {
      const scrolled = window.scrollY;
      const heroSection = document.querySelector('#headline');
      
      if (heroSection && scrolled < heroSection.offsetHeight) {
        heroImage.style.transform = `translateY(${scrolled * 0.3}px)`;
      }
    });
  }
  
  // 6. Counter animation for stats (if added)
  const animateCounter = function(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(function() {
      start += increment;
      if (start >= target) {
        element.textContent = target.toLocaleString();
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(start).toLocaleString();
      }
    }, 16);
  };
  
  // 7. Form validation enhancement
  const optinForm = document.getElementById('optin-form');
  
  if (optinForm) {
    const emailInput = document.getElementById('optin-email');
    const nameInput = document.getElementById('optin-name');
    
    if (emailInput) {
      emailInput.addEventListener('blur', function() {
        const email = this.value;
        const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        
        if (email && !isValid) {
          this.style.borderColor = '#FF6B6B';
        } else {
          this.style.borderColor = '#E2E8F0';
        }
      });
    }
  }
  
  console.log('✅ Modern animations loaded');
});
