"""
Genera la web pública de Presupuesta (HTML estático para Hostinger).

    python3 _fuente/generar.py

Crea/actualiza: index.html, ejemplos/*.html, aviso-legal.html, politica-privacidad.html,
condiciones.html, 404.html, sitemap.xml, llms.txt y llms-full.txt.
Edita los textos aquí, en ejemplos.py o en las plantillas de _fuente/ y vuelve a ejecutarlo.
La carpeta _fuente no hace falta subirla a Hostinger (y el .htaccess la bloquea por si acaso).
"""
import datetime as dt
import html
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "_fuente"))
from ejemplos import EJEMPLOS  # noqa: E402
from textos import PREGUNTAS_INICIO, FUNDADOR, LEGAL  # noqa: E402

# ---------------------------------------------------------------- Datos fijos
WEB = "https://presupuesta.net"
APP = "https://panel.presupuesta.net"
REGISTRO = f"{APP}/registro"
ENTRAR = f"{APP}/entrar"
ESTUDIOS = "https://estudios.presupuesta.net"
WHATSAPP = "34652679391"
WHATSAPP_VISIBLE = "652 67 93 91"
EMAIL = "asistente@presupuesta.net"
HOY = dt.date.today().isoformat()
PUBLICADO = "2026-08-31"
VERSION = HOY.replace("-", "")
PRECIO_MES, PRECIO_ANO = 24.90, 249
PRECIO_FUNDADOR = 14.90

e = html.escape


def euros(n: float, decimales=True) -> str:
    entero, dec = f"{n:,.2f}".split(".")
    entero = entero.replace(",", ".")
    return f"{entero},{dec} €" if decimales or dec != "00" else f"{entero} €"


def cifra(n: float) -> str:
    return (f"{n:.2f}".rstrip("0").rstrip(".")).replace(".", ",")


def wa(texto: str) -> str:
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(texto)}"


# ---------------------------------------------------------------- Iconos (trazos tipo Lucide)
ICONOS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/>',
    "chispas": '<path d="M9.9 14.1 12 21l2.1-6.9L21 12l-6.9-2.1L12 3 9.9 9.9 3 12z"/>',
    "mapa": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "documento": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "personas": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "cartera": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    "historial": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
    "subir": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
    "bajar": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "mensaje": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "reloj": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "arena": '<path d="M5 22h14"/><path d="M5 2h14"/><path d="M17 22v-4.17a2 2 0 0 0-.59-1.42L12 12l-4.41 4.41A2 2 0 0 0 7 17.83V22"/><path d="M7 2v4.17a2 2 0 0 0 .59 1.42L12 12l4.41-4.41A2 2 0 0 0 17 6.17V2"/>',
    "escudo": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "tarjeta": '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20"/>',
    "flecha": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "porcentaje": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "regalo": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    "movil": '<rect width="14" height="20" x="5" y="2" rx="2"/><path d="M12 18h.01"/>',
    "varita": '<path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72"/><path d="m14 7 3 3"/>',
    "casa": '<path d="M3 10 12 3l9 7v10a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "telefono": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
}


def icono(nombre: str, extra: str = "") -> str:
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"{extra}>{ICONOS[nombre]}</svg>')


LOGO = ('<svg viewBox="0 0 512 512" aria-hidden="true"><rect width="512" height="512" rx="116" fill="#C2410C"/>'
        '<path transform="translate(-20 -12)" fill="#FFFFFF" fill-rule="evenodd" d="M 150 232 A 126 126 0 1 1 226 347.6 '
        'L 226 392 Q 226 404 214 408 L 150 430 Z M 276 178 A 54 54 0 1 0 276.01 178 Z"/></svg>')

# ---------------------------------------------------------------- Bloques comunes
def cabecera(base: str) -> str:
    inicio = base or "/"
    return f"""<a class="saltar" href="#contenido">Saltar al contenido</a>
<div class="franja">Los 20 primeros pagan <strong>14,90 € al mes para siempre</strong> con el código FUNDADOR · <a href="{REGISTRO}">Empezar gratis →</a></div>
<header class="cabecera">
  <div class="contenedor cabecera-dentro">
    <a href="{inicio}" class="marca" aria-label="Presupuesta, ir al inicio">{LOGO}<span>Presupuesta</span></a>
    <ul id="menu" class="menu">
      <li><a href="{base}#como-funciona">Cómo funciona</a></li>
      <li><a href="{base}#funciones">Funciones</a></li>
      <li><a href="{base}ejemplos/">Ejemplos</a></li>
      <li><a href="{base}#precios">Precios</a></li>
      <li><a href="{base}#preguntas">Preguntas</a></li>
    </ul>
    <div class="acciones-cabecera">
      <a href="{ENTRAR}" class="enlace-entrar">Entrar</a>
      <a href="{REGISTRO}" class="btn btn-principal">Probar gratis</a>
      <button class="boton-menu" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">{icono("menu")}</button>
    </div>
  </div>
</header>"""


