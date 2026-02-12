import { useQuery } from "@tanstack/react-query";
import { api, type SpecCoverageScenario } from "@/lib/api";
import QualityGate from "@/components/QualityGate";

const SpecCoverage = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ["spec-coverage"],
    queryFn: () => api.getSpecCoverage(),
    refetchInterval: 10000,
  });

  if (isLoading) {
    return (
      <div className="space-y-5">
        <p className="text-sm text-muted-foreground">Chargement du Spec Coverage...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="space-y-5">
        <p className="text-sm text-destructive">
          Impossible de charger le Spec Coverage. Assurez-vous que le backend est démarré.
        </p>
      </div>
    );
  }

  const { scenarios, covered, total, percentage, uncovered_critical, quality_gate } = data;
  const uncoveredCritical = uncovered_critical || [];

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <div className="lg:col-span-2 space-y-5">
        {/* Metric */}
        <div className="flex items-end gap-4">
          <div>
            <p className="text-xs text-muted-foreground font-mono uppercase tracking-wider">
              Spec Coverage
            </p>
            <p className="text-5xl font-bold text-gradient-primary font-mono">{percentage}%</p>
          </div>
          <p className="text-sm text-muted-foreground mb-1">
            {covered}/{total} scénarios couverts
          </p>
        </div>

        {/* Bar */}
        <div className="h-2 w-full rounded-full bg-secondary overflow-hidden">
          <div
            className="h-full rounded-full bg-primary transition-all duration-1000"
            style={{ width: `${percentage}%` }}
          />
        </div>

        {/* Scenarios table */}
        <div className="rounded-md border border-border overflow-hidden">
          <table className="w-full text-xs">
            <thead>
              <tr className="bg-secondary/50">
                <th className="text-left px-3 py-2 font-mono text-muted-foreground">ID</th>
                <th className="text-left px-3 py-2 text-muted-foreground">Scénario</th>
                <th className="text-center px-3 py-2 text-muted-foreground">Critique</th>
                <th className="text-center px-3 py-2 text-muted-foreground">Couvert</th>
              </tr>
            </thead>
            <tbody>
              {scenarios.map((s: SpecCoverageScenario) => (
                <tr
                  key={s.id}
                  className="border-t border-border hover:bg-secondary/30 transition-colors"
                >
                  <td className="px-3 py-2 font-mono text-primary">{s.id}</td>
                  <td className="px-3 py-2 text-foreground">{s.name}</td>
                  <td className="px-3 py-2 text-center">
                    {s.critical && (
                      <span className="inline-block h-2 w-2 rounded-full bg-warning" />
                    )}
                  </td>
                  <td className="px-3 py-2 text-center">
                    <span
                      className={`inline-block h-2 w-2 rounded-full ${
                        s.covered ? "bg-success" : "bg-destructive"
                      }`}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Uncovered critical alert */}
        {uncoveredCritical.length > 0 && (
          <div className="rounded-md border border-destructive/30 bg-destructive/5 p-3">
            <p className="text-xs font-semibold text-destructive mb-1">
              ⚠ {uncoveredCritical.length} scénario(s) critique(s) non couvert(s)
            </p>
            <ul className="space-y-0.5">
              {uncoveredCritical.map((s) => (
                <li key={s.id} className="text-xs text-muted-foreground font-mono">
                  {s.id} — {s.name}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Quality Gate - intégré avec les mêmes données */}
      <div>
        <QualityGate
          testsPass={quality_gate.tests_pass}
          specCoverageOk={quality_gate.spec_coverage_ok}
          criticalCovered={quality_gate.critical_covered}
        />
      </div>
    </div>
  );
};

export default SpecCoverage;
