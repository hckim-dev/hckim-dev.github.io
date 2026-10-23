document.documentElement.classList.add('js');
const menu = document.querySelector('.mobile-menu');
const links = document.querySelector('.nav-links');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  links.classList.toggle('open', open);
});
links?.addEventListener('click', event => {
  if (event.target.closest('a')) {
    menu.setAttribute('aria-expanded', 'false');
    links.classList.remove('open');
  }
});
document.addEventListener('keydown', event => {
  if(event.key === 'Escape' && links?.classList.contains('open')) {
    links.classList.remove('open'); menu.setAttribute('aria-expanded','false'); menu.focus();
  }
});
const dialog = document.querySelector('dialog');
if (dialog && typeof dialog.showModal === 'function') {
  let trigger;
  const zoom = dialog.querySelector('.zoom-toggle');
  const viewport = dialog.querySelector('.image-viewport');
  const picture = dialog.querySelector('img');
  zoom.addEventListener('click', () => {
    const expanded = zoom.getAttribute('aria-pressed') !== 'true';
    if (expanded) {
      picture.style.width = `${picture.getBoundingClientRect().width * 2}px`;
      picture.style.maxWidth = 'none';
      picture.style.maxHeight = 'none';
    } else {
      picture.removeAttribute('style');
    }
    zoom.setAttribute('aria-pressed', String(expanded));
    zoom.textContent = expanded ? '화면에 맞추기' : '2배 확대';
    viewport.scrollTo(0, 0);
  });
  document.querySelectorAll('.zoom-link').forEach(link => link.addEventListener('click', event => {
    event.preventDefault(); trigger = link;
    const original = link.querySelector('img');
    dialog.querySelector('img').src = link.href;
    dialog.querySelector('img').alt = original.alt;
    picture.removeAttribute('style');
    zoom.setAttribute('aria-pressed', 'false');
    zoom.textContent = '2배 확대';
    dialog.querySelector('.original-image').href = link.href;
    dialog.querySelector('p').textContent = original.alt;
    dialog.showModal();
  }));
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => trigger?.focus());
}
