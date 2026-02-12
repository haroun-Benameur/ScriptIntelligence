import { FileText, GitCompare, TestTube, Play, BarChart3, Cpu } from "lucide-react";
import type { LucideIcon } from "lucide-react";

export interface AgentInfo {
  id: string;
  name: string;
  icon: LucideIcon;
  colorClass: string;
  borderClass: string;
  bgClass: string;
  description: string;
  capabilities: string[];
}

export const agents: AgentInfo[] = [
  {
    id: "fsd",
    name: "FSD Agent",
    icon: FileText,
    colorClass: "text-agent-fsd",
    borderClass: "border-agent-fsd/30",
    bgClass: "bg-agent-fsd/10",
    description: "Analyse le FSD et extrait les scénarios fonctionnels",
    capabilities: [
      "Parsing du document FSD",
      "Extraction scénarios (REQ-01…)",
      "Registre structuré JSON",
    ],
  },
  {
    id: "drift",
    name: "Drift Agent",
    icon: GitCompare,
    colorClass: "text-agent-drift",
    borderClass: "border-agent-drift/30",
    bgClass: "bg-agent-drift/10",
    description: "Détecte les dérives entre versions du FSD",
    capabilities: [
      "Comparaison structurée",
      "Détection ajouts / modifs / suppressions",
      "Mise à jour ciblée des tests",
    ],
  },
  {
    id: "test",
    name: "Test Agent",
    icon: TestTube,
    colorClass: "text-agent-test",
    borderClass: "border-agent-test/30",
    bgClass: "bg-agent-test/10",
    description: "Génère automatiquement des tests pytest",
    capabilities: [
      "Génération pytest automatique",
      "Liaison REQ-ID via markers",
      "Respect conventions projet",
    ],
  },
  {
    id: "exec",
    name: "Execution Agent",
    icon: Play,
    colorClass: "text-agent-exec",
    borderClass: "border-agent-exec/30",
    bgClass: "bg-agent-exec/10",
    description: "Exécute les tests et analyse les résultats",
    capabilities: [
      "Exécution tests automatique",
      "Analyse pass/fail",
      "Stacktraces et diagnostics",
    ],
  },
  {
    id: "coverage",
    name: "Coverage Agent",
    icon: BarChart3,
    colorClass: "text-agent-coverage",
    borderClass: "border-agent-coverage/30",
    bgClass: "bg-agent-coverage/10",
    description: "Calcule le Spec Coverage métier",
    capabilities: [
      "Spec Coverage %",
      "Vérification couverture scénarios",
      "Identification gaps critiques",
    ],
  },
  {
    id: "orchestrator",
    name: "Orchestrator",
    icon: Cpu,
    colorClass: "text-agent-orchestrator",
    borderClass: "border-agent-orchestrator/30",
    bgClass: "bg-agent-orchestrator/10",
    description: "Coordonne tous les agents et gère le Quality Gate",
    capabilities: [
      "Coordination multi-agents",
      "Quality Gate décisionnel",
      "Blocage PR intelligent",
    ],
  },
];
