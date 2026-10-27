"""Textos de la portada (preguntas), datos del fundador y páginas legales."""

# Pon aquí tu foto (por ejemplo "assets/raul.jpg", cuadrada, ~600 px) y tu nombre completo.
FUNDADOR = {"nombre": "Raúl", "foto": ""}

# Datos del titular de la web (obligatorios por la LSSI). Sustituye los PENDIENTE y vuelve a generar.
TITULAR = {
    "nombre": "PENDIENTE: nombre y apellidos o razón social",
    "nif": "PENDIENTE: NIF/CIF",
    "domicilio": "PENDIENTE: dirección completa, 48260 Ermua (Bizkaia)",
    "email": "asistente@presupuesta.net",
    "email_privacidad": "privacidad@presupuesta.net",
    "telefono": "+34 652 67 93 91",
}


def _dato(valor: str) -> str:
    return f'<span class="pendiente">{valor}</span>' if valor.startswith("PENDIENTE") else valor


T = {k: _dato(v) for k, v in TITULAR.items()}

PREGUNTAS_INICIO = [
    ("¿Tengo que poner la tarjeta para probarlo?",
     "No. Te registras con tu email y tienes 14 días con todas las funciones, sin tarjeta. Si al terminar no te convence, no pagas nada; tus presupuestos y PDF siguen ahí."),
    ("¿De dónde salen los precios? ¿Son fiables?",
     "La IA parte de precios medios de mercado en España, sin IVA, y Presupuesta los ajusta a la provincia de cada obra. Cuando cambias un precio, lo aprende y lo usa en los siguientes presupuestos; también puedes subir tus presupuestos antiguos en PDF para cargar tus tarifas. Son una base orientativa: el precio final lo decides tú."),
    ("¿Funciona en el móvil? ¿Hay que instalar algo?",
     "Funciona en el navegador del móvil (iPhone y Android), de la tablet y del ordenador, sin instalar nada. El dictado por voz está pensado para usarlo en la obra."),
    ("¿Qué IVA puedo poner?",
     "21 %, 10 % (reformas de vivienda que cumplan los requisitos) o 0 %. Presupuesta recuerda el que uses y lo desglosa en el PDF."),
    ("¿Cuántos presupuestos puedo hacer?",
     "El plan incluye 100 presupuestos generados con IA al mes, de sobra para un autónomo. Si tu empresa necesita más, escríbenos y te preparamos un plan a medida."),
    ("¿Me hacéis factura? ¿Cómo me doy de baja?",
     "Sí: el pago se hace con Stripe, que emite la factura con IVA y te deja poner tu NIF o CIF. Te das de baja cuando quieras desde «Mi suscripción», sin permanencia; sigues teniendo acceso hasta el final del periodo pagado."),
    ("¿Qué es el código FUNDADOR?",
     "Un agradecimiento para los 20 primeros: 10 € menos al mes para siempre en el plan mensual (14,90 € + IVA). Lo introduces al activar la suscripción."),
    ("¿Mis datos están seguros?",
     "Cada profesional solo ve sus propios clientes y presupuestos, los pagos los gestiona Stripe (nunca vemos tu tarjeta) y no vendemos tus datos a nadie. Lo tienes explicado en la política de privacidad."),
    ("¿Puedo hablar con una persona?",
     "Claro. Escríbenos por WhatsApp al 652 67 93 91 o a asistente@presupuesta.net y te responde Raúl, que es quien ha hecho Presupuesta."),
]

