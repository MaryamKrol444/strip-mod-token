/* No storage or third-party requests until an explicit playback choice. */
document.querySelectorAll('.video-review').forEach((review) => {
  const button = review.querySelector('.video-load');
  const template = review.querySelector('.video-template');
  const slot = review.querySelector('[data-video-slot]');
  if (!button || !template || !slot) return;
  button.addEventListener('click', () => {
    const fragment = template.content.cloneNode(true);
    slot.replaceChildren(fragment);
    const frame = slot.querySelector('iframe');
    if (frame) frame.focus();
  }, { once: true });
});