def pie(base: str) -> str:
    ej = "".join(f'<li><a href="{base}ejemplos/{x["slug"]}.html">{e(x["corto"])}</a></li>' for x in EJEMPLOS[:6])
    return f"""<footer class="pie">
  <div class="contenedor">
    <div class="pie-grid">
      <div>
        <a href="{base or '/'}" class="marca">{LOGO}<span>Presupuesta</span></a>
        <p>Presupuestos de obra con IA para autónomos y pymes de reformas e instalaciones. Hecho en Ermua (Bizkaia) por <a href="{ESTUDIOS}">Presupuesta Estudios</a>.</p>
      </div>
      <div>
        <h4>Producto</h4>
        <ul>
          <li><a href="{base}#como-funciona">Cómo funciona</a></li>
          <li><a href="{base}#funciones">Funciones</a></li>
          <li><a href="{base}#precios">Precios</a></li>
          <li><a href="{base}#preguntas">Preguntas frecuentes</a></li>
          <li><a href="{REGISTRO}">Crear cuenta gratis</a></li>
          <li><a href="{ENTRAR}">Entrar</a></li>
        </ul>
      </div>
      <div>
        <h4>Ejemplos</h4>
        <ul>{ej}<li><a href="{base}ejemplos/">Ver todos los ejemplos</a></li></ul>
      </div>
      <div>
        <h4>Contacto y legal</h4>
        <ul>
          <li><a href="https://wa.me/{WHATSAPP}">WhatsApp {WHATSAPP_VISIBLE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{base}#quien">Quién hay detrás</a></li>
          <li><a href="{base}aviso-legal.html">Aviso legal</a></li>
          <li><a href="{base}politica-privacidad.html">Privacidad y cookies</a></li>
          <li><a href="{base}condiciones.html">Condiciones de uso</a></li>
          <li><a href="#" data-abrir-cookies>Configurar cookies</a></li>
        </ul>
      </div>
    </div>
    <div class="pie-legal">
      <span>© {dt.date.today().year} Presupuesta · Ermua, Bizkaia (España)</span>
      <span><a href="{base}llms.txt">llms.txt</a> · <a href="{base}sitemap.xml">Mapa del sitio</a></span>
    </div>
  </div>
</footer>
<div class="barra-movil" role="complementary" aria-label="Probar Presupuesta">
  <div><strong>14 días gratis, sin tarjeta</strong><small>Luego 24,90 € + IVA/mes · sin permanencia</small></div>
  <a href="{REGISTRO}" class="btn btn-principal">Probar</a>
</div>
<div id="aviso-cookies" class="aviso-cookies" role="dialog" aria-label="Cookies" hidden>
  <p><strong>¿Nos dejas medir cómo se usa la web?</strong> Usamos Microsoft Clarity para ver qué partes se entienden y cuáles no. Sin publicidad. <a href="{base}politica-privacidad.html#cookies">Más información</a>.</p>
  <div><button class="btn btn-secundario" type="button" data-cookies="no">No, gracias</button><button class="btn btn-principal" type="button" data-cookies="si">Aceptar</button></div>
</div>
<script src="{base}assets/site.js?v={VERSION}" defer></script>"""


def cabeza(titulo, descripcion, ruta, base, jsonld=None, tipo="website", indexar=True):
    url = f"{WEB}/{ruta}"
    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")) + "</script>"
    robots = "index, follow, max-snippet:-1, max-image-preview:large" if indexar else "noindex, follow"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#C2410C">
