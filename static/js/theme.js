(function () {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('theme') || 'dark';

  root.setAttribute('data-theme', savedTheme);

  const btn = document.getElementById('themeToggle');
  if (!btn) return;

  btn.addEventListener('click', function () {
    const current = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', current);
    localStorage.setItem('theme', current);
  });
})();
