import type { AgentInfo } from "@/data/agents";

interface AgentCardProps {
  agent: AgentInfo;
  index: number;
}

const AgentCard = ({ agent, index }: AgentCardProps) => {
  const Icon = agent.icon;

  return (
    <div
      className={`group relative rounded-lg border ${agent.borderClass} bg-card p-5 transition-all duration-300 hover:glow-primary`}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-3">
        <div className={`flex h-10 w-10 items-center justify-center rounded-md ${agent.bgClass}`}>
          <Icon className={`h-5 w-5 ${agent.colorClass}`} />
        </div>
        <div>
          <h3 className={`font-semibold text-sm ${agent.colorClass}`}>{agent.name}</h3>
          <p className="text-xs text-muted-foreground">{agent.description}</p>
        </div>
      </div>

      {/* Capabilities */}
      <ul className="space-y-1.5">
        {agent.capabilities.map((cap) => (
          <li key={cap} className="flex items-center gap-2 text-xs text-muted-foreground">
            <span className={`h-1 w-1 rounded-full ${agent.bgClass} ${agent.colorClass}`} />
            <span className="font-mono">{cap}</span>
          </li>
        ))}
      </ul>

      {/* Decorative corner */}
      <div
        className={`absolute top-0 right-0 h-8 w-8 rounded-tr-lg rounded-bl-lg ${agent.bgClass} opacity-50 group-hover:opacity-100 transition-opacity`}
      />
    </div>
  );
};

export default AgentCard;