<meta name="author" content="Presupuesta">
<meta property="og:type" content="{tipo}">
<meta property="og:site_name" content="Presupuesta">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{WEB}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Presupuesta: presupuestos de obra con IA">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{base}logo.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="{base}logo.png">
<link rel="manifest" href="{base}site.webmanifest">
<link rel="alternate" type="text/plain" title="Información para asistentes de IA" href="{WEB}/llms.txt">
<link rel="preload" href="{base}assets/fuentes/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fuentes/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/site.css?v={VERSION}">
{ld}
</head>
<body>"""


ORGANIZACION = {
    "@type": "Organization", "@id": f"{WEB}/#organizacion", "name": "Presupuesta", "url": WEB,
    "logo": {"@type": "ImageObject", "url": f"{WEB}/logo.png", "width": 512, "height": 512},
    "email": EMAIL, "telephone": f"+{WHATSAPP}",
    "address": {"@type": "PostalAddress", "addressLocality": "Ermua", "postalCode": "48260", "addressRegion": "Bizkaia", "addressCountry": "ES"},
    "areaServed": {"@type": "Country", "name": "España"},
    "founder": {"@id": f"{WEB}/#fundador"},
    "parentOrganization": {"@type": "Organization", "name": "Presupuesta Estudios", "url": ESTUDIOS},
    "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "telephone": f"+{WHATSAPP}", "email": EMAIL, "availableLanguage": "es", "areaServed": "ES"},
    "sameAs": [ESTUDIOS],
}
PERSONA = {"@type": "Person", "@id": f"{WEB}/#fundador", "name": FUNDADOR["nombre"], "jobTitle": "Fundador de Presupuesta",
           "worksFor": {"@id": f"{WEB}/#organizacion"}, "address": {"@type": "PostalAddress", "addressLocality": "Ermua", "addressCountry": "ES"}}
if FUNDADOR.get("foto"):
    PERSONA["image"] = f"{WEB}/{FUNDADOR['foto']}"


def migas(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def faq_ld(preguntas):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preguntas]}


def preguntas_html(preguntas, abrir_primera=False):
    return "".join(
        f'<details class="pregunta"{" open" if abrir_primera and i == 0 else ""}><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>'
        for i, (q, a) in enumerate(preguntas))


# ---------------------------------------------------------------- Cálculos de los ejemplos
def calcular(x):
    capitulos = []
    base = 0
    for c in x["capitulos"]:
        filas = []
        for d, cant, ud, precio, origen in c["partidas"]:
            importe = round(cant * precio, 2)
            filas.append({"desc": d, "cant": cant, "ud": ud, "precio": precio, "importe": importe, "origen": origen})
        sub = round(sum(f["importe"] for f in filas), 2)
        base += sub
        capitulos.append({"titulo": c["titulo"], "filas": filas, "subtotal": sub})
    base = round(base, 2)
    iva = round(base * x["iva"] / 100, 2)
    total = round(base + iva, 2)
    pagos, acumulado = [], 0
    for i, (concepto, pct) in enumerate(x["pagos"]):
        importe = round(total - acumulado, 2) if i == len(x["pagos"]) - 1 else round(total * pct / 100, 2)
        acumulado = round(acumulado + importe, 2)
        pagos.append((concepto, pct, importe))
    return capitulos, base, iva, total, pagos


# ---------------------------------------------------------------- Página de ejemplo
def pagina_ejemplo(x):
    base = "../"
    capitulos, bimp, iva, total, pagos = calcular(x)
    x["_total"] = total
    url = f"{WEB}/ejemplos/{x['slug']}.html"

    filas_html = ""
    for ci, c in enumerate(capitulos, 1):
        filas_html += f'<div class="capitulo-titulo">{ci}. {e(c["titulo"])}</div><table class="partidas"><thead><tr><th>Partida</th><th>Cantidad</th><th>Precio</th><th>Importe</th></tr></thead><tbody>'
        for fi, f in enumerate(c["filas"], 1):
            chip = '<span class="chip chip-zona" title="Precio de mercado ajustado a la provincia de la obra">ZONA</span>' if f["origen"] == "zona" else '<span class="chip chip-tu" title="Tu precio, aprendido de presupuestos anteriores">TU</span>'
            filas_html += (f'<tr><td><span class="num-partida">{ci}.{fi}</span>{e(f["desc"])} {chip}</td>'
                           f'<td class="cant">{cifra(f["cant"])} {e(f["ud"])}</td><td class="precio">{euros(f["precio"])}</td><td>{euros(f["importe"])}</td></tr>')
        filas_html += "</tbody></table>"

    resumen_caps = "".join(f'<div class="pdf-lin"><span>{i}. {e(c["titulo"])}</span><span>{euros(c["subtotal"])}</span></div>' for i, c in enumerate(capitulos, 1))
    pagos_pdf = "<br>".join(f"{e(con)} ({pct} %): <b>{euros(imp)}</b>" for con, pct, imp in pagos)

    cobrado_hasta, linea_cobros, acumulado_pct = x["cobrado_pct"], "", 0
    for con, pct, imp in pagos:
        acumulado_pct += pct
        cobrado = acumulado_pct <= cobrado_hasta
        estado = '<span class="chip chip-ok">Cobrado</span>' if cobrado else '<span class="chip chip-pend">Pendiente</span>'
        linea_cobros += f'<div class="cobro-linea"><span>{e(con)} · {pct} %</span><span><b>{euros(imp)}</b> {estado}</span></div>'
    te_deben = round(sum(imp for (con, pct, imp), acc in zip(pagos, _acumulados(pagos)) if acc > cobrado_hasta), 2)

    otros = "".join(f'<li><a href="{o["slug"]}.html">{e(o["h1"])}</a></li>' for o in EJEMPLOS if o is not x)
    revisar = "".join(f"<li><span>{e(r)}</span></li>" for r in x["revisar"])
    problema = "".join(f"<p>{e(p)}</p>" for p in x["problema"])
    emp = x["empresa"]
    validez = (dt.date.fromisoformat(HOY) + dt.timedelta(days=30)).strftime("%d/%m/%Y")
    fecha = dt.date.fromisoformat(HOY).strftime("%d/%m/%Y")

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": f"{url}#articulo", "headline": x["h1"], "description": x["description"], "inLanguage": "es-ES",
         "datePublished": PUBLICADO, "dateModified": HOY, "mainEntityOfPage": url, "image": f"{WEB}/og-image.png",
         "author": {"@id": f"{WEB}/#fundador"}, "publisher": {"@id": f"{WEB}/#organizacion"},
         "about": f"Presupuesto de {x['oficio'].lower()}"},
        migas([("Inicio", f"{WEB}/"), ("Ejemplos", f"{WEB}/ejemplos/"), (x["h1"], url)]),
        faq_ld(x["preguntas"]), ORGANIZACION, PERSONA]}

    titulo = x['title'] if len(x['title']) > 50 else x['title'] + ' | Presupuesta'
    cuerpo = f"""{cabeza(titulo, x['description'], f"ejemplos/{x['slug']}.html", base, ld, tipo='article')}
{cabecera(base)}
<main id="contenido">
  <section class="ejemplo-hero">
    <div class="contenedor">
      <ol class="miga" aria-label="Estás en"><li><a href="{base}">Inicio</a></li><li><a href="./">Ejemplos</a></li><li aria-current="page">{e(x['oficio'])}</li></ol>
      <span class="chip chip-marca">{e(x['oficio'])}</span>
      <h1>{e(x['h1'])}</h1>
      <p class="entradilla">{e(x['entradilla'])}</p>
      <div class="resumen-obra">
        <span>📍 <b>{e(x['ciudad'])}</b></span><span>📐 <b>{e(x['superficie'])}</b></span>
        <span>Base <b>{euros(bimp)}</b></span><span>IVA <b>{x['iva']} %</b></span><span>Total <b>{euros(total)}</b></span>
      </div>
    </div>
  </section>
  <div class="contenedor articulo">
    <div class="articulo-cuerpo">
      <section class="tarjeta bloque-aviso" aria-labelledby="t-problema">
        <h2 id="t-problema">Dónde se pierde dinero</h2>
        {problema}
      </section>

      <section class="dictado-bloque" aria-labelledby="t-dictado">
        <span class="chip">{icono('mic', ' width="14" height="14"')} Lo que dicta el profesional</span>
        <h2 id="t-dictado" class="sr-only">Lo que dicta el profesional</h2>
        <blockquote>{e(x['dictado'])}</blockquote>
        <p>{e(x['nota_ia'])}</p>
      </section>

      <section class="presupuesto-tabla" aria-labelledby="t-partidas">
        <div class="presupuesto-cab"><h2 id="t-partidas">Las partidas que propone Presupuesta</h2><span class="chip chip-pend">Borrador</span></div>
        {filas_html}
        <div class="totales">
          <div><span>Base imponible</span><span>{euros(bimp)}</span></div>
          <div><span>IVA {x['iva']} %</span><span>{euros(iva)}</span></div>
          <div class="total"><span>Total</span><span>{euros(total)}</span></div>
        </div>
      </section>
      <p class="aviso-ejemplo"><span class="chip chip-zona">ZONA</span> precio de mercado ajustado a la provincia de la obra · <span class="chip chip-tu">TU</span> precio aprendido de tus presupuestos anteriores. Los precios son orientativos: siempre los repasas y decides tú.</p>

      <section aria-labelledby="t-pdf">
        <h2 id="t-pdf">Así le llega al cliente</h2>
        <p style="margin-bottom:18px">Un PDF con tu logo, tus datos fiscales, numeración automática, validez, IVA desglosado, forma de pago e IBAN, y un espacio para el conforme del cliente.</p>
        <div class="pdf-maqueta" style="--pdf-color:{emp['color']}">
          <div class="pdf-cab">
            <div class="pdf-emisor"><span class="pdf-logo" style="display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800">{e(emp['iniciales'])}</span><div><strong>{e(emp['nombre'])}</strong><small>{e(emp['datos'])}<br>{e(emp['contacto'])}</small></div></div>
            <div class="pdf-num"><small>PRESUPUESTO</small><b>{e(x['numero'])}</b><small>Fecha {fecha} · Válido hasta {validez}</small></div>
          </div>
          <h4>Cliente y obra</h4>
          <p>{e(x['cliente'])} · {e(x['obra'])}</p>
          <h4>Resumen por capítulos</h4>
          {resumen_caps}
          <div class="pdf-lin"><span>Base imponible</span><span>{euros(bimp)}</span></div>
          <div class="pdf-lin"><span>IVA {x['iva']} %</span><span>{euros(iva)}</span></div>
          <div class="pdf-tot"><span>TOTAL</span><span>{euros(total)}</span></div>
          <div class="pdf-pago"><small>FORMA DE PAGO · Transferencia a ES00 0000 0000 0000 0000 0000</small>{pagos_pdf}</div>
          <div class="pdf-firma"><div>Conforme del cliente · firma y fecha</div><div>{e(emp['nombre'])}</div></div>
        </div>
        <p class="aviso-ejemplo" style="margin-top:10px">Empresa, cliente, NIF e IBAN son datos de ejemplo ficticios.</p>
      </section>

      <section class="tarjeta" aria-labelledby="t-revisar">
        <h2 id="t-revisar">Antes de enviarlo, revisa</h2>
        <ul class="lista-revisar">{revisar}</ul>
      </section>

      <section class="tarjeta" aria-labelledby="t-cobros">
        <h2 id="t-cobros">Y después, a cobrar</h2>
        <p style="margin-bottom:16px">Cuando el cliente acepta, apuntas cada cobro y el panel te dice en todo momento lo que te deben.</p>
        <div class="cobro-bloque">{linea_cobros}
          <div class="cobro-linea" style="background:var(--brand-tint)"><span><b>Te deben</b></span><b>{euros(te_deben)}</b></div>
        </div>
      </section>

      <section aria-labelledby="t-preguntas">
        <h2 id="t-preguntas">Preguntas frecuentes</h2>
        <div class="preguntas">{preguntas_html(x['preguntas'])}</div>
      </section>

      <section class="tarjeta seccion-oscura" style="border:0">
        <h2 style="color:#fff">Haz el tuyo en un minuto</h2>
        <p style="color:var(--dark-ink);margin:8px 0 20px">Dicta el trabajo, repasa las partidas y envía el PDF. 14 días gratis, sin tarjeta.</p>
        <a href="{REGISTRO}" class="btn btn-principal btn-grande">Probar Presupuesta gratis {icono('flecha')}</a>
      </section>
    </div>

    <aside class="lateral" aria-label="Prueba Presupuesta y más ejemplos">
      <div class="tarjeta">
        <h3>Este presupuesto, dictado en un minuto</h3>
        <p>Presupuesta desglosa el trabajo con precios de tu provincia y aprende los tuyos.</p>
        <a href="{REGISTRO}" class="btn btn-principal">Probar 14 días gratis</a>
        <p style="margin:12px 0 0;font-size:14px">Sin tarjeta · Sin permanencia</p>
      </div>
      <div class="tarjeta">
        <h3>Más ejemplos</h3>
        <ul>{otros}</ul>
      </div>
    </aside>
  </div>
