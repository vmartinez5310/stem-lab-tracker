import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Building2 } from "lucide-react";
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

const ACCOUNT_TYPES = [
  "checking", "savings", "cash", "credit_card", "investment", "loan", "other",
];

function formatMoney(value: string, currency = "USD") {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(parseFloat(value || "0"));
}

export function Accounts() {
  const qc = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    name: "",
    type: "checking",
    currency: "USD",
    balance: "0",
    institution: "",
  });

  const { data: accounts = [], isLoading } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => api.get<Account[]>("/accounts"),
  });

  const createMutation = useMutation({
    mutationFn: (body: typeof form) =>
      api.post("/accounts", {
        ...body,
        balance: parseFloat(body.balance) || 0,
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["accounts"] });
      setShowForm(false);
      setForm({ name: "", type: "checking", currency: "USD", balance: "0", institution: "" });
    },
  });

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-3xl font-semibold text-bank-platinum">Accounts</h1>
          <p className="mt-1 text-sm text-bank-muted">Manage balances and institutions</p>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4" />
          New Account
        </button>
      </div>

      {showForm && (
        <div className="panel p-6 animate-slide-up">
          <h2 className="font-display text-lg text-bank-platinum mb-4">Create Account</h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div>
              <label className="label">Name</label>
              <input className="input-field" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Primary Checking" />
            </div>
            <div>
              <label className="label">Type</label>
              <select className="input-field" value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
                {ACCOUNT_TYPES.map((t) => (
                  <option key={t} value={t}>{t.replace("_", " ")}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="label">Currency</label>
              <input className="input-field" value={form.currency} onChange={(e) => setForm({ ...form, currency: e.target.value })} />
            </div>
            <div>
              <label className="label">Opening Balance</label>
              <input className="input-field" type="number" step="0.01" value={form.balance} onChange={(e) => setForm({ ...form, balance: e.target.value })} />
            </div>
            <div className="md:col-span-2">
              <label className="label">Institution</label>
              <input className="input-field" value={form.institution} onChange={(e) => setForm({ ...form, institution: e.target.value })} placeholder="Optional" />
            </div>
          </div>
          <div className="mt-5 flex gap-3">
            <button className="btn-primary" onClick={() => createMutation.mutate(form)} disabled={!form.name || createMutation.isPending}>
              {createMutation.isPending ? "Saving…" : "Create"}
            </button>
            <button className="btn-ghost" onClick={() => setShowForm(false)}>Cancel</button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {isLoading && <p className="text-sm text-bank-muted col-span-2">Loading accounts…</p>}
        {!isLoading && accounts.length === 0 && (
          <div className="panel col-span-2 p-10 text-center">
            <Building2 className="mx-auto h-8 w-8 text-bank-muted mb-3" />
            <p className="text-sm text-bank-muted">No accounts configured. Create your first account to begin.</p>
          </div>
        )}
        {accounts.map((a) => (
          <div key={a.id} className="panel panel-hover p-5">
            <div className="flex items-start justify-between">
              <div>
                <div className="text-sm font-medium text-bank-platinum">{a.name}</div>
                <div className="mt-0.5 text-xs capitalize text-bank-muted">
                  {a.type.replace("_", " ")}{a.institution ? ` · ${a.institution}` : ""}
                </div>
              </div>
              <div className="h-2 w-2 rounded-full mt-1.5" style={{ background: a.color || "#d4af37" }} />
            </div>
            <div className="mt-4 font-display text-2xl font-semibold text-bank-platinum">
              {formatMoney(a.balance, a.currency)}
            </div>
            <div className="mt-1 text-xs text-bank-muted uppercase tracking-wider">{a.currency}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
