# main.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any

from agents.orchestrator import (
    run_workflow,
    generate_tests_initial,
    analyze_fsd_workflow,
    regenerate_tests_workflow,
    get_spec_coverage,
    upload_fsd_workflow,
    list_tests_workflow,
    get_tests_for_requirement_workflow,
    delete_tests_for_requirement_workflow,
)

app = FastAPI()

# CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegenerateRequest(BaseModel):
    confirm: bool


class TestCase(BaseModel):
    requirement_id: str
    test_name: str
    description: str
    inputs: Dict[str, Any]
    expected_output: str


@app.get("/run-workflow")
def run_workflow_endpoint():
    """
    Lit le FSD, détecte le drift, régénère uniquement les tests
    des exigences ajoutées/modifiées, génère les rapports MD.
    """
    return run_workflow()


@app.post("/upload-fsd")
async def upload_fsd(file: UploadFile = File(...)):
    """
    Upload un fichier FSD (.md). Le contenu est sauvegardé et utilisé pour analyse/génération.
    """
    if not file.filename or not file.filename.lower().endswith(".md"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .md sont acceptés.")
    content = (await file.read()).decode("utf-8", errors="replace")
    result = upload_fsd_workflow(content)
    return {"status": "uploaded", "filename": file.filename}


@app.post("/generate-tests")
def generate_tests_endpoint():
    """
    Génération initiale : lit le FSD uploadé, extrait toutes les exigences, génère les tests,
    exécute pytest et produit un rapport d'exécution MD.
    """
    try:
        return generate_tests_initial()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/reports/{filename:path}")
def get_report(filename: str):
    """Récupère le contenu d'un rapport pour affichage ou téléchargement."""
    import os
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    safe_name = os.path.basename(filename)
    path = os.path.normpath(os.path.join(reports_dir, safe_name))
    if not os.path.abspath(path).startswith(os.path.abspath(reports_dir)):
        raise HTTPException(status_code=403, detail="Accès refusé")
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    return FileResponse(path, filename=safe_name)


@app.get("/analyze-fsd")
def analyze_fsd_endpoint():
    """
    Lit le FSD, détecte le drift et stocke l'état pending.
    """
    return analyze_fsd_workflow()


@app.post("/regenerate-tests")
def regenerate_tests_endpoint(request: RegenerateRequest):
    """
    Régénère UNIQUEMENT les tests pour les exigences ajoutées/modifiées
    détectées lors du dernier /analyze-fsd. Génère les rapports MD.
    """
    if not request.confirm:
        return {"status": "cancelled", "message": "Regeneration not confirmed."}

    try:
        return regenerate_tests_workflow()
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@app.get("/spec-coverage")
def get_spec_coverage_endpoint():
    """
    Retourne le Spec Coverage: scénarios (exigences FSD), couverture par tests, et qualité.
    Utilisé par le frontend pour afficher Spec Coverage et Quality Gate.
    """
    return get_spec_coverage()


@app.get("/tests", response_model=List[TestCase])
def list_tests_endpoint():
    return list_tests_workflow()


@app.get("/tests/{requirement_id}", response_model=List[TestCase])
def get_tests_for_requirement_endpoint(requirement_id: str):
    tests = get_tests_for_requirement_workflow(requirement_id)
    if not tests:
        raise HTTPException(
            status_code=404, detail="No tests found for this requirement_id."
        )
    return tests


@app.delete("/tests/{requirement_id}")
def delete_tests_for_requirement_endpoint(requirement_id: str):
    result = delete_tests_for_requirement_workflow(requirement_id)
    if result["deleted_count"] == 0:
        raise HTTPException(
            status_code=404, detail="No tests found for this requirement_id."
        )
    return {
        "status": "deleted",
        "requirement_id": requirement_id,
        "deleted_count": result["deleted_count"],
    }
