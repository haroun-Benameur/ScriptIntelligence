import { useState, useCallback } from "react";
import { Upload, FileCode, RefreshCw, Download, Loader2, CheckCircle, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { api, type TestCase, type AnalyzeResponse } from "@/lib/api";
import MarkdownViewer from "@/components/MarkdownViewer";

type ReportType = "test" | "drift" | "pytest" | null;

export default function FSDUploadWorkflow() {
  const queryClient = useQueryClient();
  const [file, setFile] = useState<File | null>(null);
  const [uploaded, setUploaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [analyzeResult, setAnalyzeResult] = useState<AnalyzeResponse | null>(null);
  const [tests, setTests] = useState<TestCase[]>([]);
  const [reportTest, setReportTest] = useState<string | null>(null);
  const [reportDrift, setReportDrift] = useState<string | null>(null);
  const [reportPytest, setReportPytest] = useState<string | null>(null);
  const [reportTestFilename, setReportTestFilename] = useState<string | null>(null);
  const [reportDriftFilename, setReportDriftFilename] = useState<string | null>(null);
  const [reportPytestFilename, setReportPytestFilename] = useState<string | null>(null);
  const [activeReport, setActiveReport] = useState<ReportType | "pytest">(null);
  const [showRegenerateDialog, setShowRegenerateDialog] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    if (!f.name.toLowerCase().endsWith(".md")) {
      toast.error("Seuls les fichiers .md sont acceptés");
      return;
    }
    setFile(f);
    setUploaded(false);
    setAnalyzeResult(null);
    setReportTest(null);
    setReportDrift(null);
    setReportPytest(null);
    setReportTestFilename(null);
    setReportDriftFilename(null);
    setReportPytestFilename(null);
    setActiveReport(null);
  };

  const handleRegenerate = useCallback(async () => {
    setShowRegenerateDialog(false);
    setLoading(true);
    try {
      const result = await api.regenerateTests();
      const allTests = await api.listTests();
      setTests(allTests);
      if (result.reports.test_generation_report) {
        setReportTestFilename(result.reports.test_generation_report);
        const txt = await api.fetchReportText(result.reports.test_generation_report);
        setReportTest(txt);
      }
      if (result.reports.drift_report) {
        setReportDriftFilename(result.reports.drift_report);
        const txt = await api.fetchReportText(result.reports.drift_report);
        setReportDrift(txt);
      }
      if (result.reports.pytest_execution_report) {
        setReportPytestFilename(result.reports.pytest_execution_report);
        const txt = await api.fetchReportText(result.reports.pytest_execution_report);
        setReportPytest(txt);
      }
      setActiveReport(result.reports.pytest_execution_report ? "pytest" : (result.reports.drift_report ? "drift" : "test"));
      queryClient.invalidateQueries({ queryKey: ["spec-coverage"] });
      toast.success(`${result.generated_tests_count} tests régénérés (modifications uniquement), pytest exécuté`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Erreur lors de la régénération");
    } finally {
      setLoading(false);
    }
  }, [queryClient]);

  const handleUpload = useCallback(async () => {
    if (!file) return;
    setLoading(true);
    try {
      await api.uploadFsd(file);
      setUploaded(true);
      toast.success(`Fichier ${file.name} uploadé`);
      const result = await api.analyzeFsd();
      setAnalyzeResult(result);
      if (result.drift_detected) {
        setShowRegenerateDialog(true);
      } else {
        const hasTests = (await api.listTests()).length > 0;
        if (hasTests) {
          toast.info("Aucun changement détecté. Les rapports et tests restent affichés.");
          const allTests = await api.listTests();
          setTests(allTests);
        } else {
          toast.info("Fichier prêt. Cliquez sur « Générer les tests » pour créer les test cases.");
        }
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Erreur";
      if (msg.includes("abort") || msg.includes("timeout")) {
        toast.error("Connexion au backend expirée. Vérifiez que le backend tourne sur http://127.0.0.1:8000");
      } else {
        toast.error(msg);
      }
    } finally {
      setLoading(false);
    }
  }, [file]);


  const handleGenerate = useCallback(async () => {
    setLoading(true);
    try {
      const result = await api.generateTests();
      setTests(result.generated_tests);
      if (result.reports.test_generation_report) {
        setReportTestFilename(result.reports.test_generation_report);
        const txt = await api.fetchReportText(result.reports.test_generation_report);
        setReportTest(txt);
        setReportDrift(null);
        setReportDriftFilename(null);
      }
      if (result.reports.pytest_execution_report) {
        setReportPytestFilename(result.reports.pytest_execution_report);
        const txt = await api.fetchReportText(result.reports.pytest_execution_report);
        setReportPytest(txt);
        setActiveReport("pytest");
      } else {
        setActiveReport("test");
      }
      queryClient.invalidateQueries({ queryKey: ["spec-coverage"] });
      toast.success(`${result.generated_tests_count} tests générés`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Erreur lors de la génération");
    } finally {
      setLoading(false);
    }
  }, []);

  const handleDownloadReport = (filename: string) => {
    const a = document.createElement("a");
    a.href = api.getReportUrl(filename);
    a.download = filename;
    a.click();
  };

  const hasChanges = analyzeResult?.drift_detected ?? false;
  const changes = analyzeResult?.changes;
  const addedCount = changes?.added?.length ?? 0;
  const updatedCount = changes?.updated?.length ?? 0;
  const removedCount = changes?.removed?.length ?? 0;

  return (
    <div className="space-y-6">
      {/* Upload FSD */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileCode className="h-5 w-5 text-primary" />
            Fichier FSD
          </CardTitle>
          <CardDescription>
            Uploadez votre fichier FSD (.md) puis générez les test cases. Format attendu : ## REQ-XXX: Titre
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-4 items-start">
            <label className="flex-1 cursor-pointer">
              <div className="rounded-lg border border-dashed border-border bg-muted/30 p-6 text-center hover:bg-muted/50 transition-colors">
                <Upload className="h-8 w-8 mx-auto text-muted-foreground mb-2" />
                <p className="text-sm text-muted-foreground">
                  {file ? file.name : "Cliquez pour sélectionner un fichier .md"}
                </p>
              </div>
              <input
                type="file"
                accept=".md"
                className="hidden"
                onChange={handleFileChange}
              />
            </label>
            <Button
              onClick={handleUpload}
              disabled={!file || loading}
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Upload className="h-4 w-4" />}
              {loading ? "En cours..." : "Uploader"}
            </Button>
          </div>

          {uploaded && !hasChanges && (
            <div className="flex items-center gap-2 p-4 rounded-lg bg-muted/50">
              <CheckCircle className="h-4 w-4 text-success shrink-0" />
              <span className="text-sm">Fichier uploadé. Aucun changement détecté.</span>
            </div>
          )}

          {uploaded && (
            <div className="flex gap-2">
              <Button onClick={handleGenerate} disabled={loading} variant="outline">
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
                Générer les tests
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Dialog : demander à l'utilisateur de régénérer les tests (modifications uniquement) */}
      <AlertDialog open={showRegenerateDialog} onOpenChange={setShowRegenerateDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-warning" />
              Changements détectés dans le FSD
            </AlertDialogTitle>
            <AlertDialogDescription asChild>
              <div className="space-y-2 text-sm">
                <p>Le fichier FSD a été modifié. Voulez-vous régénérer uniquement les tests concernant les modifications ?</p>
                <ul className="list-disc list-inside text-muted-foreground">
                  {addedCount > 0 && <li>Exigences ajoutées : {addedCount}</li>}
                  {updatedCount > 0 && <li>Exigences modifiées : {updatedCount}</li>}
                  {removedCount > 0 && <li>Exigences supprimées : {removedCount}</li>}
                </ul>
              </div>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Non</AlertDialogCancel>
            <AlertDialogAction onClick={handleRegenerate} disabled={loading}>
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
              Oui, régénérer les tests
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Report & Tests */}
      {(reportTest || reportDrift || reportPytest || tests.length > 0) && (
        <Card>
          <CardHeader>
            <CardTitle>Rapport et tests générés</CardTitle>
            <CardDescription>
              Visualisez le rapport et téléchargez les fichiers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={activeReport ?? "test"} onValueChange={(v) => setActiveReport(v as ReportType)}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="test" disabled={!reportTest}>
                  Génération
                </TabsTrigger>
                <TabsTrigger value="drift" disabled={!reportDrift}>
                  Drift
                </TabsTrigger>
                <TabsTrigger value="pytest" disabled={!reportPytest}>
                  Pytest
                </TabsTrigger>
              </TabsList>
              <TabsContent value="test" className="mt-4">
                {reportTest && (
                  <>
                    {reportTestFilename && (
                      <div className="flex justify-end mb-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDownloadReport(reportTestFilename)}
                          asChild
                        >
                          <a href={api.getReportUrl(reportTestFilename)} download={reportTestFilename}>
                            <Download className="h-4 w-4 mr-2" />
                            Télécharger
                          </a>
                        </Button>
                      </div>
                    )}
                    <ScrollArea className="h-[400px] rounded-md border p-4">
                      <MarkdownViewer content={reportTest} className="text-sm" />
                    </ScrollArea>
                  </>
                )}
              </TabsContent>
              <TabsContent value="drift" className="mt-4">
                {reportDrift && (
                  <>
                    {reportDriftFilename && (
                      <div className="flex justify-end mb-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDownloadReport(reportDriftFilename)}
                          asChild
                        >
                          <a href={api.getReportUrl(reportDriftFilename)} download={reportDriftFilename}>
                            <Download className="h-4 w-4 mr-2" />
                            Télécharger
                          </a>
                        </Button>
                      </div>
                    )}
                    <ScrollArea className="h-[400px] rounded-md border p-4">
                      <MarkdownViewer content={reportDrift} className="text-sm" />
                    </ScrollArea>
                  </>
                )}
              </TabsContent>
              <TabsContent value="pytest" className="mt-4">
                {reportPytest && (
                  <>
                    {reportPytestFilename && (
                      <div className="flex justify-end mb-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDownloadReport(reportPytestFilename!)}
                          asChild
                        >
                          <a href={api.getReportUrl(reportPytestFilename!)} download={reportPytestFilename}>
                            <Download className="h-4 w-4 mr-2" />
                            Télécharger
                          </a>
                        </Button>
                      </div>
                    )}
                    <ScrollArea className="h-[400px] rounded-md border p-4">
                      <MarkdownViewer content={reportPytest} className="text-sm" />
                    </ScrollArea>
                  </>
                )}
              </TabsContent>
            </Tabs>

            {tests.length > 0 && (
              <div className="mt-6">
                <h4 className="text-sm font-semibold mb-3">Test cases ({tests.length})</h4>
                <ScrollArea className="h-[280px] rounded-md border">
                  <div className="p-4 space-y-4">
                    {tests.map((t, i) => (
                      <div key={i} className="rounded-lg border bg-muted/30 p-4 text-sm">
                        <p className="font-mono text-primary">{t.requirement_id}</p>
                        <p className="font-medium mt-1">{t.test_name}</p>
                        <p className="text-muted-foreground mt-1">{t.description}</p>
                        <p className="text-xs mt-2">
                          Inputs: <code>{JSON.stringify(t.inputs)}</code>
                        </p>
                        <p className="text-xs">
                          Attendu: {t.expected_output}
                        </p>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
