'use client'

import { Button } from '@/components/ui/button'
import { useAuth } from '@/lib/auth-context'
import { Plus, LogOut, Menu } from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'

interface ChatSidebarProps {
  onNewChat: () => void
  isMobileOpen?: boolean
  onClose?: () => void
}

export function ChatSidebar({ onNewChat, isMobileOpen = false, onClose }: ChatSidebarProps) {
  const { user, signOut } = useAuth()
  const [isLoading, setIsLoading] = useState(false)

  const handleSignOut = async () => {
    setIsLoading(true)
    await signOut()
  }

  return (
    <div className={`
      h-screen bg-card/50 backdrop-blur-sm border-r border-border flex flex-col
      fixed lg:relative w-64 z-40 lg:z-auto
      transition-transform duration-300 ease-out
      ${isMobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
    `}>
      {/* Close button on mobile */}
      {isMobileOpen && onClose && (
        <button
          onClick={onClose}
          className="lg:hidden absolute top-4 right-4 p-2 rounded hover:bg-muted/50"
        >
          ✕
        </button>
      )}

      {/* Header */}
      <div className="p-4 border-b border-border">
        <Button
          onClick={onNewChat}
          className="w-full bg-primary hover:bg-primary/90 text-primary-foreground gap-2"
        >
          <Plus className="w-4 h-4" />
          New Chat
        </Button>
      </div>

      {/* Chat History - empty state for now */}
      <div className="flex-1 p-4">
        <p className="text-xs text-muted-foreground mb-4">Recent</p>
        <div className="text-sm text-muted-foreground">
          No conversations yet. Start a new chat!
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-border space-y-2">
        <div className="text-xs text-muted-foreground truncate">
          {user?.email}
        </div>
        <Button
          onClick={handleSignOut}
          disabled={isLoading}
          variant="outline"
          className="w-full justify-start gap-2 border-border text-destructive hover:text-destructive hover:bg-destructive/10"
        >
          <LogOut className="w-4 h-4" />
          {isLoading ? 'Signing out...' : 'Sign Out'}
        </Button>
      </div>
    </div>
  )
}
