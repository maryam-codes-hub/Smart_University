const links = document.querySelectorAll('.nav-links a');
const sections = document.querySelectorAll('section[id]');

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            links.forEach((link) => link.classList.remove('active'));
            const current = document.querySelector(
                `.nav-links a[href$="#${entry.target.id}"]`
            );
            if (current) current.classList.add('active');
        }
    });
}, { rootMargin: '-40% 0px -55% 0px' });

sections.forEach((section) => observer.observe(section));