const menu = document.querySelector('.menu-button');
const nav = document.querySelector('.nav');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
});
nav?.addEventListener('click', event => {
  if (event.target.closest('a')) {
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('open');
  }
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu) {
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('open');
  }
});
const dialog = document.querySelector('.lightbox');
document.querySelectorAll('.image-open').forEach(button => {
  button.addEventListener('click', () => {
    const image = button.querySelector('img');
    const target = dialog.querySelector('img');
    target.src = image.currentSrc || image.src;
    target.alt = image.alt;
    dialog.querySelector('p').textContent = button.closest('figure')?.querySelector('figcaption')?.textContent || image.alt;
    dialog.showModal();
  });
});
dialog?.querySelector('.close-button').addEventListener('click', () => dialog.close());
dialog?.addEventListener('click', event => {
  if (event.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  }
});
const sections = document.querySelectorAll('.feature-section');
if (sections.length && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      document.querySelectorAll('.contents a').forEach(link => {
        if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
    }
  }, {rootMargin: '-15% 0px -60% 0px'});
  sections.forEach(section => observer.observe(section));
}
// Preserve entry points from the previous single-page site (now the white-paper series).
if (location.pathname.endsWith('index.html') || location.pathname.endsWith('/')) {
  const targets = {
    technology: 'whitepapers/wp01-krylov-reduction.html',
    results: 'whitepapers/wp01-krylov-reduction.html#results',
    visualization: 'whitepapers/wp02-fullchip-visualization.html',
    features: '#capabilities',
    agentic: '#capabilities'
  };
  const target = targets[location.hash.slice(1)];
  if (target) location.replace(target);
}