</main>
{pie(base)}
</body>
</html>
"""
    return cuerpo


def _acumulados(pagos):
    acc, salida = 0, []
    for _, pct, _ in pagos:
        acc += pct
        salida.append(acc)
    return salida


def tarjeta_ejemplo(x, base):
    return (f'<a class="ejemplo-tarjeta" href="{base}ejemplos/{x["slug"]}.html"><span class="chip chip-marca">{e(x["oficio"])}</span>'
            f'<h3>{e(x["h1"])}</h3><p>{e(x["entradilla"])}</p>'
            f'<div class="ejemplo-pie"><b>{euros(x["_total"])}</b><span>Ver ejemplo {icono("flecha", " width=\"16\" height=\"16\"")}</span></div></a>')


def pagina_indice_ejemplos():
    base = "../"
    url = f"{WEB}/ejemplos/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url, "name": "Ejemplos de presupuestos de obra y reformas", "url": url, "inLanguage": "es-ES",
         "publisher": {"@id": f"{WEB}/#organizacion"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f"{WEB}/ejemplos/{x['slug']}.html", "name": x["h1"]} for i, x in enumerate(EJEMPLOS)]}},
        migas([("Inicio", f"{WEB}/"), ("Ejemplos", url)]), ORGANIZACION]}
    tarjetas = "".join(tarjeta_ejemplo(x, base) for x in EJEMPLOS)
    return f"""{cabeza('Ejemplos de presupuestos de obra con partidas y precios',
                 'Diez ejemplos de presupuestos de obra por partidas: baño, cocina, pintura, albañilería, fontanería, locales y más, con IVA, forma de pago y consejos.',
                 'ejemplos/', base, ld)}
{cabecera(base)}
<main id="contenido">
  <section class="ejemplo-hero">
    <div class="contenedor">
      <ol class="miga" aria-label="Estás en"><li><a href="{base}">Inicio</a></li><li aria-current="page">Ejemplos</li></ol>
      <h1>Ejemplos de presupuestos de obra, partida a partida</h1>
      <p class="entradilla">Cómo queda un presupuesto bien hecho en cada oficio: lo que dicta el profesional, las partidas con precio, el IVA, la forma de pago y lo que conviene revisar antes de enviarlo.</p>
    </div>
  </section>
  <section class="seccion-sm" style="padding-top:0">
    <div class="contenedor"><div class="ejemplos-rejilla">{tarjetas}</div></div>
  </section>
