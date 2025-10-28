# McKinsey PPT Generator Frontend

A modern React TypeScript frontend application for the McKinsey PowerPoint Generator, built with Material-UI and Redux Toolkit.

## Features

- 🔐 **Authentication System** - Secure login/register with JWT tokens
- 📊 **Dashboard** - Professional dashboard with presentation overview
- 📝 **Presentation Management** - Create, edit, and manage presentations
- 🎨 **McKinsey Design System** - Professional styling following McKinsey brand guidelines
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices
- ⚡ **Modern Stack** - React 18, TypeScript, Vite, Material-UI v5
- 🗄️ **State Management** - Redux Toolkit for efficient state management
- 🎯 **Type Safety** - Full TypeScript implementation with strict typing

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI) v5
- **State Management**: Redux Toolkit
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Form Handling**: React Hook Form
- **Notifications**: React Toastify
- **Styling**: Material-UI Theme + CSS Custom Properties

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navbar.tsx
│   ├── PrivateRoute.tsx
│   ├── LoadingSpinner.tsx
│   └── SlideCard.tsx
├── pages/              # Page components
│   ├── auth/           # Authentication pages
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   └── AuthLayout.tsx
│   └── dashboard/      # Dashboard pages
│       ├── Dashboard.tsx
│       ├── PresentationList.tsx
│       ├── CreatePresentation.tsx
│       └── PresentationEditor.tsx
├── services/           # API services
│   ├── api.ts
│   ├── auth.service.ts
│   └── presentation.service.ts
├── store/              # Redux store and slices
│   ├── store.ts
│   ├── authSlice.ts
│   └── presentationSlice.ts
├── styles/             # Styling and theme
│   ├── theme.ts
│   └── globals.css
├── types/              # TypeScript type definitions
│   └── index.ts
├── App.tsx             # Main app component
└── main.tsx            # Application entry point
```

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Update the `.env` file with your configuration:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to http://localhost:3000

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features Overview

### Authentication
- Secure login/register system
- JWT token-based authentication
- Automatic token refresh
- Password strength validation
- Form validation with error handling

### Dashboard
- Welcome screen with user statistics
- Recent presentations overview
- Quick actions for creating new presentations
- Professional McKinsey-style design

### Presentation Management
- Create presentations from templates
- Edit presentations with slide management
- Slide reordering with drag-and-drop
- Real-time saving
- Export to PowerPoint (backend integration)

### Design System
- McKinsey brand colors (#0070C0, #002E6C)
- Professional typography using Inter font
- Consistent spacing and layout
- Responsive breakpoints
- Accessible design patterns

## API Integration

The frontend integrates with the FastAPI backend through:

- **Authentication endpoints**: `/api/v1/auth/*`
- **Presentation endpoints**: `/api/v1/presentations/*`
- **File upload/download**: Multipart form data handling
- **Error handling**: Comprehensive error responses

### API Configuration

The API client includes:
- Automatic token injection
- Request/response interceptors
- Error handling with user notifications
- File upload progress tracking
- Download functionality

## State Management

Redux Toolkit slices:

### Auth Slice
- User authentication state
- Token management
- Profile information
- Loading and error states

### Presentation Slice
- Presentations list
- Current presentation editing
- Slides management
- CRUD operations

## Styling

### Theme System
- McKinsey brand colors
- Typography scale
- Component overrides
- Consistent shadows and spacing

### Responsive Design
- Mobile-first approach
- Breakpoints: xs(0), sm(600), md(900), lg(1200), xl(1536)
- Flexible grid system
- Touch-friendly interfaces

## Development Guidelines

### Code Style
- TypeScript strict mode
- ESLint configuration
- Consistent component patterns
- Service layer abstraction

### Component Structure
- Functional components with hooks
- TypeScript interfaces for props
- Error boundaries for robustness
- Loading states for better UX

### Best Practices
- Separation of concerns
- Reusable component library
- Centralized error handling
- Type-safe API calls

## Building for Production

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Preview the build:**
   ```bash
   npm run preview
   ```

3. **Deploy:**
   The `dist` folder contains the production build ready for deployment.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |
| `VITE_APP_NAME` | Application name | `McKinsey PPT Generator` |
| `VITE_ENABLE_DEBUG_MODE` | Enable debug features | `true` |

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Update tests for changes
4. Follow Material-UI patterns
5. Maintain responsive design

## License

This project is proprietary and confidential.