// Mobilmenu + diskret baggrund på topmenuen ved scroll
(function () {
  var header = document.getElementById('site-header');
  var toggle = document.getElementById('menu-toggle');
  var menu = document.getElementById('top-menu');

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  function onScroll() {
    if (window.scrollY > 40) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