</main>
{pie(base)}
</body>
</html>
"""


# ---------------------------------------------------------------- Portada
def pagina_inicio():
    base = ""
    plantilla = (RAIZ / "_fuente" / "inicio.html").read_text(encoding="utf-8")
    sustituir = {
        "REGISTRO": REGISTRO, "ENTRAR": ENTRAR, "ESTUDIOS": ESTUDIOS, "EMAIL": EMAIL,
        "WHATSAPP_URL": wa("Hola, tengo una duda sobre Presupuesta"),
        "WHATSAPP_EMPRESA": wa("Hola, me interesa Presupuesta para una empresa con varias personas"),
        "WHATSAPP_VISIBLE": WHATSAPP_VISIBLE,
        "EJEMPLOS": "".join(tarjeta_ejemplo(x, base) for x in EJEMPLOS[:6]),
        "PREGUNTAS": preguntas_html(PREGUNTAS_INICIO, abrir_primera=True),
        "FOTO_FUNDADOR": (f'<img class="foto-fundador" src="{FUNDADOR["foto"]}" alt="{e(FUNDADOR["nombre"])}, fundador de Presupuesta" width="220" height="220" loading="lazy">'
                          if FUNDADOR.get("foto") else f'<div class="foto-fundador" aria-hidden="true">{e(FUNDADOR["nombre"][0])}</div>'),
        "NOMBRE_FUNDADOR": e(FUNDADOR["nombre"]),
    }
    for clave, nombre in [("I_CHECK", "check"), ("I_MIC", "mic"), ("I_CHISPAS", "chispas"), ("I_MAPA", "mapa"), ("I_DOC", "documento"),
                          ("I_PERSONAS", "personas"), ("I_CARTERA", "cartera"), ("I_HISTORIAL", "historial"), ("I_SUBIR", "subir"),
                          ("I_BAJAR", "bajar"), ("I_MENSAJE", "mensaje"), ("I_RELOJ", "reloj"), ("I_ARENA", "arena"), ("I_ESCUDO", "escudo"),
                          ("I_TARJETA", "tarjeta"), ("I_FLECHA", "flecha"), ("I_PORCENTAJE", "porcentaje"), ("I_REGALO", "regalo"),
                          ("I_MOVIL", "movil"), ("I_VARITA", "varita"), ("I_CASA", "casa"), ("I_TELEFONO", "telefono")]:
        sustituir[clave] = icono(nombre)
    for k, v in sustituir.items():
        plantilla = plantilla.replace("{{" + k + "}}", v)
    assert "{{" not in plantilla, plantilla[plantilla.find("{{"):plantilla.find("{{") + 40]

    ld = {"@context": "https://schema.org", "@graph": [
        ORGANIZACION, PERSONA,
        {"@type": "WebSite", "@id": f"{WEB}/#web", "url": f"{WEB}/", "name": "Presupuesta", "inLanguage": "es-ES", "publisher": {"@id": f"{WEB}/#organizacion"}},
        {"@type": "SoftwareApplication", "@id": f"{WEB}/#app", "name": "Presupuesta", "url": f"{WEB}/",
         "applicationCategory": "BusinessApplication", "applicationSubCategory": "Software de presupuestos de obra",
         "operatingSystem": "Web (navegador en móvil, tablet u ordenador)", "inLanguage": "es-ES",
         "description": "Presupuestos de obra con IA para autónomos y pymes de reformas e instalaciones en España: dictado por voz, partidas con precios ajustados a la provincia, aprendizaje de los precios propios, PDF con logo, NIF, IBAN e IVA, clientes, obras y control de cobros.",
         "featureList": ["Dictado por voz desde el móvil", "Presupuestos por capítulos y partidas generados con IA",
                         "Precios de mercado ajustados a las 52 provincias", "Aprende los precios del profesional e importa presupuestos antiguos en PDF",
                         "Edición con IA en lenguaje natural", "PDF con logo, NIF, IBAN, IVA 21/10/0 % y numeración automática",
                         "Clientes y obras con acceso directo a WhatsApp", "Panel de cobros: presupuestado, aceptado, cobrado y lo que te deben"],
         "screenshot": f"{WEB}/og-image.png", "publisher": {"@id": f"{WEB}/#organizacion"},
         "offers": [
             {"@type": "Offer", "name": "Plan mensual", "price": f"{PRECIO_MES:.2f}", "priceCurrency": "EUR", "url": REGISTRO, "availability": "https://schema.org/InStock",
              "priceSpecification": {"@type": "UnitPriceSpecification", "price": f"{PRECIO_MES:.2f}", "priceCurrency": "EUR", "unitCode": "MON", "valueAddedTaxIncluded": False},
              "eligibleDuration": {"@type": "QuantitativeValue", "value": 14, "unitCode": "DAY"}, "description": "14 días de prueba gratis sin tarjeta. Sin permanencia."},
             {"@type": "Offer", "name": "Plan anual", "price": f"{PRECIO_ANO:.2f}", "priceCurrency": "EUR", "url": REGISTRO, "availability": "https://schema.org/InStock",
              "priceSpecification": {"@type": "UnitPriceSpecification", "price": f"{PRECIO_ANO:.2f}", "priceCurrency": "EUR", "unitCode": "ANN", "valueAddedTaxIncluded": False},
              "description": "Dos meses gratis frente al plan mensual."}]},
        faq_ld(PREGUNTAS_INICIO)]}
    return f"""{cabeza('Presupuesta: presupuestos de obra con IA en un minuto',
                 'Dicta el trabajo en la obra y Presupuesta lo desglosa en partidas con precios de tu provincia. PDF con tu logo y control de cobros. 14 días gratis.',
                 '', base, ld)}
{cabecera(base)}
{plantilla}
{pie(base)}
</body>
</html>
"""


# ---------------------------------------------------------------- Legal y 404
def pagina_legal(clave):
    base = "/"
    d = LEGAL[clave]
    return f"""{cabeza(d['title'] + ' | Presupuesta', d['description'], d['archivo'], base)}
{cabecera(base)}
<main id="contenido" class="legal">
  <div class="contenedor contenedor-estrecho">
    <h1>{e(d['h1'])}</h1>
    <p class="fecha">Última actualización: {dt.date.fromisoformat(HOY).strftime('%d/%m/%Y')}</p>
    {d['cuerpo']}
  </div>
