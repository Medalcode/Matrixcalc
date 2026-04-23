# 🧮 MatrixCalc

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Vue](https://img.shields.io/badge/vue-3.x-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Cloud Run](https://img.shields.io/badge/deployment-google%20cloud%20run-blueviolet)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-3.0-orange)

**The Cloud-Native Linear Algebra Workspace.**

MatrixCalc es una plataforma web de grado de producción diseñada para realizar cálculos matriciales rigurosos (SVD, Autovalores, Cholesky, etc.). Combinando la accesibilidad de una aplicación web moderna con la potencia y precisión de un backend en NumPy, proporciona un entorno de trabajo persistente y auditable para ingenieros, estudiantes y desarrolladores.

---

## 🧐 Problema que resuelve

El ecosistema actual de herramientas matemáticas obliga a los usuarios a elegir entre extremos:
- **Calculadoras web simples:** Son efímeras, carecen de operaciones avanzadas y calculan los datos en el cliente (perdiendo precisión y estabilidad al trabajar con matrices grandes).
- **Herramientas de escritorio (MATLAB/Excel):** Requieren licencias costosas, instalaciones pesadas o interfaces poco intuitivas para cálculos multidimensionales.
- **Scripts locales (Python/Jupyter):** Exigen configuración estricta de entornos y conocimientos previos de programación solo para verificar un simple resultado matemático.

**MatrixCalc democratiza el acceso a herramientas de álgebra lineal de grado científico.** Ofrece la inmediatez de la web, la exactitud de un motor numérico robusto (NumPy de 64-bits) y la trazabilidad de un historial inmutable.

---

## ✨ Características principales

- **⚙️ Motor Computacional Avanzado:** Cálculos precisos y estables de operaciones fundamentales y factorizaciones complejas (SVD, Descomposición QR, Eigenvectores, Rango, Cholesky).
- **💾 Persistencia de Trabajo y Auditoría:** Cada operación se guarda de forma inmutable, permitiendo reconstruir cualquier resultado a lo largo del tiempo con métricas de ejecución.
- **🔍 GlassBox Mode (Modo "Caja de Cristal"):** No solo da el resultado, sino que explica _cómo_ llegó a él. Ejecuta algoritmos numéricos paso a paso (ej. Eliminación Gaussiana) con justificaciones narrativas intuitivas, funcionando como una potente herramienta de enseñanza.
- **🌐 Exportación e Importación Dinámica:** Soporte para carga de datasets vía CSV y exportación del historial de operaciones de un proyecto.
- **🖥️ Renderizado Matemático Nivel Académico:** Representación visual elegante tanto de las matrices entrantes como de los resultados mediante integración con LaTeX.

---

## 🛠️ Stack tecnológico con justificación breve

El proyecto sigue una arquitectura de **Monolito Desacoplado** ("Decoupled Monolith"), fuertemente enfocado en buenas prácticas, testabilidad y optimizado para despliegue serverless.

### Backend (Core Lógico y API API)
- **Python 3.11 & Django REST Framework:** Seleccionado por su madurez, seguridad y velocidad de desarrollo para la construcción de APIs robustas. Implementa un diseño de "Lean Views" adaptando Domain Driven Design.
- **NumPy:** El estándar definitivo de la industria para computación científica. Garantiza precisión total (*64-bit precision*) y manejo veloz de algoritmos matriciales.
- **Celery & Redis:** Para procesamiento asíncrono y de mensajería (escalabilidad de cálculos altamente intensivos sin bloquear requests HTTP).
- **PostgreSQL / SQLite:** Almacenamiento optimizado y serialización eficiente de objetos JSON para guardar el estado matricial de las sesiones matemáticas.

### Frontend (Interfaz de Usuario)
- **Vue 3 (Composition API) & TypeScript:** Permite un desarrollo de componentes fuertemente tipados, escalables y provee una gestión de dependencias predecible.
- **Pinia:** Elegido como gestor moderno para el almacenamiento global de las interacciones asíncronas del workspace matricial.
- **Tailwind CSS:** Asegura consistencia visual, iteración muy rápida del diseño UI/UX sin cargar CSS residual e innecesario, manteniendo un aspecto pulido "Math-First".

### Infraestructura (DevOps)
- **Docker & Docker Compose:** Entorno de despliegue contenerizado tanto del backend, front y de la base de datos de manera uniforme usando builds multi-etapa para reducción de pesos de imágenes.
- **Google Cloud Run & Cloud Build:** Orientación total hacia un despliegue "Serverless" y pipelines de CI/CD automatizadas (autoescalado desde y a cero sin infraestructura a gestionar).

---

## 🏗️ Arquitectura del sistema

MatrixCalc está compuesto dividiendo responsabilidades estrictas, implementando patrones de *Domain-Driven Design (DDD)* para asegurar mantenibilidad y legibilidad:

1. **Presentation Layer (Vue/Frontend):** Captura interacciones, mantiene el estado del workspace de forma fluida (SPA) y renderiza tipografía compleja en LaTeX para lectura matemática amigable.
2. **Gateway Layer (DRF):** Expone endpoints estilo RESTful. Orquesta el tráfico de red, validaciones de seguridad de permisos e hidratación inicial de modelos perezosos.
3. **Services Layer:** Controla las transacciones y lógica alta de aplicación, de manera independiente a la forma en que los datos entraron, asegurando que el core jamás se ensucie con datos de red.
4. **Domain Layer (Anti-Corruption):** Módulo core (ej. `calculator.utils.matrix_model`) aislado 100% libre de frameworks web que mapea matrices inseguras u operaciones de las interfaces y revalida todo a través del motor NumPy, protegiendo así toda la lógica de cálculo puro del sistema.

---

## 🚀 Instalación paso a paso

### Prerrequisitos
- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) instalados en tu máquina.
- Git.

