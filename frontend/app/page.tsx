'use client'

import { Button } from '@/components/ui/button'
import Link from 'next/link'
import { ArrowRight, Sparkles, Zap, Shield } from 'lucide-react'
import { useAuth } from '@/lib/auth-context'

export default function LandingPage() {
  const { user } = useAuth()

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-background to-primary/10">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 backdrop-blur-md bg-background/80 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            AI Chat
          </Link>
          <div className="flex items-center gap-4">
            <a href="/docs" className="text-sm text-muted-foreground hover:text-foreground transition">
              Docs
            </a>
            <a href="#features" className="text-sm text-muted-foreground hover:text-foreground transition">
              Features
            </a>
            {user ? (
              <Button asChild>
                <Link href="/chat">Go to Chat</Link>
              </Button>
            ) : (
              <Button asChild>
                <Link href="/auth/login">Get Started</Link>
              </Button>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 sm:py-32">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl opacity-50" />
          <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-accent/20 rounded-full blur-3xl opacity-50" />
        </div>

        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm text-primary">Powered by Advanced AI</span>
          </div>

          <h1 className="text-5xl sm:text-7xl font-bold tracking-tight text-foreground mb-6">
            Have Intelligent{' '}
            <span className="bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent">
              Conversations
            </span>
          </h1>

          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
            Experience the future of AI-powered communication. Fast, intuitive, and designed for meaningful interactions.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            {user ? (
              <Button asChild size="lg" className="bg-primary hover:bg-primary/90">
                <Link href="/chat">
                  Open Chat <ArrowRight className="w-4 h-4 ml-2" />
                </Link>
              </Button>
            ) : (
              <>
                <Button asChild size="lg" className="bg-primary hover:bg-primary/90">
                  <Link href="/auth/signup">
                    Start Chatting <ArrowRight className="w-4 h-4 ml-2" />
                  </Link>
                </Button>
                <Button asChild variant="outline" size="lg" className="border-border hover:bg-border/10">
                  <Link href="/auth/login">Sign In</Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 sm:py-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl sm:text-5xl font-bold text-center mb-4">
            Why Choose Us
          </h2>
          <p className="text-center text-muted-foreground mb-16 max-w-2xl mx-auto text-lg">
            Everything you need for seamless AI conversations in one platform.
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-accent/10 rounded-2xl opacity-0 group-hover:opacity-100 transition duration-300" />
              <div className="relative bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-8 hover:border-primary/50 transition duration-300">
                <Zap className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-3">Lightning Fast</h3>
                <p className="text-muted-foreground">
                  Real-time responses powered by state-of-the-art language models. Get answers instantly.
                </p>
              </div>
            </div>

            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-accent/10 rounded-2xl opacity-0 group-hover:opacity-100 transition duration-300" />
              <div className="relative bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-8 hover:border-primary/50 transition duration-300">
                <Shield className="w-12 h-12 text-accent mb-4" />
                <h3 className="text-xl font-semibold mb-3">Secure & Private</h3>
                <p className="text-muted-foreground">
                  Your conversations are encrypted and stored securely. Your privacy is our priority.
                </p>
              </div>
            </div>

            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-accent/10 rounded-2xl opacity-0 group-hover:opacity-100 transition duration-300" />
              <div className="relative bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-8 hover:border-primary/50 transition duration-300">
                <Sparkles className="w-12 h-12 text-secondary mb-4" />
                <h3 className="text-xl font-semibold mb-3">Context Aware</h3>
                <p className="text-muted-foreground">
                  The AI remembers your conversation history for more meaningful and coherent exchanges.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 sm:py-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto bg-gradient-to-r from-primary/20 to-accent/20 rounded-3xl border border-primary/20 p-12 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Transform Your Conversations?
          </h2>
          <p className="text-lg text-muted-foreground mb-8">
            Join thousands of users experiencing the power of AI-driven communication.
          </p>
          {user ? (
            <Button asChild size="lg" className="bg-primary hover:bg-primary/90">
              <Link href="/chat">
                Start Chatting Now <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </Button>
          ) : (
            <Button asChild size="lg" className="bg-primary hover:bg-primary/90">
              <Link href="/auth/signup">
                Create Free Account <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </Button>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center">
          <p className="text-muted-foreground text-sm">
            © 2026 AI Chat. All rights reserved.
          </p>
          <div className="flex gap-6 mt-4 sm:mt-0">
            <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition">
              Privacy
            </a>
            <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition">
              Terms
            </a>
            <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition">
              Contact
            </a>
          </div>
        </div>
      </footer>
    </main>
  )
}
