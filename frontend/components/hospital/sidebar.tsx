"use client"

import { Suspense } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Home, Users, AlertTriangle, FileText, Stethoscope, Activity } from "lucide-react"

const navItems = [
  { href: "/", label: "Staff Intake", icon: Home },
  { href: "/doctor", label: "Doctor Dashboard", icon: Stethoscope },
  { href: "/patients", label: "Patients", icon: Users },
  { href: "/triage", label: "Case Overview", icon: AlertTriangle },
  { href: "/reports", label: "Reports", icon: FileText },
]

function NavLinks() {
  const pathname = usePathname()

  return (
    <nav className="flex flex-col gap-1 p-4">
      {navItems.map((item) => {
        const isActive = pathname === item.href
        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
              isActive
                ? "bg-sidebar-accent text-sidebar-accent-foreground"
                : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground",
            )}
          >
            <item.icon className="h-5 w-5" />
            {item.label}
          </Link>
        )
      })}
    </nav>
  )
}

function NavLinksFallback() {
  return (
    <nav className="flex flex-col gap-1 p-4">
      {navItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-sidebar-foreground/70 transition-colors hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
        >
          <item.icon className="h-5 w-5" />
          {item.label}
        </Link>
      ))}
    </nav>
  )
}

export function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 bg-sidebar text-sidebar-foreground">
      <div className="flex h-16 items-center gap-3 border-b border-sidebar-border px-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-sidebar-primary">
          <Activity className="h-5 w-5 text-sidebar-primary-foreground" />
        </div>
        <div>
          <h1 className="text-lg font-semibold tracking-tight">MediCare</h1>
          <p className="text-xs text-sidebar-foreground/60">AI Triage System</p>
        </div>
      </div>
      <Suspense fallback={<NavLinksFallback />}>
        <NavLinks />
      </Suspense>

    </aside>
  )
}
