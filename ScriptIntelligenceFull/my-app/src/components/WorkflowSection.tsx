import { GitPullRequest, RefreshCw, Zap } from "lucide-react";

const workflows = [
  {
    icon: Zap,
    title: "Premier lancement",
    steps: [
      "Lecture du FSD",
      "Extraction des scénarios",
      "Génération des tests",
      "Exécution pytest",
      "Calcul Spec Coverage",
    ],
  },
  {
    icon: RefreshCw,
    title: "Changement du FSD",
    steps: [
      "Détection via hash",
      "Comparaison structurée",
      "Identification des différences",
      "Régénération ciblée des tests",
    ],
  },
  {
    icon: GitPullRequest,
    title: "Pull Request",
    steps: [
      "CI lance le système",
      "Quality Gate évaluation",
      "Blocage si critères non remplis",
      "Rapport publié dans la PR",
    ],
  },
];

const WorkflowSection = () => {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {workflows.map((wf) => {
        const Icon = wf.icon;
        return (
          <div key={wf.title} className="rounded-lg border border-border bg-card p-5">
            <div className="flex items-center gap-2 mb-3">
              <Icon className="h-4 w-4 text-primary" />
              <h3 className="text-sm font-semibold text-foreground">{wf.title}</h3>
            </div>
            <ol className="space-y-1.5">
              {wf.steps.map((step, i) => (
                <li key={step} className="flex items-start gap-2 text-xs text-muted-foreground">
                  <span className="font-mono text-primary/60 min-w-[1rem]">{i + 1}.</span>
                  <span className="font-mono">{step}</span>
                </li>
              ))}
            </ol>
          </div>
        );
      })}
    </div>
  );
};

export default WorkflowSection;
