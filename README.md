# 🧮 MatrixCalc

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Vue](https://img.shields.io/badge/vue-3.x-green)
![Cloud Run](https://img.shields.io/badge/deployment-google%20cloud%20run-blueviolet)
![License](https://img.shields.io/badge/license-MIT-green)

**The Cloud-Native Linear Algebra Workspace.**

MatrixCalc is a production-grade web platform designed to bridge the gap between ephemeral online calculators and complex desktop environments like MATLAB. It provides a persistent, audit-traceable workspace for performing rigorous matrix computations (SVD, Eigenvalues, Cholesky) with backend-guaranteed numerical stability.

---

## 🧐 Why This Project Exists

Linear algebra is the "assembly language" of modern data science and engineering. However, the current tooling landscape forces a difficult trade-off:

- **Simple Calculators:** Lack persistence, advanced decompositions, and often run on client-side JS (sacrificing precision).
- **Excel:** Struggles with dimensionality and obscures logic behind opaque formulas.
- **MATLAB/Wolfram:** Expensive licenses and heavy local footprints.
- **Python/Jupyter:** Requires environment management and coding skills just to verify a result.

**MatrixCalc exists to democratize access to powerful, verifiable linear algebra.** It combines the accessibility of a web app with the power of a NumPy backend.

## 👥 Who Is This For

- **Engineering Students & Academics:** Instantly verify hand-calculations for complex factorizations using a reliable engine.
- **Machine Learning Learners:** Visualize the building blocks of algorithms (e.g., decomposing a matrix to understand PCA) in a noise-free environment.
- **Software Architects:** A reference implementation for a clean **Django + Vue + Cloud Run** architecture, demonstrating Domain-Driven Design (DDD) patterns within a decoupled monolith.

---

## ✨ Key Features

### 📐 Advanced Computational Engine

Powered by a hardened **NumPy** core, ensuring 64-bit float precision for all operations.

- **Fundamental Ops:** `A + B`, `A * B`, Inverse, Determinant, Transpose.
- **Decompositions:**
  - **SVD (Singular Value Decomposition):** Analyze singular values securely.
  - **Eigenvalues/Vectors:** For stability analysis.
  - **QR & Cholesky:** Optimized implementation for symmetric positive-definite matrices.
  - **Rank:** Numerical rank calculation using SVD tolerance.

### 💾 Persistence & Auditability

- **Workspace History:** Unlike standard calculators, every operation is logged as an immutable event.
- **Traceability:** See exactly when `Operation #42` was created, its inputs, and execution time (ms).
- **Data Portability:** Import datasets via CSV; export results for use in other tools.

---

## 🔍 GlassBox Mode: Understanding the "How"

**Don't just get the answer. Understand the algorithm.**

Standard engineering tools (Excel, NumPy, MATLAB) operate as "Black Boxes"—inputs go in, results come out, but the intermediate logic remains hidden. This is efficient for automation but terrible for learning.

**GlassBox Mode** transforms MatrixCalc from a calculator into an algorithmic visualizer. It runs a dedicated tracing engine alongside the numerical core to capture every atomic step of complex operations.

### ✨ Why It Matters

- **For Students:** Verify your manual Gaussian elimination homework step-by-step. Pinpoint exactly where your calculation diverged from the correct path.
- **For Instructors:** Demonstrate algorithms like LU Decomposition or Gram-Schmidt dynamically in the classroom without drawing dozens of matrices on a whiteboard.
- **For Developers:** Visualize numerical stability issues (e.g., pivot decay) in real-time.

### 🕹️ Interactive Trace Player

When you enable GlassBox Mode, you get full "VCR-style" control over the mathematical process:

- **Step-by-Step Playback:** Rewind and fast-forward through row operations ($R_2 \leftarrow R_2 - 3R_1$).
- **Contextual Highlighting:** See exactly which rows are interacting—Source rows glow green, Target rows glow red.
- **Semantic Explanation:** Each step is accompanied by a human-readable narrative explaining _why_ the algorithm made that move (e.g., _"Swapping rows 2 and 3 to avoid a zero pivot"_).

> _Available now for: Gaussian Elimination, RREF, and Determinant Expansion._

---

## 🏗️ Technical Architecture

MatrixCalc follows a **Decoupled Monolith** pattern, optimized for containerization and serverless deployment.

### Backend (The Core)

- **Django REST Framework:** Acts as the API Gateway. Views have been refactored into **Lean Views**, delegating orchestration to internal helpers to ensure "DRY" code.
- **Services Layer:** Located in `calculator.services`, it orchestrates high-level application logic (backups, data retention) separately from HTTP concerns.
- **Domain Layer:** Encapsulated in `calculator.utils.matrix_model`. This "Anti-Corruption Layer" sanitizes inputs and abstracts NumPy complexity, implementing strict domain rules and custom domain exceptions.
- **Persistence:** PostgreSQL (Production) / SQLite (Dev) with optimized JSON storage for matrix data.

### Frontend (The Interface)

- **Vue 3 (Composition API):** Modular, reactive UI components built with TypeScript.
- **Pinia:** Type-safe state management for handling the Matrix Workspace.
- **TailwindCSS:** Utility-first styling for a clean, "Math-First" aesthetic.
- **Latex Support:** Renders beautiful mathematical notation for results.

### DevOps (The Pipeline)

- **Docker:** Multi-stage builds reduce image size for faster cold starts.
- **Google Cloud Run:** Serverless deployment ensuring auto-scaling and zero-maintenance infrastructure.
- **Cloud Build:** Automated CI/CD pipelines defined in `cloudbuild.yaml`.

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose

### Fast Launch

1.  **Clone the repository**

    ```bash
    git clone https://github.com/medalcode/MatrixCalc.git
    cd MatrixCalc
    ```

2.  **Configure Environment**

    ```bash
    cp .env.example .env
    ```

3.  **Start the stack**

    ```bash
    docker-compose up --build
    ```

4.  **Access the application**
    - **Frontend:** `http://localhost:5173`
    - **Backend API:** `http://localhost:8000/api/`

---

## 📦 Deployment

This project is "Cloud Run Ready".

1.  **Authenticate with GCP**
    Ensure you have the `gcloud` CLI installed and authenticated.

2.  **Deploy via Cloud Build**
    ```bash
    gcloud builds submit --config cloudbuild.yaml .
    ```

For detailed configuration (database URLs, secret keys), see [Deployment Documentation](docs/deployment/README.md).

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to propose bug fixes and new features.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
