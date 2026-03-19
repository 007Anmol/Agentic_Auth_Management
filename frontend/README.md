# AI Chat Application

A modern, end-to-end AI chat application built with Next.js 16, Supabase, and the Vercel AI SDK.

## Features

- **Intelligent Conversations**: Powered by OpenAI's GPT-4 Turbo
- **User Authentication**: Secure Supabase authentication with session management
- **Real-time Chat**: Streaming responses with optimized UX
- **Dark Theme**: Modern glassmorphism design with purple/blue gradient accents
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Context Aware**: AI remembers conversation history for coherent exchanges

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript
- **UI Components**: shadcn/ui with Tailwind CSS v4
- **Authentication**: Supabase Auth
- **Database**: Supabase PostgreSQL
- **AI**: Vercel AI SDK v6 with OpenAI
- **Styling**: Tailwind CSS with custom design tokens

## Getting Started

### Prerequisites

- Node.js 18+ and pnpm
- Supabase account
- OpenAI API key

### Installation

1. Clone the repository and install dependencies:
```bash
pnpm install
```

2. Set up environment variables in `.env.local`:
```bash
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

3. Run the development server:
```bash
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
app/
├── page.tsx              # Landing page
├── chat/
│   └── page.tsx         # Chat interface
├── auth/
│   ├── login/page.tsx   # Login page
│   ├── signup/page.tsx  # Signup page
│   └── callback/route.ts # Auth callback
├── api/
│   └── chat/route.ts    # Chat API endpoint
├── layout.tsx           # Root layout with auth provider
└── globals.css          # Global styles and design tokens

components/
├── chat-message.tsx     # Message display component
├── chat-input.tsx       # Input form component
└── chat-sidebar.tsx     # Sidebar with chat history

lib/
├── auth-context.tsx     # Auth context and hooks
├── supabase/
│   ├── client.ts       # Client-side Supabase setup
│   └── server.ts       # Server-side Supabase setup
└── utils.ts            # Utility functions
```

## Key Features Implementation

### Authentication
- Email/password signup and login
- Session management with Supabase
- Protected chat routes with automatic redirects

### Chat Interface
- Real-time message streaming
- Auto-scrolling message view
- Loading indicators with animations
- Mobile-responsive sidebar

### Design System
- Purple to blue gradient theme
- Glassmorphism effects with backdrop blur
- Smooth animations and transitions
- Semantic color tokens for easy theming

## Database Schema

The application uses the following Supabase tables:

- **users**: Extended auth.users with custom fields
- **chats**: Stores conversation metadata
- **messages**: Stores individual messages with role and content

All tables have Row Level Security (RLS) policies enabled.

## Deployment

Deploy to Vercel with one click:

```bash
vercel deploy
```

Make sure to configure the environment variables in your Vercel project settings.

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - See LICENSE file for details
