import { streamText } from 'ai'
import { createClient } from '@/lib/supabase/server'

export async function POST(request: Request) {
  const { messages } = await request.json()

  // Get the authenticated user
  const supabase = await createClient()
  const {
    data: { user },
  } = await supabase.auth.getUser()

  if (!user) {
    return new Response('Unauthorized', { status: 401 })
  }

  const result = streamText({
    model: 'openai/gpt-4-turbo',
    system:
      'You are a helpful, intelligent AI assistant. Provide clear, concise, and thoughtful responses. Format your responses using markdown when appropriate.',
    messages,
  })

  return result.toUIMessageStreamResponse()
}
