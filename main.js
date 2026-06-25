// =============================================
// EduVerse LMS - Main JavaScript File
// =============================================

document.addEventListener('DOMContentLoaded', () => {
    initFlashMessages();
    initRoleSelector();
    initSidebarToggle();
    initActiveNav();
    animateStatNumbers();
    initSearchFilter();
    initModals();
    initDynamicForms();
});

// ─────────────────────────────────────────────
// FLASH MESSAGES AUTO-DISMISS
// ─────────────────────────────────────────────
function initFlashMessages() {
    const flashMsgs = document.querySelectorAll('.flash-msg');
    flashMsgs.forEach((msg, i) => {
        // Auto dismiss after 4 seconds
        setTimeout(() => dismissFlash(msg), 4000 + i * 300);

        // Close button
        const closeBtn = msg.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => dismissFlash(msg));
        }
    });
}

function dismissFlash(el) {
    el.style.opacity = '0';
    el.style.transform = 'translateX(40px)';
    el.style.transition = 'all 0.3s ease';
    setTimeout(() => el.remove(), 300);
}

// ─────────────────────────────────────────────
// ROLE SELECTOR (Register Page)
// ─────────────────────────────────────────────
function initRoleSelector() {
    const roleInputs = document.querySelectorAll('input[name="role"]');
    const extraFieldsMap = {
        student: document.getElementById('student-fields'),
        trainer: document.getElementById('trainer-fields'),
        institute: document.getElementById('institute-fields'),
    };
    const instSelectEl = document.getElementById('institute-select-fields');

    function updateFields(selectedRole) {
        Object.entries(extraFieldsMap).forEach(([role, el]) => {
            if (!el) return;
            if (role === selectedRole) {
                el.style.display = 'block';
                el.style.animation = 'fadeInUp 0.3s ease';
            } else {
                el.style.display = 'none';
            }
        });

        if (instSelectEl) {
            const selectField = instSelectEl.querySelector('select');
            const textareaField = instSelectEl.querySelector('textarea');
            if (selectedRole === 'student' || selectedRole === 'trainer') {
                instSelectEl.style.display = 'block';
                instSelectEl.style.animation = 'fadeInUp 0.3s ease';
                if (selectField) selectField.required = true;
                if (textareaField) textareaField.required = true;
            } else {
                instSelectEl.style.display = 'none';
                if (selectField) selectField.required = false;
                if (textareaField) textareaField.required = false;
            }
        }
    }

    roleInputs.forEach(input => {
        input.addEventListener('change', () => updateFields(input.value));
    });

    // Initialize with currently checked
    const checked = document.querySelector('input[name="role"]:checked');
    if (checked) updateFields(checked.value);
}

// ─────────────────────────────────────────────
// SIDEBAR TOGGLE (Mobile)
// ─────────────────────────────────────────────
function initSidebarToggle() {
    const toggleBtn = document.getElementById('sidebar-toggle-btn');
    const sidebar = document.getElementById('app-sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (!toggleBtn || !sidebar) return;

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        if (overlay) overlay.classList.toggle('active');
    });

    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }
}

// ─────────────────────────────────────────────
// ACTIVE NAV HIGHLIGHT
// ─────────────────────────────────────────────
function initActiveNav() {
    const navItems = document.querySelectorAll('.nav-item');
    const currentPath = window.location.pathname;
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && (currentPath === href || currentPath.startsWith(href + '/'))) {
            item.classList.add('active');
        }
    });
}

// ─────────────────────────────────────────────
// ANIMATED STAT NUMBERS
// ─────────────────────────────────────────────
function animateStatNumbers() {
    const statNums = document.querySelectorAll('[data-count]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.getAttribute('data-count'));
                animateNumber(el, target);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    statNums.forEach(el => observer.observe(el));
}

function animateNumber(el, target, duration = 1500) {
    const start = Date.now();
    const startVal = 0;
    function update() {
        const elapsed = Date.now() - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(startVal + (target - startVal) * eased);
        el.textContent = current.toLocaleString() + (el.dataset.suffix || '');
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

// ─────────────────────────────────────────────
// SEARCH / FILTER
// ─────────────────────────────────────────────
function initSearchFilter() {
    const searchInput = document.getElementById('course-search');
    const categoryFilter = document.getElementById('category-filter');
    const courseCards = document.querySelectorAll('.course-card');

    function filterCourses() {
        const searchVal = searchInput ? searchInput.value.toLowerCase() : '';
        const catVal = categoryFilter ? categoryFilter.value.toLowerCase() : '';

        courseCards.forEach(card => {
            const title = (card.dataset.title || '').toLowerCase();
            const category = (card.dataset.category || '').toLowerCase();
            const matchSearch = !searchVal || title.includes(searchVal);
            const matchCat = !catVal || category === catVal;
            card.style.display = (matchSearch && matchCat) ? '' : 'none';
        });
    }

    if (searchInput) searchInput.addEventListener('input', filterCourses);
    if (categoryFilter) categoryFilter.addEventListener('change', filterCourses);
}

// ─────────────────────────────────────────────
// MODALS
// ─────────────────────────────────────────────
function initModals() {
    // Open
    document.querySelectorAll('[data-modal]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.dataset.modal;
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.add('active');
        });
    });

    // Close via overlay click or close button
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.classList.remove('active');
        });
    });

    document.querySelectorAll('[data-close-modal]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal-overlay');
            if (modal) modal.classList.remove('active');
        });
    });
}

