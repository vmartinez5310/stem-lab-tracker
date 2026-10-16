import { useQuery } from "@tanstack/react-query";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { TrendingUp, Wallet, Target } from "lucide-react";
import { api } from "../lib/api";

interface Account {
  id: number;
  name: string;
  type: string;
  currency: string;
  balance: string;
  institution?: string;
  color?: string;
}

const cashflowDemo = [
  { month: "May", value: 12400 },
  { month: "Jun", value: 13100 },
  { month: "Jul", value: 12850 },
  { month: "Aug", value: 14200 },
  { month: "Sep", value: 13980 },
  { month: "Oct", value: 15120 },
];

function formatMoney(value: number | string, currency = "USD") {
  const n = typeof value === "string" ? parseFloat(value) : value;
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(n);
}

export function Dashboard() {
  const { data: accounts = [], isLoading } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => api.get<Account[]>("/accounts"),
  });

  const totalBalance = accounts.reduce(
    (sum, a) => sum + parseFloat(a.balance || "0"),
    0
  );

  return (
    <div className="space-y-8">
      <div className="flex items-end justify-between">
        <div>
          <p className="stat-label mb-1">Total Net Position</p>
          <h1 className="stat-value gold-text">
            {isLoading ? "—" : formatMoney(totalBalance)}
          </h1>
        </div>
        <div className="flex items-center gap-2 text-sm text-bank-success">
          <TrendingUp className="h-4 w-4" />
          <span>+4.2% this month</span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 md:grid-cols-3">
        <KpiCard icon={<Wallet className="h-4 w-4 text-bank-gold-400" />} label="Liquid Assets" value={formatMoney(totalBalance * 0.72)} delta="+2.1%" positive />
        <KpiCard icon={<Target className="h-4 w-4 text-bank-info" />} label="Goals Progress" value="68%" delta="On track" positive />
        <KpiCard icon={<TrendingUp className="h-4 w-4 text-bank-success" />} label="Monthly Outflow" value={formatMoney(3840)} delta="-8.4%" positive />
      </div>

      <div className="panel p-6">
        <div className="mb-6">
          <h2 className="font-display text-xl text-bank-platinum">Cash Position</h2>
          <p className="text-xs text-bank-muted mt-0.5">Trailing six months</p>
        </div>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={cashflowDemo}>
              <defs>
                <linearGradient id="goldFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#d4af37" stopOpacity={0.35} />
                  <stop offset="100%" stopColor="#d4af37" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: "#6b7280", fontSize: 12 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fill: "#6b7280", fontSize: 12 }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
              <Tooltip contentStyle={{ background: "#161920", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, fontSize: 13 }} formatter={(v: number) => [formatMoney(v), "Balance"]} />
              <Area type="monotone" dataKey="value" stroke="#d4af37" strokeWidth={2} fill="url(#goldFill)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="panel p-6">
        <h2 className="font-display text-xl text-bank-platinum mb-5">Accounts</h2>
        {isLoading ? (
          <p className="text-sm text-bank-muted">Loading…</p>
        ) : accounts.length === 0 ? (
          <p className="text-sm text-bank-muted">No accounts yet. Create one from the Accounts section.</p>
        ) : (
          <div className="space-y-3">
            {accounts.map((a) => (
              <div key={a.id} className="flex items-center justify-between rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-3 panel-hover">
                <div className="flex items-center gap-3">
                  <div className="h-2.5 w-2.5 rounded-full" style={{ background: a.color || "#d4af37" }} />
                  <div>
                    <div className="text-sm font-medium text-bank-platinum">{a.name}</div>
                    <div className="text-xs text-bank-muted capitalize">{a.type.replace("_", " ")}{a.institution ? ` · ${a.institution}` : ""}</div>
                  </div>
                </div>
                <div className="font-mono text-sm text-bank-platinum">{formatMoney(a.balance, a.currency)}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function KpiCard({ icon, label, value, delta, positive }: { icon: React.ReactNode; label: string; value: string; delta: string; positive?: boolean }) {
  return (
    <div className="panel panel-hover p-5">
      <div className="flex items-center justify-between mb-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/[0.04]">{icon}</div>
        <span className={`text-xs font-medium ${positive ? "text-bank-success" : "text-bank-danger"}`}>{delta}</span>
      </div>
      <p className="stat-label mb-1">{label}</p>
      <p className="font-display text-2xl font-semibold text-bank-platinum">{value}</p>
    </div>
  );
}
