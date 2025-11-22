from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from models import AnalysisResponse, AnalysisListResponse, UserResponse
from services.analysis_service import create_analysis, get_analyses, get_analysis_by_id
from middleware import get_current_user
from typing import List


router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/upload", response_model=AnalysisResponse)
async def upload_syllabus(
    student_name: str = Form(...),
    pdf_file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user)
):
    """Endpoint para upload e análise de ementa"""
    # Valida se é PDF
    if not pdf_file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos PDF são aceitos"
        )
    
    # Lê arquivo
    file_content = await pdf_file.read()
    
    if len(file_content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo vazio"
        )
    
    # Cria análise
    try:
        analysis = await create_analysis(
            student_name=student_name,
            pdf_file=file_content,
            user_id=current_user.id
        )
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar análise: {str(e)}"
        )


@router.get("/", response_model=List[AnalysisListResponse])
async def list_analyses(current_user: UserResponse = Depends(get_current_user)):
    """Endpoint para listar todas as análises do usuário"""
    try:
        analyses = await get_analyses(current_user.id)
        return analyses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar análises: {str(e)}"
        )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Endpoint para buscar análise específica"""
    try:
        analysis = await get_analysis_by_id(analysis_id, current_user.id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Análise não encontrada"
            )
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar análise: {str(e)}"
        )

