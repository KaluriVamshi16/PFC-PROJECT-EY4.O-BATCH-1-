// =============================
// Section Navigation
// =============================
const navLinks = document.querySelectorAll('.nav-links a');
const sections = document.querySelectorAll('section');

navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const target = link.getAttribute('data-section');

    sections.forEach(sec => {
      if (sec.id === target) {
        // Keep flex for Home (hero), block for others
        sec.style.display = (sec.id === 'home') ? 'flex' : 'block';
      } else {
        sec.style.display = 'none';
      }
    });

    // Scroll to top when section changes
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});

// Show only Home by default
sections.forEach(sec => {
  if (sec.id !== 'home') {
    sec.style.display = 'none';
  } else {
    sec.style.display = 'flex'; // ensures hero stays centered
  }
});

// =============================
// Menu Toggle for Navbar
// =============================
const menuBtn = document.getElementById("menu-btn");
const navLinksList = document.getElementById("nav-links");
const menuIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", () => {
  navLinksList.classList.toggle("open");
  const isOpen = navLinksList.classList.contains("open");
  menuIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-3-line");
});

navLinksList.addEventListener("click", () => {
  navLinksList.classList.remove("open");
  menuIcon.setAttribute("class", "ri-menu-3-line");
});

// =============================
// Features Menu Toggle
// =============================
const featuresBtn = document.getElementById("menu-features-btn");
const featuresMenu = document.getElementById("features-menu");

if(featuresBtn && featuresMenu){
  featuresBtn.addEventListener("click", (e) => {
    e.preventDefault();
    featuresMenu.classList.toggle("open");
  });
}

// Optional: close features menu if clicked outside
document.addEventListener('click', (e) => {
  if(featuresMenu && !featuresMenu.contains(e.target) && e.target !== featuresBtn){
    featuresMenu.classList.remove('open');
  }
});

// =============================
// Scroll Reveal Animations
// =============================
const srOpts = { distance: "50px", origin: "bottom", duration: 1500 };
if (typeof ScrollReveal !== "undefined") {
  ScrollReveal().reveal(".hero-content h1", { ...srOpts, delay: 500 });
  ScrollReveal().reveal(".hero-content p", { ...srOpts, delay: 1000 });
  ScrollReveal().reveal(".btn", { ...srOpts, delay: 1500 });
  ScrollReveal().reveal(".socials a", { ...srOpts, delay: 2000, interval: 300 });
}

// =============================
// Register & Login Modals
// =============================
const registerBtn = document.getElementById("registerBtn");
const loginBtn = document.getElementById("loginBtn");
const registerModal = document.getElementById("registerModal");
const loginModal = document.getElementById("loginModal");
const closeBtns = document.querySelectorAll(".close");
const toLogin = document.getElementById("toLogin");

// Open Register Modal
if(registerBtn){
  registerBtn.onclick = () => {
    registerModal.style.display = "block";
    loginModal.style.display = "none";
  };
}

// Open Login Modal
if(loginBtn){
  loginBtn.onclick = () => {
    loginModal.style.display = "block";
    registerModal.style.display = "none";
  };
}

// Close buttons
closeBtns.forEach(btn => {
  btn.onclick = () => {
    registerModal.style.display = "none";
    loginModal.style.display = "none";
  };
});

// Switch Register → Login
if(toLogin){
  toLogin.onclick = (e) => {
    e.preventDefault();
    registerModal.style.display = "none";
    loginModal.style.display = "block";
  };
}

// Close modal if clicking outside
window.onclick = (e) => {
  if(e.target === registerModal) registerModal.style.display = "none";
  if(e.target === loginModal) loginModal.style.display = "none";
};
