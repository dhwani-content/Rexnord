document.addEventListener('DOMContentLoaded', () => {
    // Mobile Navigation Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('show');
            const icon = mobileToggle.querySelector('i');
            if (navLinks.classList.contains('show')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Scroll Animation - Fade In Elements
    const fadeElements = document.querySelectorAll('.card, .about-grid > div, .category-content > div, .contact-card');
    
    // Add initial pristine class for animation targeting
    fadeElements.forEach(el => el.classList.add('fade-in'));

    const observeElements = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: Stop observing once faded in
                observeElements.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15, // Trigger when 15% visible
        rootMargin: '0px 0px -50px 0px'
    });

    fadeElements.forEach(el => observeElements.observe(el));

    // Simple Form Validation for Contact Page
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Basic validation check
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            if(name && email && message) {
                // In a real application, send this data to a server
                alert('Thank you for your inquiry, ' + name + '. Our sales team will get back to you shortly.');
                contactForm.reset();
            } else {
                alert('Please fill out all required fields.');
            }
        });
    }
    
    // Smooth scrolling for anchor links (e.g., from Home to Products categories)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if(targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if(targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // PDF Modal Logic for Couplings/Bearings Page
    const pdfModal = document.getElementById('pdfModal');
    const pdfIframe = document.getElementById('pdfIframe');

    if (pdfModal) {
        const closeModal = () => {
            pdfModal.classList.remove('show');
            if (pdfIframe) {
                setTimeout(() => {
                    pdfIframe.src = ''; // Clear iframe after small delay for smooth transition
                }, 300);
            }
            document.body.style.overflow = ''; // Restore scrolling
        };

        // Target close buttons specifically within pdfModal
        const pdfCloseBtns = pdfModal.querySelectorAll('.close-modal');
        pdfCloseBtns.forEach(el => {
            el.addEventListener('click', closeModal);
        });

        // Close on outside click
        window.addEventListener('click', (e) => {
            if (e.target === pdfModal) {
                closeModal();
            }
        });

        // Close on Esc key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && pdfModal.classList.contains('show')) {
                closeModal();
            }
        });

        // Handle direct single catalog buttons (if any still exist)
        const viewCatalogBtns = document.querySelectorAll('.view-catalog-btn');
        viewCatalogBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const pdfSrc = this.getAttribute('data-pdf-src');
                if (pdfSrc && pdfIframe) {
                    pdfIframe.src = pdfSrc;
                    pdfModal.classList.add('show');
                    document.body.style.overflow = 'hidden'; // Prevent background scrolling
                }
            });
        });
    }

    // Catalog Multi-Selector Modal Logic
    const selectorModal = document.getElementById('selectorModal');
    const selectorModalBody = document.getElementById('selectorModalBody');
    const selectorModalTitle = document.getElementById('selectorModalTitle');

    if (selectorModal) {
        const closeSelector = () => {
            selectorModal.classList.remove('show');
            document.body.style.overflow = ''; // Restore scrolling
        };

        // Target close buttons specifically within selectorModal
        const selectorCloseBtns = selectorModal.querySelectorAll('.close-modal');
        selectorCloseBtns.forEach(el => {
            el.addEventListener('click', closeSelector);
        });

        // Close on outside click
        window.addEventListener('click', (e) => {
            if (e.target === selectorModal) {
                closeSelector();
            }
        });

        // Close on Esc key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && selectorModal.classList.contains('show')) {
                closeSelector();
            }
        });

        const multiCatalogBtns = document.querySelectorAll('.view-multi-catalog-btn');
        multiCatalogBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const brand = this.getAttribute('data-brand') || "Available";
                const catalogsStr = this.getAttribute('data-catalogs');
                
                if (catalogsStr && selectorModalBody) {
                    try {
                        const catalogs = JSON.parse(catalogsStr);
                        if (selectorModalTitle) selectorModalTitle.textContent = `${brand} Catalogs`;
                        
                        // Clear previous buttons
                        selectorModalBody.innerHTML = '';
                        
                        catalogs.forEach(cat => {
                            const linkBtn = document.createElement('button');
                            linkBtn.className = 'catalog-link-btn';
                            linkBtn.innerHTML = `<span>${cat.title}</span> <i class="fas fa-chevron-right"></i>`;
                            linkBtn.onclick = () => {
                                // Close this modal
                                selectorModal.classList.remove('show');
                                // Open PDF modal
                                if (pdfModal && pdfIframe) {
                                    pdfIframe.src = cat.src;
                                    setTimeout(() => {
                                        pdfModal.classList.add('show');
                                        document.body.style.overflow = 'hidden'; // Keep background locked
                                    }, 100);
                                }
                            };
                            selectorModalBody.appendChild(linkBtn);
                        });
                        
                        selectorModal.classList.add('show');
                        document.body.style.overflow = 'hidden'; // Lock background
                    } catch (err) {
                        console.error('Error parsing catalogs:', err);
                    }
                }
            });
        });
    }

    // Part Number Search Logic
    const searchInput = document.getElementById('partSearchInput');
    const tableBody = document.getElementById('catalogTableBody');
    const noResultsMessage = document.getElementById('noResultsMessage');

    if (searchInput && tableBody) {
        searchInput.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const rows = tableBody.getElementsByTagName('tr');
            let visibleCount = 0;

            for (let i = 0; i < rows.length; i++) {
                const textContent = rows[i].textContent || rows[i].innerText;
                if (textContent.toLowerCase().indexOf(filter) > -1) {
                    rows[i].style.display = '';
                    visibleCount++;
                } else {
                    rows[i].style.display = 'none';
                }
            }

            // Show 'No Results' if nothing matches
            if (visibleCount === 0) {
                noResultsMessage.style.display = 'block';
                tableBody.parentElement.style.display = 'none'; // hide table header
            } else {
                noResultsMessage.style.display = 'none';
                tableBody.parentElement.style.display = 'table';
            }
        });
    }
});
