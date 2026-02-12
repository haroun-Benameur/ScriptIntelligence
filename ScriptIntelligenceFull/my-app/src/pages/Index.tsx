import { Brain } from "lucide-react";
import AgentCard from "@/components/AgentCard";
import PipelineFlow from "@/components/PipelineFlow";
import SpecCoverage from "@/components/SpecCoverage";
import WorkflowSection from "@/components/WorkflowSection";
import FSDUploadWorkflow from "@/components/FSDUploadWorkflow";
import { agents } from "@/data/agents";

const Index = () => {
  return (
    <div className="min-h-screen bg-background bg-grid">
      <div className="mx-auto max-w-6xl px-4 py-12 space-y-12">
        {/* Header */}
        <header className="text-center space-y-3">
          <div className="flex items-center justify-center gap-3">
            <Brain className="h-8 w-8 text-primary" />
            <h1 className="text-3xl md:text-4xl font-bold text-gradient-primary font-mono">
              Spec Intelligence
            </h1>
          </div>
          <p className="text-sm text-muted-foreground max-w-2xl mx-auto">
            AI Agent for Specification-Driven Test Orchestration with Drift Detection
          </p>
          <p className="text-xs text-muted-foreground/60 font-mono">
            FSD → Scénarios → Tests → Exécution → Coverage → Quality Gate
          </p>
        </header>

        {/* FSD Upload & Test Generation */}
        <section>
          <SectionTitle>Upload FSD & Génération de tests</SectionTitle>
          <FSDUploadWorkflow />
        </section>

        {/* Pipeline */}
        <section>
          <SectionTitle>Pipeline d'Orchestration</SectionTitle>
          <div className="rounded-lg border border-border bg-card/50 p-6">
            <PipelineFlow />
          </div>
        </section>

        {/* Agents */}
        <section>
          <SectionTitle>Architecture Multi-Agents</SectionTitle>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent, i) => (
              <AgentCard key={agent.id} agent={agent} index={i} />
            ))}
          </div>
        </section>

        {/* Workflows */}
        <section>
          <SectionTitle>Modes de Fonctionnement</SectionTitle>
          <WorkflowSection />
        </section>

        {/* Spec Coverage + Quality Gate (données backend) */}
        <section>
          <SectionTitle>Spec Coverage — Innovation Clé</SectionTitle>
          <SpecCoverage />
        </section>

        {/* Footer */}
        <footer className="text-center pt-8 border-t border-border">
          <p className="text-xs text-muted-foreground font-mono">
            Spec Coverage = % des scénarios métier couverts par des tests
          </p>
          <p className="text-xs text-muted-foreground/50 mt-1">
            Powered by FastAPI · Multi-Agent Architecture · LLM Orchestration
          </p>
        </footer>
      </div>
    </div>
  );
};

const SectionTitle = ({ children }: { children: React.ReactNode }) => (
  <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
    <span className="h-1 w-4 rounded-full bg-primary" />
    {children}
  </h2>
);

export default Index;
