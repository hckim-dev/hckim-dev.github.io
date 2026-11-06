const root = document.documentElement;
root.classList.add('js');

const menuButton = document.querySelector('.mobile-menu');
const navLinks = document.querySelector('.nav-links');

if (menuButton && navLinks) {
  function setMenuOpen(open) {
    menuButton.setAttribute('aria-expanded', String(open));
    navLinks.classList.toggle('open', open);
  }

  menuButton.addEventListener('click', () => {
    setMenuOpen(menuButton.getAttribute('aria-expanded') !== 'true');
  });

  navLinks.addEventListener('click', event => {
    if (event.target.closest('a')) setMenuOpen(false);
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && navLinks.classList.contains('open')) {
      setMenuOpen(false);
      menuButton.focus();
    }
  });
}

const imageDialog = document.querySelector('dialog');

if (imageDialog && typeof imageDialog.showModal === 'function') {
  const zoomButton = imageDialog.querySelector('.zoom-toggle');
  const imageViewport = imageDialog.querySelector('.image-viewport');
  const dialogImage = imageDialog.querySelector('img');
  const originalImageLink = imageDialog.querySelector('.original-image');
  const imageCaption = imageDialog.querySelector('p');
  const closeButton = imageDialog.querySelector('.dialog-close');
  let imageTrigger;

  function setZoomed(expanded) {
    if (expanded) {
      dialogImage.style.width = `${dialogImage.getBoundingClientRect().width * 2}px`;
      dialogImage.style.maxWidth = 'none';
      dialogImage.style.maxHeight = 'none';
    } else {
      dialogImage.style.width = '';
      dialogImage.style.maxWidth = '';
      dialogImage.style.maxHeight = '';
    }
    zoomButton.setAttribute('aria-pressed', String(expanded));
    zoomButton.textContent = expanded ? '화면에 맞추기' : '2배 확대';
    imageViewport.scrollTo(0, 0);
  }

  zoomButton.addEventListener('click', () => {
    setZoomed(zoomButton.getAttribute('aria-pressed') !== 'true');
  });

  document.querySelectorAll('.zoom-link').forEach(link => {
    link.addEventListener('click', event => {
      // Preserve modified clicks for opening the original image in another tab.
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      imageTrigger = link;
      const originalImage = link.querySelector('img');
      dialogImage.src = link.href;
      dialogImage.alt = originalImage.alt;
      originalImageLink.href = link.href;
      imageCaption.textContent = originalImage.alt;
      setZoomed(false);

      // Compensate for classic scrollbars when locking background scrolling.
      root.style.setProperty('--scrollbar-width', `${window.innerWidth - root.clientWidth}px`);
      root.classList.add('image-open');
      imageDialog.showModal();
    });
  });

  closeButton.addEventListener('click', () => imageDialog.close());

  imageDialog.addEventListener('click', event => {
    if (event.target !== imageDialog) return;
    const bounds = imageDialog.getBoundingClientRect();
    const outside = event.clientX < bounds.left || event.clientX > bounds.right ||
      event.clientY < bounds.top || event.clientY > bounds.bottom;
    if (outside) imageDialog.close();
  });

  imageDialog.addEventListener('close', () => {
    root.classList.remove('image-open');
    root.style.removeProperty('--scrollbar-width');
    imageTrigger?.focus({ preventScroll: true });
  });
}
