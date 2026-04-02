# LearnFlow Neural Studio (Frontend)

The advanced React frontend for the Study Planner system, designed with a high-performance "Neural Studio" aesthetic.

## 🚀 Features

- **Neural Architecture:** Built with React 19, TypeScript, and Vite.
- **Precision Routing:** Integrated `react-router-dom` for seamless client-side navigation.
- **Secure Sync:** Full JWT authentication flow with protected routes and persistent sessions.
- **Advanced Aesthetics:** Custom glass-morphism, glowing UI elements, and high-contrast dark mode.
- **Dynamic Deep Linking:** URL-synchronized subject views for bookmarkable knowledge nodes.

## 🛠️ Tech Stack

- **Framework:** React 19
- **Styling:** Tailwind CSS + custom glass-morphism
- **Icons:** Lucide React
- **Routing:** React Router 7
- **HTTP Client:** Axios
- **Testing:** Vitest + React Testing Library

## 🚦 Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

### Production Build

```bash
npm run build
```

### Testing

```bash
npm run test
```

## 📂 Architecture

- `/src/components/auth`: Login, Register, and Route Guards.
- `/src/components/layout`: Sidebar and Topbar (Neural Core layout).
- `/src/components/dashboard`: Main subjects overview.
- `/src/components/subject`: Deep-dive subject analysis and resource viewing.
- `/src/context`: Global state management (Auth and App contexts).
- `/src/services`: API communication layer.
