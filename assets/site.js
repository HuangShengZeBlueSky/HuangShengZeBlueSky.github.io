document.querySelectorAll('.surface-explorer').forEach(explorer => {
  const buttons = explorer.querySelectorAll('[data-surface]');
  buttons.forEach(button => button.addEventListener('click', () => {
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    explorer.querySelectorAll('.surface-panel').forEach(panel => {
      panel.hidden = panel.id !== button.dataset.surface;
    });
  }));
});
