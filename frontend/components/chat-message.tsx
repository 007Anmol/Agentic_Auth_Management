import { UIMessage } from 'ai'
import { cn } from '@/lib/utils'
import { Check, Copy } from 'lucide-react'
import { useState } from 'react'

interface ChatMessageProps {
  message: UIMessage
}

function getMessageText(message: UIMessage): string {
  if (!message.parts || !Array.isArray(message.parts)) return ''
  return message.parts
    .filter((p): p is { type: 'text'; text: string } => p.type === 'text')
    .map((p) => p.text)
    .join('')
}

export function ChatMessage({ message }: ChatMessageProps) {
  const [copied, setCopied] = useState(false)
  const text = getMessageText(message)
  const isUser = message.role === 'user'

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div
      className={cn('flex gap-3 mb-4 animate-in fade-in-50 duration-300', isUser && 'justify-end')}
    >
      <div
        className={cn(
          'max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-lg',
          isUser
            ? 'bg-primary text-primary-foreground rounded-br-none'
            : 'bg-card border border-border rounded-bl-none'
        )}
      >
        <p className="text-sm whitespace-pre-wrap break-words">{text}</p>
        {!isUser && (
          <button
            onClick={handleCopy}
            className="mt-2 inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs hover:bg-muted/50 transition opacity-0 group-hover:opacity-100"
          >
            {copied ? (
              <>
                <Check className="w-3 h-3" />
                Copied
              </>
            ) : (
              <>
                <Copy className="w-3 h-3" />
                Copy
              </>
            )}
          </button>
        )}
      </div>
    </div>
  )
}
