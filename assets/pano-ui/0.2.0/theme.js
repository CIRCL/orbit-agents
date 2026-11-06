/* Pano UI: system by default; preferences stay in this browser origin. */
(() => {
  'use strict';
  const key = 'pano-theme';
  const valid = value => value === 'light' || value === 'dark' ? value : 'system';
  let preference = 'system';
  try { preference = valid(localStorage.getItem(key)); } catch (_) { /* Storage may be disabled. */ }
  let select;
  function apply(value) {
    preference = valid(value);
    if (preference === 'system') document.documentElement.removeAttribute('data-pano-theme');
    else document.documentElement.setAttribute('data-pano-theme', preference);
    if (select) select.value = preference;
  }
  apply(preference);
  function mount() {
    const control = document.createElement('label');
    control.className = 'pano-theme-control';
    const text = document.createElement('span');
    text.textContent = 'Theme';
    select = document.createElement('select');
    select.setAttribute('aria-label', 'Color theme');
    for (const [value, title] of [['system', 'System'], ['light', 'Light'], ['dark', 'Dark']]) {
      const option = document.createElement('option');
      option.value = value; option.textContent = title; select.append(option);
    }
    select.value = preference;
    select.addEventListener('change', () => {
      apply(select.value);
      try {
        if (preference === 'system') localStorage.removeItem(key);
        else localStorage.setItem(key, preference);
      } catch (_) { /* The current page still works without persistence. */ }
    });
    control.append(text, select);
    document.body.append(control);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once: true});
  else mount();
  window.addEventListener('storage', event => {
    if (event.key === key || event.key === null) apply(event.newValue);
  });
})();
