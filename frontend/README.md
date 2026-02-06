# AI-Powered Todo Chatbot - Frontend

This is the frontend for the AI-Powered Todo Chatbot application, built with React and Next.js. The interface provides a conversational experience for managing tasks through an intelligent AI assistant.

## Features

- **Conversational Interface**: Natural chat interface for task management
- **AI Assistant Integration**: Connects to backend AI for natural language processing
- **Task Management**: View, create, update, and delete tasks
- **Real-time Updates**: Instant feedback on task operations
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **User Authentication**: Secure login and signup flows
- **Modern UI**: Clean, intuitive interface with smooth animations

## Tech Stack

- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **API Client**: Axios for HTTP requests
- **UI Components**: Custom-built reusable components
- **Icons**: Lucide React icons

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages
│   │   ├── signin/        # Sign in page
│   │   └── signup/        # Sign up page
│   ├── dashboard/         # Main dashboard
│   │   ├── layout.tsx     # Dashboard layout
│   │   └── page.tsx       # Dashboard page
│   ├── chat/              # Chat interface
│   │   └── page.tsx       # Chat page
│   ├── tasks/             # Task management
│   │   ├── page.tsx       # Tasks list
│   │   └── [id]/          # Individual task pages
│   ├── layout.tsx         # Main layout
│   └── page.tsx           # Landing page
├── components/            # Reusable components
│   ├── auth/              # Authentication components
│   ├── chat/              # Chat interface components
│   ├── tasks/             # Task management components
│   ├── ui/                # Shared UI components
│   └── layout/            # Layout components
├── context/               # React Context providers
│   └── AuthContext.tsx    # Authentication context
├── lib/                   # Business logic and utilities
│   ├── api/              # API client and endpoints
│   ├── hooks/            # Custom React hooks
│   └── utils/            # Utility functions
├── types/                 # TypeScript type definitions
│   ├── auth.ts           # Authentication types
│   ├── tasks.ts          # Task types
│   └── chat.ts           # Chat types
└── styles/                # Global styles
    └── globals.css        # Tailwind and custom styles
```

## Setup Instructions

### Prerequisites

- Node.js 18+
- npm, yarn, pnpm, and bun are supported
- Backend API running at `http://localhost:8000`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. **Open the application**
   Visit [http://localhost:3000](http://localhost:3000) in your browser

## Environment Variables

The frontend requires the following environment variables:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AI Todo Chatbot
NEXT_PUBLIC_VERSION=1.0.0
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Lint the codebase
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode

## API Integration

The frontend connects to the backend API at the following endpoints:

### Authentication Endpoints
- `POST /api/auth/signup` - Create account
- `POST /api/auth/signin` - Login to account
- `POST /api/auth/signout` - Logout from account

### Task Endpoints (require authentication)
- `GET /api/users/{user_id}/tasks` - Get user's tasks
- `POST /api/users/{user_id}/tasks` - Create a new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PATCH /api/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete a task

### Chat Endpoint (requires authentication)
- `POST /api/{user_id}/chat` - Send message to AI assistant

## User Flows

### 1. Landing Page (`/`)
- View project introduction
- Navigate to sign in or sign up

### 2. Authentication Flow
- **Sign Up** (`/signup`): Create a new account
- **Sign In** (`/signin`): Log into existing account
- Protected routes redirect unauthenticated users

### 3. Dashboard (`/dashboard`)
- Overview of tasks and AI assistant
- Quick access to chat and task management

### 4. Chat Interface (`/chat`)
- Conversational interface with AI assistant
- Natural language task management
- Real-time responses from AI

### 5. Task Management (`/tasks`)
- View all tasks with filtering options
- Create new tasks
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete

## Component Library

### Authentication Components
- `SignInForm` - Sign in form with validation
- `SignUpForm` - Sign up form with validation
- `ProtectedRoute` - Higher-order component for protected routes

### Chat Components
- `ChatWindow` - Main chat interface
- `MessageBubble` - Individual message display
- `MessageInput` - Input field for sending messages
- `TypingIndicator` - Shows when AI is responding

### Task Components
- `TaskCard` - Visual representation of a task
- `TaskList` - Collection of task cards
- `TaskForm` - Form for creating/updating tasks
- `TaskFilter` - Filtering and sorting controls

### UI Components
- `Button` - Reusable button component
- `Input` - Styled input fields
- `Modal` - Overlay dialogs
- `Spinner` - Loading indicators
- `Alert` - Notification messages

## Styling

The application uses Tailwind CSS for styling with the following principles:

- **Responsive Design**: Mobile-first approach with breakpoints for tablets and desktops
- **Consistent Spacing**: Standardized spacing using Tailwind's spacing scale
- **Color Palette**: Cohesive color scheme with primary, secondary, and accent colors
- **Typography**: Clear hierarchy with appropriate font sizes and weights
- **Accessibility**: Proper contrast ratios and semantic HTML

## State Management

The application uses React Context API for state management:

- **AuthContext**: Manages user authentication state
- **TaskContext**: Manages task-related state
- **ChatContext**: Manages chat-related state

## API Client

The application uses Axios for HTTP requests with the following features:

- **Interceptors**: Automatic JWT token attachment
- **Error Handling**: Centralized error handling
- **Loading States**: Track request status
- **Retry Logic**: Automatic retry for failed requests

## Best Practices

- **Type Safety**: Full TypeScript coverage
- **Component Reusability**: Modular, composable components
- **Performance**: Optimized rendering and data fetching
- **Accessibility**: WCAG-compliant markup
- **Security**: Proper input sanitization and authentication
- **Testing**: Comprehensive test coverage

## Deployment

### Vercel (Recommended)
The easiest way to deploy is using Vercel:

1. Push your code to a Git repository
2. Connect your repository to Vercel
3. Vercel will automatically detect Next.js and deploy

### Other Platforms
For other platforms, ensure you build the application first:
```bash
npm run build
npm start
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run linting and tests (`npm run lint && npm test`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the backend API is running at the configured URL
3. Ensure all environment variables are properly set
4. Review the network tab for API request/response details

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs) - Learn about Next.js features
- [React Documentation](https://react.dev) - Learn about React concepts
- [TypeScript Documentation](https://www.typescriptlang.org/docs/) - Learn about TypeScript
- [Tailwind CSS Documentation](https://tailwindcss.com/docs) - Learn about styling
- [Axios Documentation](https://axios-http.com/docs/intro) - Learn about HTTP requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Next.js for the excellent React framework
- React for the component-based architecture
- Tailwind CSS for the utility-first styling
- Axios for the HTTP client
- All the open-source libraries that made this project possible
