/* =============================================================
   Shawn Wang — interactions
   Vanilla JS, no dependencies.
   ============================================================= */
(function () {
  "use strict";

  /* ---------- current year in footer ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- scroll reveal ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- lightbox ---------- */
  var shots = Array.prototype.slice.call(document.querySelectorAll(".shot"));
  var lightbox = document.getElementById("lightbox");
  var lbImg = document.getElementById("lb-img");
  var lbCount = document.getElementById("lb-count");
  var btnClose = document.getElementById("lb-close");
  var btnPrev = document.getElementById("lb-prev");
  var btnNext = document.getElementById("lb-next");

  if (!lightbox || shots.length === 0) return;

  // Build a list of {src, alt} from the gallery figures.
  var slides = shots.map(function (fig) {
    var img = fig.querySelector("img");
    return {
      src: fig.getAttribute("data-full"),
      alt: img ? img.getAttribute("alt") : ""
    };
  });

  var current = 0;
  var lastFocused = null;

  function preload(i) {
    if (i < 0 || i >= slides.length) return;
    var im = new Image();
    im.src = slides[i].src;
  }

  function render() {
    var slide = slides[current];
    lbImg.src = slide.src;
    lbImg.alt = slide.alt;
    lbCount.textContent =
      String(current + 1).padStart(2, "0") + " / " + String(slides.length).padStart(2, "0");
    // restart the entrance animation
    lbImg.style.animation = "none";
    // force reflow so the animation can replay
    void lbImg.offsetWidth;
    lbImg.style.animation = "";
    preload(current + 1);
    preload(current - 1);
  }

  function open(index) {
    current = index;
    lastFocused = document.activeElement;
    lightbox.hidden = false;
    // next frame → add class for the opacity transition
    requestAnimationFrame(function () {
      lightbox.classList.add("is-open");
    });
    document.body.style.overflow = "hidden";
    render();
    btnClose.focus();
  }

  function close() {
    lightbox.classList.remove("is-open");
    document.body.style.overflow = "";
    window.setTimeout(function () {
      lightbox.hidden = true;
      lbImg.src = "";
    }, 380);
    if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
  }

  function next() { current = (current + 1) % slides.length; render(); }
  function prev() { current = (current - 1 + slides.length) % slides.length; render(); }

  shots.forEach(function (fig, i) {
    fig.addEventListener("click", function () { open(i); });
  });

  btnClose.addEventListener("click", close);
  btnNext.addEventListener("click", next);
  btnPrev.addEventListener("click", prev);

  // Click on the backdrop (but not the image or buttons) closes.
  lightbox.addEventListener("click", function (e) {
    if (e.target === lightbox || e.target.classList.contains("lightbox__stage")) close();
  });

  // Keyboard controls
  document.addEventListener("keydown", function (e) {
    if (lightbox.hidden) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowRight") next();
    else if (e.key === "ArrowLeft") prev();
  });

  // Basic swipe support on touch devices
  var touchX = null;
  lightbox.addEventListener("touchstart", function (e) {
    touchX = e.changedTouches[0].clientX;
  }, { passive: true });
  lightbox.addEventListener("touchend", function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) { dx < 0 ? next() : prev(); }
    touchX = null;
  }, { passive: true });
})();
