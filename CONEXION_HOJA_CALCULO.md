# Guía de Conexión Segura a Google Sheets (Hoja de Cálculo) para ObraFlow

Esta guía explica paso a paso cómo conectar el formulario de captación de tu landing page directamente con una **Hoja de Cálculo de Google** de forma **100% segura, gratuita y sin depender de herramientas de pago** como Zapier o Make.

---

## 🔒 ¿Por qué es este método 100% seguro?

Cuando trabajamos con páginas web estáticas (como GitHub Pages), colocar credenciales de bases de datos o tokens de acceso en el código JavaScript es muy peligroso, ya que cualquier usuario puede inspeccionar la página y robarlas.

Nuestra solución utiliza **Google Apps Script** como una pasarela intermedia (API segura):
1. **Acceso unidireccional (Solo Escritura)**: El script de Google solo expone una función de recepción de datos (`doPost`). La página web solo puede *enviar* nuevos leads.
2. **Invisibilidad de Datos**: Nadie que inspeccione tu página web puede leer los leads que ya han sido guardados, ni editar o borrar filas, ni acceder a tu cuenta de Google. Tu hoja de cálculo es completamente privada.
3. **Cero Costes**: Funciona de forma nativa e ilimitada bajo la infraestructura gratuita de Google Cloud.

---

## 🛠️ Paso 1: Preparar tu Hoja de Cálculo

1. Entra en tu cuenta de Google Drive y crea una nueva **Hoja de Cálculo de Google** (Google Sheet).
2. Nómbrala como gustes, por ejemplo: `Leads ObraFlow`.
3. En la primera fila (Fila 1), crea las siguientes columnas para estructurar los datos:
   * **Columna A**: `Fecha`
   * **Columna B**: `Nombre`
   * **Columna C**: `Teléfono`
   * **Columna D**: `Tipo de Obra`
   * **Columna E**: `Volumen de Presupuestos / mes`

---

## 💻 Paso 2: Configurar el Apps Script Seguro

1. En el menú superior de tu hoja de cálculo, haz clic en **Extensiones** ➔ **Apps Script**.
2. Se abrirá una nueva pestaña con el editor de código. Borra todo el código que aparezca por defecto en el archivo `Código.gs`.
3. Copia y pega exactamente el siguiente código:

```javascript
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  try {
    // Parseamos el JSON recibido desde la página web
    var data = JSON.parse(e.postData.contents);
    
    // Formateamos la fecha a formato local en España (GMT+2 / GMT+1)
    var formattedDate = new Date(data.date).toLocaleString('es-ES', { timeZone: 'Europe/Madrid' });
    
    // Mapeamos los valores internos de los selects a texto elegante en español
    var workTypeMap = {
      'obra-nueva': 'Obra nueva',
      'reforma-integral': 'Reforma integral',
      'fontaneria-electricidad': 'Fontanería / Electricidad',
      'pintura-acabados': 'Pintura y acabados',
      'varios': 'Varios'
    };
    
    var volumeMap = {
      '1-5': '1-5 presupuestos/mes',
      '6-15': '6-15 presupuestos/mes',
      '16-30': '16-30 presupuestos/mes',
      'mas-de-30': 'Más de 30 presupuestos/mes'
    };
    
    var workTypeSpanish = workTypeMap[data.workType] || data.workType;
    var volumeSpanish = volumeMap[data.volume] || data.volume;
    
    // Añadimos la fila a la hoja de cálculo.
    // El prefijo "'" en el teléfono asegura que Excel/Google Sheets lo lea como texto y no trunque los ceros a la izquierda.
    sheet.appendRow([
      formattedDate,
      data.name,
      "'" + data.phone,
      workTypeSpanish,
      volumeSpanish
    ]);
    
    // Devolvemos una respuesta exitosa compatible con CORS preflight
    return ContentService.createTextOutput(JSON.stringify({ 'status': 'success', 'message': 'Lead guardado con éxito.' }))
                         .setMimeType(ContentService.MimeType.JSON)
                         .setHeader('Access-Control-Allow-Origin', '*');
                         
  } catch (error) {
    // Devolvemos el error en formato JSON
    return ContentService.createTextOutput(JSON.stringify({ 'status': 'error', 'message': error.toString() }))
                         .setMimeType(ContentService.MimeType.JSON)
                         .setHeader('Access-Control-Allow-Origin', '*');
  }
}

// Requerido por los navegadores modernos para peticiones Fetch asíncronas entre dominios (CORS Preflight)
function doOptions(e) {
  return ContentService.createTextOutput("")
                       .setMimeType(ContentService.MimeType.TEXT)
                       .setHeader('Access-Control-Allow-Origin', '*')
                       .setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
                       .setHeader('Access-Control-Allow-Headers', 'Content-Type');
}
```

4. Haz clic en el icono de **Guardar** (el disquete en la barra superior) o pulsa `Ctrl + S`.

---

## 🚀 Paso 3: Publicar el Apps Script como Aplicación Web

Para que la landing page pueda comunicarse con este código, debemos publicarlo:

1. Haz clic en el botón azul **Implementar** (en la esquina superior derecha) ➔ **Nueva implementación**.
2. En la ventana que aparece, haz clic en el icono del engranaje al lado de "Seleccionar tipo" y elige **Aplicación web**.
3. Rellena los campos de la siguiente manera:
   * **Descripción**: `Webhook de captura Leads ObraFlow`
   * **Ejecutar como**: `Yo (tu-correo@gmail.com)`
   * **Quién tiene acceso**: Cambia a **Cualquiera** (*Esto es fundamental, de lo contrario Google bloqueará las llamadas desde la web*).
4. Haz clic en el botón azul **Implementar**.
5. *Nota: Si es la primera vez, Google te pedirá "Autorizar acceso". Haz clic en "Autorizar acceso", selecciona tu cuenta de Google, haz clic en "Avanzado" (abajo) y luego en "Ir a Proyecto sin nombre (no seguro)" para dar los permisos necesarios.*
6. Una vez completado, Google te mostrará una ventana con la **URL de la aplicación web**.
7. Haz clic en **Copiar** bajo la URL (tendrá un formato similar a: `https://script.google.com/macros/s/AKfycb.../exec`).

---

## 🔗 Paso 4: Vincular en tu Landing Page

1. Abre tu archivo `index.html`.
2. Busca la línea donde se definen las variables globales de configuración (alrededor de la línea 2426). Verás lo siguiente:
   ```javascript
   const WEBHOOK_URL = ""; // Introduce tu webhook URL si deseas enviar los datos a un CRM/Email
   ```
3. Pega la URL que has copiado de Google Apps Script dentro de las comillas dobles. Deberá quedar así:
   ```javascript
   const WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbXXXXXXXXXXXXXXXXXXXXXXXXXXXX/exec";
   ```
4. Guarda el archivo `index.html`.

¡Eso es todo! Abre tu web localmente, rellena el formulario de registro y pulsa enviar. Verás que en menos de 2 segundos la nueva fila aparece automáticamente en tu hoja de cálculo con el nombre, teléfono formateado y datos de obra perfectamente desglosados en español.
