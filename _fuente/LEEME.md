# Web de Presupuesta (presupuesta.net)

HTML estático para Hostinger. Las páginas se **generan**: no edites a mano `index.html` ni `ejemplos/*.html`.

## Cambiar algo
- Portada: `_fuente/inicio.html`
- Preguntas de la portada, fundador (nombre y foto) y textos legales: `_fuente/textos.py`
- Ejemplos de presupuestos: `_fuente/ejemplos.py` (los importes los calcula el generador)
- Cabecera, pie, SEO, datos estructurados, sitemap y llms.txt: `_fuente/generar.py`
- Estilos y JavaScript: `assets/site.css` y `assets/site.js`

Después ejecuta, desde la carpeta de la web:

    python3 _fuente/generar.py

## Subir a Hostinger
Sube todo **menos** `_fuente/` y `.git/` a `public_html`. Antes de sobrescribir el `.htaccess`, mira si Hostinger
ya tenía uno con reglas propias y júntalas.