// ─────────────────────────────────────────────
// DYNAMIC FORMS
// ─────────────────────────────────────────────
function initDynamicForms() {
    // Password strength indicator
    const passInput = document.getElementById('password');
    const passStrength = document.getElementById('pass-strength');

    if (passInput && passStrength) {
        passInput.addEventListener('input', () => {
            const val = passInput.value;
            let strength = 0;
            if (val.length >= 6) strength++;
            if (/[A-Z]/.test(val)) strength++;
            if (/[0-9]/.test(val)) strength++;
            if (/[^A-Za-z0-9]/.test(val)) strength++;

            const levels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
            const colors = ['', '#ef4444', '#f59e0b', '#3b82f6', '#10b981'];
            passStrength.textContent = levels[strength] || '';
            passStrength.style.color = colors[strength] || '';
        });
    }

    // Confirm password validation
    const confirmPass = document.getElementById('confirm_password');
    if (confirmPass && passInput) {
        confirmPass.addEventListener('input', () => {
            if (confirmPass.value !== passInput.value) {
                confirmPass.style.borderColor = 'var(--danger)';
            } else {
                confirmPass.style.borderColor = 'var(--success)';
            }
        });
    }

    // Form submit loading state
    document.querySelectorAll('form[data-loading]').forEach(form => {
        form.addEventListener('submit', () => {
            const btn = form.querySelector('[type="submit"]');
            if (btn) {
                btn.disabled = true;
                const original = btn.textContent;
                btn.textContent = 'Loading...';
                btn.dataset.original = original;
            }
        });
    });
}

// ─────────────────────────────────────────────
// NAVBAR SCROLL EFFECT
// ─────────────────────────────────────────────
const navbar = document.querySelector('.navbar');
if (navbar) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(15,14,23,0.98)';
            navbar.style.boxShadow = '0 4px 24px rgba(0,0,0,0.4)';
        } else {
            navbar.style.background = 'rgba(15,14,23,0.85)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// ─────────────────────────────────────────────
// ENROLL BUTTON CONFIRM
// ─────────────────────────────────────────────
document.querySelectorAll('.enroll-form').forEach(form => {
    form.addEventListener('submit', (e) => {
        const btn = form.querySelector('button');
        if (btn && btn.dataset.enrolled === 'true') {
            e.preventDefault();
            return;
        }
    });
});

// ─────────────────────────────────────────────
// NOTIFICATION DISMISS
// ─────────────────────────────────────────────
document.querySelectorAll('[data-notif-id]').forEach(btn => {
    btn.addEventListener('click', async () => {
        const id = btn.dataset.notifId;
        try {
            await fetch(`/api/mark-notification-read/${id}`, { method: 'POST' });
            const item = btn.closest('.notif-item');
            if (item) item.classList.remove('unread');
            btn.style.display = 'none';
        } catch (e) {}
    });
});

// ─────────────────────────────────────────────
// SMOOTH SCROLL FOR ANCHOR LINKS
// ─────────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ─────────────────────────────────────────────
// TOOLTIP INIT (custom lightweight tooltips)
// ─────────────────────────────────────────────
document.querySelectorAll('[data-tooltip]').forEach(el => {
    const tip = document.createElement('div');
    tip.className = 'tooltip-box';
    tip.textContent = el.dataset.tooltip;
    tip.style.cssText = `
        position: absolute; background: var(--bg-card2);
        border: 1px solid var(--border-color); color: var(--text-primary);
        font-size: 12px; padding: 6px 10px; border-radius: 6px;
        white-space: nowrap; z-index: 9999; pointer-events: none;
        opacity: 0; transition: opacity 0.2s;
    `;
    document.body.appendChild(tip);

    el.addEventListener('mouseenter', (e) => {
        const rect = el.getBoundingClientRect();
        tip.style.top = `${rect.top + window.scrollY - 36}px`;
        tip.style.left = `${rect.left + rect.width / 2 - tip.offsetWidth / 2}px`;
        tip.style.opacity = '1';
    });
    el.addEventListener('mouseleave', () => { tip.style.opacity = '0'; });
});

console.log('%c EduVerse LMS Loaded ✓', 'color: #6C63FF; font-weight: bold; font-size: 16px;');
