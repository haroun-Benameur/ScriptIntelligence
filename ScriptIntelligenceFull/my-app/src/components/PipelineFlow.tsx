import { ArrowRight } from "lucide-react";

const steps = [
  { label: "FSD", sub: "Source of Truth", color: "bg-agent-fsd" },
  { label: "Extraction", sub: "Scénarios", color: "bg-agent-drift" },
  { label: "Génération", sub: "Tests pytest", color: "bg-agent-test" },
  { label: "Exécution", sub: "Pass / Fail", color: "bg-agent-exec" },
  { label: "Coverage", sub: "Spec Coverage", color: "bg-agent-coverage" },
  { label: "Quality Gate", sub: "PR Decision", color: "bg-agent-orchestrator" },
];

const PipelineFlow = () => {
  return (
    <div className="flex flex-wrap items-center justify-center gap-2 md:gap-0">
      {steps.map((step, i) => (
        <div key={step.label} className="flex items-center">
          <div className="flex flex-col items-center gap-1.5 px-3 py-2">
            <div className={`h-2 w-2 rounded-full ${step.color} animate-pulse-glow`} />
            <span className="text-xs font-semibold text-foreground font-mono">{step.label}</span>
            <span className="text-[10px] text-muted-foreground">{step.sub}</span>
          </div>
          {i < steps.length - 1 && (
            <ArrowRight className="h-3.5 w-3.5 text-muted-foreground/40 hidden md:block" />
          )}
        </div>
      ))}
    </div>
  );
};

export default PipelineFlow;