### Entorno de Desarrollo Rápido

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/medalcode/MatrixCalc.git
   cd MatrixCalc
   ```

2. **Configurar las variables de entorno:**
   Usa el archivo base preparado para levantar los servicios elementales.
   ```bash
   cp .env.example .env
   ```

3. **Desplegar toda la pila local:**
   Docker Compose se encargará de configurar la base de datos, descargar todas las dependencias y levantar tanto la API de Python como el servidor en vivo de Vue y el gestor asíncrono.
   ```bash
   docker-compose up --build
   ```

4. **Acceso a la aplicación:**
   Una vez que los contenedores estén corriendo saludables:
   - **Interfaz en el navegador:** `http://localhost:5173`
   - **Acceso API y Backend:** `http://localhost:8000/api/`

*_💡 Tip para Desarrolladores:_* Existe un `Makefile` preconfigurado en la raíz del proyecto para tareas recurrentes. Simplemente ejecuta `make help` para ver comandos ágiles como `make test`, `make down` o `make setup`.

---

## 🕹️ Uso del sistema

### Diferentes formas de utilizar MatrixCalc

1. **La Verificadora (El Estudiante / Profesor):**
   Un estudiante está teniendo problemas detectando errores en sus cálculos fraccionales de un Algoritmo RREF. En un clic, ingresa su matriz a MatrixCalc activando el modo de análisis visual *GlassBox*. El sistema recorre renglón por renglón dictando textualmente las operaciones aritméticas efectuadas y resaltando qué filas restaron de cuáles.

2. **Cómputos Masivos (Data Scientist):**
   Un investigador intenta hacer la Descomposición de Valores Singulares de una matriz densa extraída de un data source. Crea un *espacio de trabajo* aislado en la plataforma, sube las dimensiones, ejecuta el cálculo pesado (el cual NumPy procesa velozmente) e inspecciona el valor de los eigenvectores. Esta sesión queda completamente trazada en la red como operación de consulta auditable para su tesis.

3. **Revisión de Arquitecturas (Ingenieros & Reclutadores):**
   Un equipo evalúa la destreza del Autor con patrones de código maduros. Revisan cómo la SPA está conectada asíncronamente a Django DRF con control transaccional eficiente a bases de datos relacionales mediado todo mediante Docker Orchestration limpio.

---

## 📁 Estructura de carpetas explicada

Este proyecto está organizado modularmente separando estrictamente código de infraestructura y responsabilidades.

```text
Matrixcalc/
├── calculator/           # ✅ Lógica Core: Servicios, endpoints REST, validadores avanzados y el motor de NumPy.
├── matrixcalc_web/       # ⚙️ Configurador Django: Centralización de routing, settings y middleware (WSGI/ASGI).
├── frontend/             # 💻 Single Page Application: Código fuente en Vue 3, views, composables de TypeScript y Tailwind.
├── docs/                 # 📚 Documentación técnica exhaustiva del desarrollo.
├── docker/               # 🐳 Infraestructura de contenedores para scripts y entrypoints.
├── backups/              # 📥 Almacén de dumps de base de datos intermedios en caso de reinicios masivos.
├── docker-compose.yml    # 🚢 Orquestador maestro que interconecta todos los servicios (Django + Node/Vue + DBs).
├── Makefile              # 🪄 Archivo mágico para la automatización local de tareas en consola (Developer Experience).
└── cloudbuild.yaml       # ☁️ CI/CD Pipelines: Reglas y stages automatizados de Google Cloud.
```

---

## 🛣️ Roadmap futuro

- [ ] **Realtime Collaborative Workspaces:** Añadir integración de WebSockets para permitir que varios usuarios manipulen en vivo la misma matriz o espacio de trabajo simultáneamente.
- [ ] **Extensión Tensor (Matemáticas N-Dimensionales):** Expandir la base para admitir visualización cruzada y cálculos avanzados para Inteligencia Artificial soportando *Arrays multicapa*.
- [ ] **Soporte total de Números Complejos:** Habilitar a través de toda la aplicación validaciones puramente imaginarias en operaciones elementales de descomposiciones densas de factorizaciones QR avanzadas.
- [ ] **Refinamiento de Microservicios:** Mover asincronía más pesada al modelo *Pub/Sub*, permitiendo arquitecturas event-driven desacopladas verdaderamente en un entorno backend puro.

---

## 🤝 Contribuciones

MatrixCalc cree firmemente en el movimiento de código abierto para dotar a la comunidad con aplicaciones robustas construyentes. Las contribuciones, discusiones de *Issues* y *Pull Requests* son siempre altamente alentadas.

Para participar, clona el respositorio y sigue las pautas detalladas en el archivo [CONTRIBUTING.md](CONTRIBUTING.md) sobre cómo inicializar tu entorno y nuestras convenciones estrictas de Git Flow.

---

## 📄 Licencia

Este proyecto está disponible y distribuido bajo la permisiva licencia estandarizada **[MIT License](LICENSE)**, protegiendo tanto uso libre, modificaciones o sublicenciamiento tanto en campos abiertos o con fines comerciales.

---

## 👨‍💻 Autor

Diseñado, conceptualizado y programado íntegramente por **Medalcode**

- **Rol:** Senior Software Engineer | Mención completa a roles de backend logic a UI/UX y Devops CI/CD del despliegue en línea.
- **GitHub:** [@medalcode](https://github.com/medalcode)
- **LinkedIn/Portfolio:** [Referenciado en mis repositorios principales en GitHub](https://github.com/medalcode)

> _"Escribir código escalable es un desafío de álgebra lógica en sí mismo."_
