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
  document.querySelectorAll('.zoom-link').forEach(link => link.addEventListener('click', event => {
    event.preventDefault(); trigger = link;
    const original = link.querySelector('img');
    dialog.querySelector('img').src = link.href;
    dialog.querySelector('img').alt = original.alt;
    dialog.querySelector('p').textContent = original.alt;
    dialog.showModal();
  }));
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => trigger?.focus());
}
