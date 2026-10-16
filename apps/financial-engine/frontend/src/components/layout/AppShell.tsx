import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Wallet,
  ArrowLeftRight,
  LogOut,
  Sparkles,
} from "lucide-react";
import { useAuthStore } from "../../lib/auth";
import clsx from "clsx";

const nav = [
  { to: "/", label: "Overview", icon: LayoutDashboard },
  { to: "/accounts", label: "Accounts", icon: Wallet },
  { to: "/transactions", label: "Activity", icon: ArrowLeftRight },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const logout = useAuthStore((s) => s.logout);

  return (
    <div className="min-h-screen flex">
      <aside className="fixed inset-y-0 left-0 z-30 flex w-64 flex-col border-r border-white/[0.06] bg-bank-abyss/90 backdrop-blur-xl">
        <div className="flex h-16 items-center gap-3 px-6">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gold-degrade shadow-glow">
            <Sparkles className="h-4 w-4 text-bank-void" />
          </div>
          <div>
            <div className="font-display text-lg font-semibold tracking-wide gold-text">
              Financial Engine
            </div>
            <div className="text-[10px] uppercase tracking-[0.2em] text-bank-muted">
              Private Banking
            </div>
          </div>
        </div>

        <nav className="mt-6 flex flex-1 flex-col gap-1 px-3">
          {nav.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              className={({ isActive }) =>
                clsx("nav-link", isActive && "nav-link-active")
              }
            >
              <Icon className="h-4 w-4 opacity-80" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-white/[0.06] p-4">
          <button
            onClick={logout}
            className="nav-link w-full text-bank-muted hover:text-bank-danger"
          >
            <LogOut className="h-4 w-4" />
            Sign out
          </button>
        </div>
      </aside>

      <main className="ml-64 flex-1 min-h-screen">
        <div className="mx-auto max-w-6xl px-8 py-8 animate-fade-in">
          {children}
        </div>
      </main>
    </div>
  );
}
