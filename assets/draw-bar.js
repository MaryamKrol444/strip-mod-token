/* Dismissal is page-local. No cookies, storage, timers or third-party requests. */
(() => {
  const bar = document.querySelector('.draw-bar');
  const close = bar?.querySelector('.draw-bar-close');
  if (!bar || !close) return;
  const root = document.documentElement;
  let previousFocus = null;
  const updateSpace = () => {
    root.style.setProperty('--draw-bar-space', `${bar.hidden ? 0 : Math.ceil(bar.getBoundingClientRect().height)}px`);
  };
  const onFocus = (event) => {
    if (bar.contains(event.target)) return;
    previousFocus = event.target;
    // Keep keyboard-focused article/footer links above the fixed notice.
    const bounds = event.target.getBoundingClientRect();
    // A skip link can focus the entire main landmark: do not scroll its bottom
    // into view and accidentally jump the reader to the end of the article.
    if (bounds.height > window.innerHeight / 2) return;
    const top = bar.getBoundingClientRect().top;
    if (!bar.hidden && bounds.bottom > top - 16) {
      window.scrollBy({ top: bounds.bottom - top + 16, behavior: 'instant' });
    }
  };
  const observer = typeof ResizeObserver === 'function' ? new ResizeObserver(updateSpace) : null;
  observer?.observe(bar);
  window.addEventListener('resize', updateSpace);
  document.addEventListener('focusin', onFocus);
  close.addEventListener('click', () => {
    const returnFocus = bar.contains(document.activeElement);
    bar.hidden = true;
    document.body.classList.remove('has-draw-bar');
    updateSpace();
    observer?.disconnect();
    window.removeEventListener('resize', updateSpace);
    document.removeEventListener('focusin', onFocus);
    if (returnFocus) {
      const target = previousFocus?.isConnected ? previousFocus : document.querySelector('#main');
      if (target) {
        if (!target.hasAttribute('tabindex') && target.tagName === 'MAIN') target.tabIndex = -1;
        target.focus({ preventScroll: true });
      }
    }
  }, { once: true });
  close.hidden = false;
  updateSpace();
})();