</main>
{pie(base)}
</body>
</html>
"""


def pagina_404():
    base = "/"
    return f"""{cabeza('Página no encontrada | Presupuesta', 'Esta página no existe o ha cambiado de sitio. Vuelve al inicio de Presupuesta o mira los ejemplos de presupuestos.', '404.html', base, indexar=False)}
{cabecera(base)}
<main id="contenido" class="pagina-404">
  <div class="contenedor contenedor-estrecho">
    <span class="antetitulo">Error 404</span>
    <h1>Aquí no hay obra que presupuestar</h1>
    <p class="entradilla" style="margin:0 auto">La página que buscas no existe o ha cambiado de sitio.</p>
    <div class="hero-ctas"><a href="/" class="btn btn-principal">Ir al inicio</a><a href="/ejemplos/" class="btn btn-secundario">Ver ejemplos</a></div>
  </div>
</main>
{pie(base)}
</body>
</html>
"""


# ---------------------------------------------------------------- Sitemap y llms
def sitemap():
    urls = [("", "1.0", "weekly"), ("ejemplos/", "0.8", "monthly")]
    urls += [(f"ejemplos/{x['slug']}.html", "0.7", "monthly") for x in EJEMPLOS]
    urls += [("aviso-legal.html", "0.2", "yearly"), ("politica-privacidad.html", "0.2", "yearly"), ("condiciones.html", "0.2", "yearly")]
    filas = "".join(f"  <url><loc>{WEB}/{u}</loc><lastmod>{HOY}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority></url>\n" for u, p, f in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{filas}</urlset>\n'


def llms():
    ej = "\n".join(f"- [{x['h1']}]({WEB}/ejemplos/{x['slug']}.html): {x['description']}" for x in EJEMPLOS)
    return f"""# Presupuesta

