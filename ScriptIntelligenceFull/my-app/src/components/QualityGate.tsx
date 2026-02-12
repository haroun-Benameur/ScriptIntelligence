import { ShieldCheck, ShieldX, ShieldAlert } from "lucide-react";

interface QualityGateProps {
  testsPass: boolean;
  specCoverageOk: boolean;
  criticalCovered: boolean;
}

const QualityGate = ({ testsPass, specCoverageOk, criticalCovered }: QualityGateProps) => {
  const allPass = testsPass && specCoverageOk && criticalCovered;

  const checks = [
    { label: "Tests passent", ok: testsPass },
    { label: "Spec Coverage ≥ 80%", ok: specCoverageOk },
    { label: "Critiques couverts", ok: criticalCovered },
  ];

  return (
    <div
      className={`rounded-lg border p-5 ${
        allPass
          ? "border-success/30 glow-success"
          : "border-destructive/30"
      }`}
    >
      <div className="flex items-center gap-3 mb-4">
        {allPass ? (
          <ShieldCheck className="h-8 w-8 text-success" />
        ) : (
          <ShieldX className="h-8 w-8 text-destructive" />
        )}
        <div>
          <h3 className={`text-lg font-bold ${allPass ? "text-success" : "text-destructive"}`}>
            Quality Gate — {allPass ? "PASS" : "BLOCKED"}
          </h3>
          <p className="text-xs text-muted-foreground">
            {allPass ? "La PR peut être mergée" : "La PR est bloquée"}
          </p>
        </div>
      </div>

      <div className="space-y-2">
        {checks.map((c) => (
          <div key={c.label} className="flex items-center gap-2">
            {c.ok ? (
              <ShieldCheck className="h-4 w-4 text-success" />
            ) : (
              <ShieldAlert className="h-4 w-4 text-destructive" />
            )}
            <span className={`text-sm font-mono ${c.ok ? "text-success" : "text-destructive"}`}>
              {c.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default QualityGate;
