// =====================================================
//  main.js  –  FitPlanner Frontend Logic
// =====================================================

// ── Toggle password visibility ────────────────────
function togglePassword(fieldId) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  field.type = field.type === "password" ? "text" : "password";
}

// ── Auto-dismiss flash messages after 5 seconds ───
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".flash").forEach(flash => {
    setTimeout(() => {
      flash.style.transition = "opacity .4s ease, transform .4s ease";
      flash.style.opacity    = "0";
      flash.style.transform  = "translateY(-8px)";
      setTimeout(() => flash.remove(), 400);
    }, 5000);
  });

  // Animate exercise table rows
  document.querySelectorAll(".exercise-row").forEach((row, i) => {
    row.style.animationDelay = `${i * 0.07}s`;
  });

  // Highlight active nav link
  const path = window.location.pathname;
  document.querySelectorAll(".nav-link").forEach(link => {
    if (link.getAttribute("href") === path) {
      link.style.color = "#e8e8ff";
      link.style.fontWeight = "700";
    }
  });
});
