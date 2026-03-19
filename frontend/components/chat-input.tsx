'use client'

import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Send } from 'lucide-react'
import { useRef, useEffect } from 'react'

interface ChatInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: (message: string) => void
  disabled: boolean
}

export function ChatInput({ value, onChange, onSubmit, disabled }: ChatInputProps) {
  const inputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (value.trim()) {
      onSubmit(value)
    }
  }

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 items-end w-full">
      <div className="flex-1">
        <Input
          ref={inputRef}
          type="text"
          placeholder="Ask me anything..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          className="bg-input border-border focus:ring-2 focus:ring-primary disabled:opacity-50"
        />
      </div>
      <Button
        type="submit"
        disabled={disabled || !value.trim()}
        className="bg-primary hover:bg-primary/90 text-primary-foreground px-4"
      >
        <Send className="w-4 h-4" />
      </Button>
    </form>
  )
}