> Presupuesta (presupuesta.net) es una aplicación web española para hacer presupuestos de obra con inteligencia artificial. Está pensada para autónomos y pymes de reformas e instalaciones (albañiles, fontaneros, electricistas, pintores, reformistas). El profesional dicta o escribe el trabajo y la app lo desglosa en capítulos y partidas con precios de mercado ajustados a la provincia de la obra; después lo repasa, lo ajusta y descarga un PDF con su logo, NIF, IBAN e IVA. Cuesta 24,90 € + IVA al mes o 249 € + IVA al año, con 14 días de prueba gratis sin tarjeta.

Datos básicos:

- Web: {WEB}
- App (registro y acceso): {APP} · registro: {REGISTRO}
- Hecha en Ermua (Bizkaia, España) por {FUNDADOR['nombre']}, de Presupuesta Estudios ({ESTUDIOS})
- Contacto: WhatsApp +34 {WHATSAPP_VISIBLE} · {EMAIL}
- Idioma y mercado: español, España
- Funciona en el navegador (móvil, tablet u ordenador); no hay que instalar nada

## Producto

- [Cómo funciona]({WEB}/#como-funciona): dictar, repasar y enviar.
- [Funciones]({WEB}/#funciones): dictado por voz, IA por partidas, precios por provincia, «Mis precios», PDF, clientes, obras y cobros.
- [Precios]({WEB}/#precios): plan mensual 24,90 € + IVA, anual 249 € + IVA, código FUNDADOR para los 20 primeros.
- [Preguntas frecuentes]({WEB}/#preguntas)
- [Información ampliada para asistentes de IA]({WEB}/llms-full.txt)

## Ejemplos de presupuestos

{ej}

## Legal

- [Aviso legal]({WEB}/aviso-legal.html)
- [Privacidad y cookies]({WEB}/politica-privacidad.html)
- [Condiciones de uso]({WEB}/condiciones.html)
"""


def llms_full():
    faq = "\n\n".join(f"### {q}\n{a}" for q, a in PREGUNTAS_INICIO)
    ejemplos = []
    for x in EJEMPLOS:
        caps, bimp, iva, total, pagos = calcular(x)
        partidas = "\n".join(f"  - {f['desc']} — {cifra(f['cant'])} {f['ud']} × {euros(f['precio'])} = {euros(f['importe'])}" for c in caps for f in c["filas"])
        ejemplos.append(f"### {x['h1']}\n{WEB}/ejemplos/{x['slug']}.html\n{x['description']}\n- Base imponible: {euros(bimp)} · IVA {x['iva']} %: {euros(iva)} · Total: {euros(total)}\n- Partidas:\n{partidas}")
    ejemplos = "\n\n".join(ejemplos)
    return f"""# Presupuesta — información completa

Última actualización: {HOY}. Este documento describe Presupuesta con datos verificables para asistentes de IA, buscadores y personas.

## Qué es

Presupuesta es una aplicación web para hacer presupuestos de obra y reformas con inteligencia artificial, pensada para autónomos y pequeñas empresas de reformas e instalaciones en España.

Flujo de trabajo:
1. El profesional dicta el trabajo con el micrófono del móvil (o lo escribe): qué hay que hacer, medidas y dónde está la obra.
2. La IA lo desglosa en capítulos y partidas con unidad, cantidad y precio. Los precios parten de una media de mercado sin IVA y se ajustan a la provincia de la obra (52 provincias). Los importes, el IVA y los totales los calcula la aplicación al céntimo, no la IA.
3. El profesional repasa y edita las partidas (como una hoja de cálculo o pidiéndoselo a la IA en lenguaje natural, por ejemplo «añade un extractor» o «baja un 5 % los precios»).
4. Descarga un PDF profesional con su logo, NIF, dirección, numeración automática (2026-0001…), validez, IVA (21 %, 10 % o 0 %), forma de pago, IBAN y espacio para el conforme del cliente, y se lo envía por WhatsApp o email.
5. Cuando el cliente acepta, apunta los cobros. El panel muestra lo presupuestado, aceptado y cobrado del mes, lo que le deben y avisos «Para hoy» (presupuestos sin respuesta, que caducan o pendientes de cobro).

## Funciones

- Dictado por voz desde el navegador del móvil (iPhone y Android), hasta 3 minutos por dictado.
- Presupuestos por capítulos y partidas generados con IA (modelos de Anthropic; transcripción de voz con OpenAI).
- Precios de mercado ajustados a la provincia de cada obra, marcados como ZONA.
- «Mis precios»: cuando el profesional cambia un precio, Presupuesta lo aprende y lo usa en los siguientes presupuestos (marcado como TU). Se pueden importar presupuestos antiguos en PDF para cargar sus precios.
- Editor en móvil y ordenador, con guardado automático y deshacer.
- Clientes y obras, con acceso directo a llamar, WhatsApp, email y mapa.
- Estados del presupuesto: borrador, pendiente, aceptado y rechazado; control de cobros.
- Beneficio repartido en los precios u opcionalmente visible.

Lo que Presupuesta no hace (para evitar confusiones): no emite facturas a los clientes del profesional, no exporta a Excel, no tiene firma digital online ni portal del cliente, y no es una app de las tiendas de aplicaciones (se usa desde el navegador).

## Precios

- Plan mensual: 24,90 € + IVA al mes, sin permanencia.
- Plan anual: 249 € + IVA al año (dos meses gratis frente al mensual).
- Prueba gratis de 14 días con todas las funciones, sin tarjeta.
- Código FUNDADOR: los 20 primeros suscriptores del plan mensual pagan 10 € menos al mes para siempre (14,90 € + IVA).
- Incluye 100 presupuestos con IA al mes. Para empresas con más volumen o varias personas: plan a medida (contacto por WhatsApp).
- Pago con tarjeta a través de Stripe, con factura con IVA y opción de poner NIF/CIF. La baja se hace desde «Mi suscripción» y tiene efecto al final del periodo pagado.
- Sin suscripción activa se bloquea solo la IA; los datos y los PDF siguen accesibles.

## Quién hay detrás

Presupuesta la ha creado {FUNDADOR['nombre']}, desde Ermua (Bizkaia, España), dentro de Presupuesta Estudios ({ESTUDIOS}), un estudio que hace páginas web y posicionamiento local en Google para empresas de reformas y oficios. Soporte directo por WhatsApp (+34 {WHATSAPP_VISIBLE}) y en {EMAIL}.

## Preguntas frecuentes

{faq}

## Ejemplos de presupuestos (datos de ejemplo, empresas y clientes ficticios)

{ejemplos}
"""


# ---------------------------------------------------------------- Escribir todo
def escribir(ruta, contenido):
    p = RAIZ / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenido, encoding="utf-8")
    print("  ·", ruta)


def main():
    print("Generando la web de Presupuesta…")
    for x in EJEMPLOS:
        escribir(f"ejemplos/{x['slug']}.html", pagina_ejemplo(x))
    escribir("ejemplos/index.html", pagina_indice_ejemplos())
    escribir("index.html", pagina_inicio())
    for clave, d in LEGAL.items():
        escribir(d["archivo"], pagina_legal(clave))
    escribir("404.html", pagina_404())
    escribir("sitemap.xml", sitemap())
    escribir("llms.txt", llms())
    escribir("llms-full.txt", llms_full())
    print("Listo.")


if __name__ == "__main__":
    main()
