/* Presupuesta · web pública. Sin dependencias. */
(function () {
  "use strict";
  var reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Cookies: Microsoft Clarity solo con permiso ---------- */
  var CLARITY_ID = "x2haye6mzc";
  var CLAVE = "presupuesta-cookies";
  function leer() { try { return localStorage.getItem(CLAVE); } catch (e) { return null; } }
  function guardar(v) { try { localStorage.setItem(CLAVE, v); } catch (e) { /* modo privado */ } }
  function cargarClarity() {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", CLARITY_ID);
  }
  var aviso = document.getElementById("aviso-cookies");
  var decision = leer();
  if (decision === "si") cargarClarity();
  else if (decision !== "no" && aviso) aviso.hidden = false;
  if (aviso) {
    aviso.addEventListener("click", function (e) {
      var b = e.target.closest("[data-cookies]");
      if (!b) return;
      var v = b.getAttribute("data-cookies");
      guardar(v);
      aviso.hidden = true;
      if (v === "si") cargarClarity();
    });
  }
  document.querySelectorAll("[data-abrir-cookies]").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); if (aviso) aviso.hidden = false; });
  });

  /* ---------- Menú móvil ---------- */
  var botonMenu = document.querySelector(".boton-menu");
  var menu = document.getElementById("menu");
  if (botonMenu && menu) {
    botonMenu.addEventListener("click", function () {
      var abierto = menu.classList.toggle("abierto");
      botonMenu.setAttribute("aria-expanded", String(abierto));
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) { menu.classList.remove("abierto"); botonMenu.setAttribute("aria-expanded", "false"); }
    });
  }

  /* ---------- Cabecera con borde y barra fija móvil al bajar ---------- */
  var cabecera = document.querySelector(".cabecera");
  var barra = document.querySelector(".barra-movil");
  function alDesplazar() {
    var y = window.scrollY;
    if (cabecera) cabecera.classList.toggle("con-borde", y > 8);
    if (barra) barra.classList.toggle("visible", y > 520);
  }
  window.addEventListener("scroll", alDesplazar, { passive: true });
  alDesplazar();

  /* ---------- Aparición suave de secciones ---------- */
  var revelar = document.querySelectorAll(".revelar");
  if ("IntersectionObserver" in window && !reducido) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("visto"); obs.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    revelar.forEach(function (el) { obs.observe(el); });
  } else {
    revelar.forEach(function (el) { el.classList.add("visto"); });
  }

  /* ---------- Precios: mensual / anual ---------- */
  var botonesPlan = document.querySelectorAll("[data-plan]");
  botonesPlan.forEach(function (b) {
    b.addEventListener("click", function () {
      var plan = b.getAttribute("data-plan");
      botonesPlan.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
      document.querySelectorAll("[data-precio-" + plan + "]").forEach(function (el) {
        el.textContent = el.getAttribute("data-precio-" + plan);
      });
      var fundador = document.getElementById("fundador");
      if (fundador) fundador.hidden = plan !== "mensual";
    });
  });

  /* ---------- Demo del móvil: dictar → IA → partidas → PDF ---------- */
  var demo = document.getElementById("demo");
  if (!demo) return;
  var pasos = demo.querySelectorAll(".demo-paso");
  var puntos = document.querySelectorAll(".demo-puntos button");
  var leyenda = document.getElementById("demo-leyenda");
  var textoDictado = document.getElementById("demo-texto");
  var frase = textoDictado.getAttribute("data-frase");
  var filasIA = demo.querySelectorAll(".pensando-fila");
  var progreso = demo.querySelector(".barra-progreso i");
  var partidas = demo.querySelectorAll("[data-partida]");
  var total = document.getElementById("demo-total");
  var leyendas = [
    "1. Dictas el trabajo desde la obra",
    "2. La IA lo desglosa y pone precios de tu zona",
    "3. Repasas las partidas y el total",
    "4. Descargas el PDF y se lo mandas por WhatsApp"
  ];
  var DURACION = [6200, 3400, 5200, 5600];
  var actual = -1, temporizadores = [];

  function limpiar() { temporizadores.forEach(clearTimeout); temporizadores = []; }
  function luego(fn, ms) { temporizadores.push(setTimeout(fn, ms)); }
  function euros(n) {
    // Siempre con punto de miles (Intl en español no lo pone en números de 4 cifras)
    var partes = n.toFixed(2).split(".");
    return partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "," + partes[1] + " €";
  }

  function mostrar(i, auto) {
    limpiar();
    actual = i;
    pasos.forEach(function (p, j) { p.classList.toggle("activo", j === i); });
    puntos.forEach(function (p, j) { p.classList.toggle("activo", j === i); p.setAttribute("aria-current", j === i ? "step" : "false"); });
    leyenda.textContent = leyendas[i];

    if (i === 0) {
      if (reducido) { textoDictado.textContent = frase; }
      else {
        textoDictado.textContent = "";
        var k = 0;
        (function escribir() {
          if (k > frase.length) return;
          textoDictado.textContent = frase.slice(0, k);
          k += 2;
          luego(escribir, 55);
        })();
      }
    }
    if (i === 1) {
      filasIA.forEach(function (f) { f.classList.remove("hecho"); });
      progreso.style.width = "0";
      filasIA.forEach(function (f, j) {
        luego(function () { f.classList.add("hecho"); progreso.style.width = ((j + 1) / filasIA.length * 100) + "%"; }, reducido ? 0 : 450 + j * 700);
      });
    }
    if (i === 2) {
      var suma = 0, objetivo = Number(total.getAttribute("data-total"));
      partidas.forEach(function (p) { p.style.display = "none"; });
      total.textContent = euros(0);
      partidas.forEach(function (p, j) {
        luego(function () {
          p.style.display = "";
          suma += Number(p.getAttribute("data-partida"));
          total.textContent = euros(j === partidas.length - 1 ? objetivo : suma);
        }, reducido ? 0 : 300 + j * 650);
      });
    }
    // Último paso: «Enviado» al poco de mostrar el PDF
    var estado = document.getElementById("demo-estado");
    var enviado = demo.querySelector(".pdf-enviado");
    if (estado) { estado.textContent = "Borrador"; estado.className = "chip chip-pend"; }
    if (enviado) enviado.classList.remove("visto");
    if (i === 3) {
      luego(function () {
        if (estado) { estado.textContent = "Enviado"; estado.className = "chip chip-ok"; }
        if (enviado) enviado.classList.add("visto");
      }, reducido ? 0 : 1400);
    }
    if (auto && !reducido) luego(function () { mostrar((i + 1) % pasos.length, true); }, DURACION[i]);
  }

  puntos.forEach(function (p, j) { p.addEventListener("click", function () { mostrar(j, false); }); });

  // Solo se anima cuando el móvil está a la vista (ahorra batería y CPU)
  if ("IntersectionObserver" in window && !reducido) {
    var enMarcha = false;
    new IntersectionObserver(function (entradas) {
      var visible = entradas[0].isIntersecting;
      if (visible && !enMarcha) { enMarcha = true; mostrar(actual < 0 ? 0 : actual, true); }
      if (!visible && enMarcha) { enMarcha = false; limpiar(); }
    }, { threshold: 0.25 }).observe(demo);
  } else {
    mostrar(2, false);
  }
})();
