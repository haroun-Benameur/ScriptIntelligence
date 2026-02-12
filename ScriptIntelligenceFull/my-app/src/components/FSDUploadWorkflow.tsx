import { useState, useCallback } from "react";
import { Upload, FileCode, RefreshCw, Download, Loader2, AlertTriangle, CheckCircle } from "lucide-react";
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
import { toast } from "sonner";
import { api, type TestCase, type AnalyzeResponse } from "@/lib/api";

type ReportType = "test" | "drift" | null;

export default function FSDUploadWorkflow() {
  const [file, setFile] = useState<File | null>(null);
  const [uploaded, setUploaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [analyzeResult, setAnalyzeResult] = useState<AnalyzeResponse | null>(null);
  const [showRegenerateDialog, setShowRegenerateDialog] = useState(false);
  const [tests, setTests] = useState<TestCase[]>([]);
  const [reportTest, setReportTest] = useState<string | null>(null);
  const [reportDrift, setReportDrift] = useState<string | null>(null);
  const [reportTestFilename, setReportTestFilename] = useState<string | null>(null);
  const [reportDriftFilename, setReportDriftFilename] = useState<string | null>(null);
  const [activeReport, setActiveReport] = useState<ReportType>(null);

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
    setReportTestFilename(null);
    setReportDriftFilename(null);
    setActiveReport(null);
  };

  const handleUpload = useCallback(async () => {
    if (!file) return;
    setLoading(true);
    try {
      await api.uploadFsd(file);
      setUploaded(true);
      toast.success(`Fichier ${file.name} uploadé`);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Erreur lors de l'upload";
      if (msg.includes("abort") || msg.includes("timeout")) {
        toast.error("Connexion au backend expirée. Vérifiez que le backend tourne sur http://127.0.0.1:8000");
      } else {
        toast.error(msg);
      }
      return;
    } finally {
      setLoading(false);
    }

    // Analyser le FSD après upload réussi
    setLoading(true);
    try {
      const result = await api.analyzeFsd();
      setAnalyzeResult(result);
      if (result.drift_detected) {
        setShowRegenerateDialog(true);
      } else {
        toast.info("Aucun changement détecté dans le FSD");
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Erreur lors de l'analyse");
    } finally {
      setLoading(false);
    }
  }, [file]);

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
      setActiveReport(result.reports.drift_report ? "drift" : "test");
      toast.success(`${result.generated_tests_count} tests régénérés`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Erreur lors de la régénération");
    } finally {
      setLoading(false);
    }
  }, []);

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
        setActiveReport("test");
      }
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

  const changes = analyzeResult?.changes;
  const hasChanges = analyzeResult?.drift_detected && changes;
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

      {/* Drift Dialog */}
      <AlertDialog open={showRegenerateDialog} onOpenChange={setShowRegenerateDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-warning" />
              Changements détectés dans le FSD
            </AlertDialogTitle>
            <AlertDialogDescription asChild>
              <div className="space-y-2 text-sm">
                <p>Le fichier FSD a été modifié. Souhaitez-vous régénérer les test cases ?</p>
                <ul className="list-disc list-inside text-muted-foreground">
                  {addedCount > 0 && <li>Exigences ajoutées : {addedCount}</li>}
                  {updatedCount > 0 && <li>Exigences modifiées : {updatedCount}</li>}
                  {removedCount > 0 && <li>Exigences supprimées : {removedCount}</li>}
                </ul>
              </div>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Annuler</AlertDialogCancel>
            <AlertDialogAction onClick={handleRegenerate} disabled={loading}>
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
              Régénérer les tests
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Report & Tests */}
      {(reportTest || reportDrift || tests.length > 0) && (
        <Card>
          <CardHeader>
            <CardTitle>Rapport et tests générés</CardTitle>
            <CardDescription>
              Visualisez le rapport et téléchargez les fichiers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={activeReport ?? "test"} onValueChange={(v) => setActiveReport(v as ReportType)}>
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="test" disabled={!reportTest}>
                  Rapport de génération
                </TabsTrigger>
                <TabsTrigger value="drift" disabled={!reportDrift}>
                  Rapport de drift
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
                      <pre className="text-xs whitespace-pre-wrap font-mono">{reportTest}</pre>
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
                      <pre className="text-xs whitespace-pre-wrap font-mono">{reportDrift}</pre>
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