LEGAL = {
    "aviso": {
        "archivo": "aviso-legal.html",
        "title": "Aviso legal",
        "h1": "Aviso legal",
        "description": "Datos identificativos del titular de presupuesta.net y condiciones de uso de la web.",
        "cuerpo": f"""
<h2>1. Titular de la web</h2>
<p>En cumplimiento de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), estos son los datos del titular de presupuesta.net y de la aplicación panel.presupuesta.net:</p>
<ul>
  <li><strong>Titular:</strong> {T['nombre']}</li>
  <li><strong>NIF:</strong> {T['nif']}</li>
  <li><strong>Domicilio:</strong> {T['domicilio']}</li>
  <li><strong>Email:</strong> <a href="mailto:{TITULAR['email']}">{TITULAR['email']}</a></li>
  <li><strong>Teléfono y WhatsApp:</strong> {TITULAR['telefono']}</li>
</ul>
<p>Presupuesta es una marca comercial vinculada a Presupuesta Estudios (estudios.presupuesta.net).</p>

<h2>2. Objeto</h2>
<p>Esta web informa sobre Presupuesta, una aplicación para hacer presupuestos de obra con inteligencia artificial, y permite acceder a su registro. El uso de la aplicación se rige además por las <a href="condiciones.html">condiciones de uso</a>.</p>

<h2>3. Uso de la web</h2>
<p>Te comprometes a usar la web de forma lícita y a no dañar sus sistemas ni los de terceros. Los contenidos (textos, diseño, código, logotipos y ejemplos) son de Presupuesta o de sus autores y no se pueden reproducir con fines comerciales sin permiso.</p>

<h2>4. Ejemplos y precios orientativos</h2>
<p>Los presupuestos de ejemplo usan empresas, clientes, NIF e IBAN ficticios. Los precios que propone la aplicación son estimaciones de referencia: el profesional debe revisarlos y es responsable del presupuesto que envía a su cliente.</p>

<h2>5. Responsabilidad</h2>
<p>Ponemos los medios razonables para que la web funcione y su información sea correcta, pero no podemos garantizar la ausencia total de errores o interrupciones. No nos hacemos responsables de los contenidos de webs de terceros enlazadas.</p>

<h2>6. Legislación aplicable</h2>
<p>Se aplica la legislación española. Para cualquier conflicto, las partes se someten a los juzgados y tribunales que correspondan según la ley; si eres consumidor, los de tu domicilio.</p>
""",
    },
    "privacidad": {
        "archivo": "politica-privacidad.html",
        "title": "Política de privacidad y cookies",
        "h1": "Privacidad y cookies",
        "description": "Cómo trata Presupuesta tus datos personales en la web y en la aplicación, con qué proveedores, durante cuánto tiempo y cómo ejercer tus derechos.",
        "cuerpo": f"""
<p>Te explicamos de forma clara qué datos tratamos, para qué y con quién, según el Reglamento General de Protección de Datos (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD).</p>

<h2>1. Responsable</h2>
<p>{T['nombre']} · NIF {T['nif']} · {T['domicilio']} · <a href="mailto:{TITULAR['email_privacidad']}">{TITULAR['email_privacidad']}</a></p>

<h2>2. Qué datos tratamos y para qué</h2>
<table>
  <tr><th>Cuándo</th><th>Datos</th><th>Para qué</th><th>Base legal</th></tr>
  <tr><td>Te registras y usas la app</td><td>Nombre, email, contraseña (cifrada), datos de tu negocio (NIF, dirección, logo, IBAN, condiciones) y lo que introduces: clientes, obras, presupuestos, precios y cobros</td><td>Prestarte el servicio</td><td>Contrato</td></tr>
  <tr><td>Dictas o generas un presupuesto</td><td>El audio y el texto del trabajo</td><td>Pasar el audio a texto y generar las partidas</td><td>Contrato</td></tr>
  <tr><td>Te suscribes</td><td>Datos de facturación (la tarjeta la gestiona Stripe; nunca la vemos)</td><td>Cobrar la suscripción y emitir facturas</td><td>Contrato y obligación legal</td></tr>
  <tr><td>Nos escribes</td><td>Lo que nos cuentes por WhatsApp o email</td><td>Responderte</td><td>Interés legítimo</td></tr>
  <tr><td>Visitas la web y aceptas cookies</td><td>Datos de navegación (ver cookies)</td><td>Entender cómo se usa la web y mejorarla</td><td>Consentimiento</td></tr>
</table>
<p>Los datos de tus clientes que metes en la aplicación son tuyos: los tratamos solo por cuenta tuya y para darte el servicio (actuamos como encargado del tratamiento).</p>

<h2>3. Proveedores que nos ayudan</h2>
<ul>
  <li><strong>Supabase</strong>: base de datos, cuentas y almacenamiento de archivos.</li>
  <li><strong>Vercel</strong>: alojamiento de la aplicación.</li>
  <li><strong>Hostinger</strong>: alojamiento de esta web.</li>
  <li><strong>Anthropic</strong>: IA que genera y edita las partidas a partir de tu descripción.</li>
  <li><strong>OpenAI</strong>: transcripción del audio del dictado.</li>
  <li><strong>Stripe</strong>: cobros y facturas de la suscripción.</li>
  <li><strong>Microsoft Clarity</strong>: medición del uso de la web, solo si lo aceptas.</li>
</ul>
<p>Algunos están fuera del Espacio Económico Europeo (principalmente en EE. UU.). Las transferencias se amparan en el Marco de Privacidad de Datos UE-EE. UU. o en cláusulas contractuales tipo de la Comisión Europea. No vendemos tus datos ni los usamos para publicidad.</p>

<h2>4. Cuánto tiempo los guardamos</h2>
<p>Mientras tengas la cuenta. Si la borras, eliminamos tus datos salvo los que la ley nos obligue a conservar (por ejemplo, las facturas, durante los plazos fiscales). Los mensajes de contacto, el tiempo necesario para atenderte.</p>

<h2>5. Tus derechos</h2>
<p>Puedes pedir acceso, rectificación, supresión, oposición, limitación y portabilidad de tus datos, y retirar tu consentimiento, escribiendo a <a href="mailto:{TITULAR['email_privacidad']}">{TITULAR['email_privacidad']}</a>. Si crees que no lo hemos hecho bien, puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>

<h2 id="cookies">6. Cookies</h2>
<p>Esta web no usa cookies de publicidad. Solo, si lo aceptas, <strong>Microsoft Clarity</strong> para ver de forma agregada cómo se navega (clics, desplazamiento) y mejorar los textos. Guardamos tu elección en tu navegador. Puedes cambiarla en cualquier momento en <a href="#" data-abrir-cookies>Configurar cookies</a>.</p>
<table>
  <tr><th>Cookie</th><th>Proveedor</th><th>Finalidad</th><th>Duración</th></tr>
  <tr><td>_clck, _clsk, CLID, MUID</td><td>Microsoft Clarity</td><td>Medición y análisis del uso de la web</td><td>De 1 día a 1 año</td></tr>
</table>
<p>La aplicación (panel.presupuesta.net) usa solo las cookies técnicas necesarias para mantener tu sesión iniciada.</p>
""",
    },
    "condiciones": {
        "archivo": "condiciones.html",
        "title": "Condiciones de uso de Presupuesta",
        "h1": "Condiciones de uso",
        "description": "Condiciones de uso y contratación de Presupuesta: prueba gratis, precio, pago, baja, uso de la IA y responsabilidades.",
        "cuerpo": f"""
<p>Estas condiciones regulan el uso de Presupuesta (panel.presupuesta.net), prestado por {T['nombre']} (NIF {T['nif']}). Al crear una cuenta las aceptas.</p>

<h2>1. El servicio</h2>
<p>Presupuesta es una aplicación web para profesionales y empresas que permite crear presupuestos de obra con ayuda de inteligencia artificial, guardarlos, editarlos, descargarlos en PDF y llevar el control de clientes, obras y cobros.</p>

<h2>2. Cuenta</h2>
<p>Necesitas una cuenta con un email válido. Eres responsable de guardar tu contraseña y de que los datos de tu negocio sean correctos. El servicio está dirigido a profesionales: al registrarte declaras que lo usas para tu actividad.</p>

<h2>3. Prueba gratis</h2>
<p>Al registrarte tienes 14 días de prueba con todas las funciones y sin tarjeta. Al terminar, si no te suscribes, se desactivan las funciones de IA (generar, editar con IA, dictar e importar PDF); tus datos y PDF siguen disponibles.</p>

<h2>4. Precio y pago</h2>
<ul>
  <li>Plan mensual: 24,90 € + IVA al mes. Plan anual: 249 € + IVA al año.</li>
  <li>El cobro es por adelantado al inicio de cada periodo, con tarjeta, a través de Stripe, que emite la factura.</li>
  <li>El código FUNDADOR (20 plazas) aplica 10 € de descuento al mes, de forma indefinida mientras la suscripción mensual siga activa.</li>
  <li>Incluye hasta 100 presupuestos generados con IA al mes por cuenta.</li>
  <li>Si cambiamos el precio, te avisaremos con al menos 30 días de antelación y podrás darte de baja antes.</li>
</ul>

<h2>5. Baja</h2>
<p>No hay permanencia. Puedes darte de baja cuando quieras desde «Mi suscripción»; la baja tiene efecto al final del periodo ya pagado y no se devuelven periodos parciales. Puedes pedir que borremos tu cuenta y tus datos escribiendo a <a href="mailto:{TITULAR['email']}">{TITULAR['email']}</a>.</p>

<h2>6. Uso de la inteligencia artificial</h2>
<p>Las partidas, mediciones y precios que propone la IA son estimaciones orientativas y pueden contener errores. Debes revisarlos antes de enviar un presupuesto: tú eres el responsable de su contenido, de los precios y del IVA que aplicas.</p>

<h2>7. Tus datos y tus contenidos</h2>
<p>Lo que introduces es tuyo. Lo tratamos para darte el servicio, según la <a href="politica-privacidad.html">política de privacidad</a>. Puedes descargar tus presupuestos en PDF en cualquier momento.</p>

<h2>8. Disponibilidad y responsabilidad</h2>
<p>Trabajamos para que el servicio funcione siempre, pero puede haber interrupciones por mantenimiento o causas ajenas. En la medida que permita la ley, nuestra responsabilidad se limita al importe pagado en los últimos 12 meses.</p>

<h2>9. Cambios y ley aplicable</h2>
<p>Podemos actualizar estas condiciones; si el cambio es importante, te avisaremos por email. Se aplica la ley española.</p>
""",
    },
}
