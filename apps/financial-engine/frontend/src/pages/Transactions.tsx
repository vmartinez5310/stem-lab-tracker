import { useQuery } from "@tanstack/react-query";
import { format, parseISO } from "date-fns";
import { ArrowUpRight, ArrowDownRight, ArrowLeftRight } from "lucide-react";
import { api } from "../lib/api";

interface Transaction {
  id: number;
  account_id: number;
  type: string;
  amount: string;
  currency: string;
  description?: string;
  merchant?: string;
  date: string;
}

function formatMoney(value: string, currency = "USD") {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(parseFloat(value || "0"));
}

const typeIcon = {
  income: <ArrowUpRight className="h-4 w-4 text-bank-success" />,
  expense: <ArrowDownRight className="h-4 w-4 text-bank-danger" />,
  transfer: <ArrowLeftRight className="h-4 w-4 text-bank-info" />,
};

export function Transactions() {
  const { data: transactions = [], isLoading } = useQuery({
    queryKey: ["transactions"],
    queryFn: () => api.get<Transaction[]>("/transactions?limit=100"),
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-3xl font-semibold text-bank-platinum">
          Activity
        </h1>
        <p className="mt-1 text-sm text-bank-muted">
          Recent movements across all accounts
        </p>
      </div>

      <div className="panel overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-sm text-bank-muted">Loading activity…</div>
        ) : transactions.length === 0 ? (
          <div className="p-10 text-center text-sm text-bank-muted">
            No transactions recorded yet.
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/[0.06] text-left text-xs uppercase tracking-wider text-bank-muted">
                <th className="px-5 py-3.5 font-medium">Date</th>
                <th className="px-5 py-3.5 font-medium">Description</th>
                <th className="px-5 py-3.5 font-medium">Type</th>
                <th className="px-5 py-3.5 font-medium text-right">Amount</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((tx) => (
                <tr
                  key={tx.id}
                  className="border-b border-white/[0.03] transition-colors hover:bg-white/[0.02]"
                >
                  <td className="px-5 py-3.5 text-bank-silver font-mono text-xs">
                    {format(parseISO(tx.date), "dd MMM yyyy")}
                  </td>
                  <td className="px-5 py-3.5">
                    <div className="text-bank-platinum">
                      {tx.description || tx.merchant || "—"}
                    </div>
                    {tx.merchant && tx.description && (
                      <div className="text-xs text-bank-muted">{tx.merchant}</div>
                    )}
                  </td>
                  <td className="px-5 py-3.5">
                    <div className="flex items-center gap-2 capitalize text-bank-silver">
                      {typeIcon[tx.type as keyof typeof typeIcon]}
                      {tx.type}
                    </div>
                  </td>
                  <td
                    className={`px-5 py-3.5 text-right font-mono ${
                      tx.type === "income"
                        ? "text-bank-success"
                        : tx.type === "expense"
                        ? "text-bank-platinum"
                        : "text-bank-silver"
                    }`}
                  >
                    {tx.type === "income" ? "+" : tx.type === "expense" ? "−" : ""}
                    {formatMoney(tx.amount, tx.currency)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
