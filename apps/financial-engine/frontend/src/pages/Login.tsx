import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles } from "lucide-react";
import { iamRegister, iamRequestOtp, iamVerifyOtp } from "../lib/api";
import { useAuthStore } from "../lib/auth";

type Step = "email" | "otp";

export function Login() {
  const [step, setStep] = useState<Step>("email");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [otp, setOtp] = useState("");
  const [devOtp, setDevOtp] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const setTokens = useAuthStore((s) => s.setTokens);
  const navigate = useNavigate();

  async function handleRequestOtp(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      try {
        await iamRegister(email, fullName || undefined);
      } catch {
        // already registered
      }
      const res = await iamRequestOtp(email);
      setDevOtp(res.dev_otp || null);
      setStep("otp");
    } catch (err: any) {
      setError(err.message || "Could not request OTP");
    } finally {
      setLoading(false);
    }
  }

  async function handleVerify(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await iamVerifyOtp(email, otp);
      if (!data.apps?.includes("financial-engine") && !data.apps?.includes("admin")) {
        setError(
          "You do not have access to Financial Engine yet. An admin must grant the role (POST /apps/grant-role)."
        );
        return;
      }
      setTokens(data.access_token, "");
      navigate("/");
    } catch (err: any) {
      setError(err.message || "Invalid OTP");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center px-4">
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 left-1/2 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-bank-gold-500/[0.07] blur-[120px]" />
        <div className="absolute bottom-0 right-0 h-[300px] w-[400px] rounded-full bg-bank-gold-700/[0.05] blur-[100px]" />
      </div>

      <div className="relative w-full max-w-md animate-slide-up">
        <div className="mb-10 text-center">
          <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-gold-degrade shadow-glow">
            <Sparkles className="h-6 w-6 text-bank-void" />
          </div>
          <h1 className="font-display text-3xl font-semibold tracking-wide gold-text">
            Financial Engine
          </h1>
          <p className="mt-2 text-sm text-bank-muted tracking-wide">
            STEM-Lab · Shared identity
          </p>
        </div>

        <form
          onSubmit={step === "email" ? handleRequestOtp : handleVerify}
          className="panel p-8 space-y-5"
        >
          {error && (
            <div className="rounded-lg border border-bank-danger/30 bg-bank-danger/10 px-4 py-2.5 text-sm text-bank-danger">
              {error}
            </div>
          )}

          {step === "email" ? (
            <>
              <div>
                <label className="label" htmlFor="email">Email</label>
                <input id="email" type="email" className="input-field" value={email}
                  onChange={(e) => setEmail(e.target.value)} required placeholder="you@domain.com" />
              </div>
              <div>
                <label className="label" htmlFor="name">Full name (optional)</label>
                <input id="name" className="input-field" value={fullName}
                  onChange={(e) => setFullName(e.target.value)} placeholder="Valente Martínez" />
              </div>
              <button type="submit" className="btn-primary w-full mt-2" disabled={loading}>
                {loading ? "Sending code…" : "Continue with OTP"}
              </button>
            </>
          ) : (
            <>
              <p className="text-sm text-bank-silver">
                Code sent to <span className="text-bank-platinum">{email}</span>
              </p>
              {devOtp && (
                <div className="rounded-lg border border-bank-gold-500/20 bg-bank-gold-500/10 px-4 py-2 text-xs text-bank-gold-200">
                  Dev OTP: <span className="font-mono font-semibold">{devOtp}</span>
                </div>
              )}
              <div>
                <label className="label" htmlFor="otp">One-time code</label>
                <input id="otp" className="input-field font-mono tracking-widest text-center text-lg"
                  value={otp} onChange={(e) => setOtp(e.target.value)} required maxLength={6} placeholder="••••••" />
              </div>
              <button type="submit" className="btn-primary w-full mt-2" disabled={loading}>
                {loading ? "Verifying…" : "Enter"}
              </button>
              <button type="button" className="btn-ghost w-full" onClick={() => { setStep("email"); setOtp(""); setDevOtp(null); }}>
                Back
              </button>
            </>
          )}
        </form>

        <p className="mt-6 text-center text-xs text-bank-muted">
          Powered by Shared-Auth-Service · STEM-Lab Tracker
        </p>
      </div>
    </div>
  );
}
