const CONTACT = {
  email: "sebastian.aguirre@ug.uchile.cl",
  whatsapp: "56994226803",
};

const navbar = document.querySelector("#navbar");
const navLinks = document.querySelectorAll("#menuPrincipal .nav-link");
const menu = document.querySelector("#menuPrincipal");
const emailLink = document.querySelector("#email-link");
const whatsappLink = document.querySelector("#whatsapp-link");

function updateNavbar() {
  navbar.classList.toggle("scrolled", window.scrollY > 30);
}

function configureContact() {
  emailLink.href = "mailto:" + CONTACT.email;
  document.querySelector("#email-text").textContent = CONTACT.email;

  whatsappLink.href =
    "https://wa.me/" +
    CONTACT.whatsapp +
    "?text=" +
    encodeURIComponent(
      "Hola Sebastián, me interesa conocer el servicio integral de imagen para equipos deportivos.",
    );
  whatsappLink.target = "_blank";
  whatsappLink.rel = "noopener noreferrer";
  document.querySelector("#whatsapp-text").textContent =
    "+" + CONTACT.whatsapp;
}

function closeMobileMenu() {
  const instance = bootstrap.Collapse.getInstance(menu);

  if (instance && window.innerWidth < 1200) {
    instance.hide();
  }
}

function updateActiveLink() {
  const sections = [...document.querySelectorAll("header[id], main section[id]")];
  const current = sections
    .filter((section) => section.getBoundingClientRect().top <= 120)
    .at(-1);

  navLinks.forEach((link) => {
    link.classList.toggle(
      "active",
      current && link.getAttribute("href") === "#" + current.id,
    );
  });
}

window.addEventListener("scroll", () => {
  updateNavbar();
  updateActiveLink();
});

navLinks.forEach((link) => link.addEventListener("click", closeMobileMenu));

configureContact();
updateNavbar();
updateActiveLink();
document.querySelector("#year").textContent = new Date().getFullYear();
