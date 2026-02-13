import ReactMarkdown from "react-markdown";

interface MarkdownViewerProps {
  content: string;
  className?: string;
}

const MarkdownViewer = ({ content, className = "" }: MarkdownViewerProps) => (
  <div className={`prose prose-sm dark:prose-invert max-w-none prose-headings:text-foreground prose-p:text-foreground prose-li:text-foreground prose-strong:text-foreground ${className}`}>
    <ReactMarkdown>{content}</ReactMarkdown>
  </div>
);

export default MarkdownViewer;
