from datetime import datetime
from fastapi import HTTPException, status
from database import db
from models import AnalysisCreate, AnalysisResponse, AnalysisListResponse
from services.groq_service import groq_service
from services.pdf_service import extract_text_from_pdf
from typing import List, Optional


async def create_analysis(
    student_name: str,
    pdf_file: bytes,
    user_id: str
) -> AnalysisResponse:
    """Cria nova análise de ementa"""
    client = db.get_client()
    
    # Verifica se já existe análise para este aluno
    existing = client.table("analyses").select("*").eq(
        "student_name", student_name
    ).eq("user_id", user_id).execute()
    
    if existing.data:
        # Retorna análise existente
        analysis = existing.data[0]
        return AnalysisResponse(
            id=analysis["id"],
            student_name=analysis["student_name"],
            analysis_detail=analysis["analysis_detail"],
            created_at=datetime.fromisoformat(analysis["created_at"].replace("Z", "+00:00")),
            user_id=analysis["user_id"]
        )
    
    # Extrai texto do PDF
    pdf_text = await extract_text_from_pdf(pdf_file)
    
    if not pdf_text or len(pdf_text.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível extrair texto do PDF. Verifique se o arquivo está correto."
        )
    
    # Analisa com Groq
    analysis_detail = await groq_service.analyze_syllabus(pdf_text, student_name)
    
    # Salva análise no banco
    analysis_record = {
        "student_name": student_name,
        "analysis_detail": analysis_detail,
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat()
    }
    
    result = client.table("analyses").insert(analysis_record).execute()
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao salvar análise"
        )
    
    analysis = result.data[0]
    return AnalysisResponse(
        id=analysis["id"],
        student_name=analysis["student_name"],
        analysis_detail=analysis["analysis_detail"],
        created_at=datetime.fromisoformat(analysis["created_at"].replace("Z", "+00:00")),
        user_id=analysis["user_id"]
    )


async def get_analyses(user_id: str) -> List[AnalysisListResponse]:
    """Busca todas as análises do usuário"""
    client = db.get_client()
    
    result = client.table("analyses").select("*").eq(
        "user_id", user_id
    ).order("created_at", desc=True).execute()
    
    analyses = []
    for item in result.data:
        analyses.append(AnalysisListResponse(
            id=item["id"],
            student_name=item["student_name"],
            analysis_detail=item["analysis_detail"],
            created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
        ))
    
    return analyses


async def get_analysis_by_id(analysis_id: str, user_id: str) -> Optional[AnalysisResponse]:
    """Busca análise específica por ID"""
    client = db.get_client()
    
    result = client.table("analyses").select("*").eq(
        "id", analysis_id
    ).eq("user_id", user_id).execute()
    
    if not result.data:
        return None
    
    item = result.data[0]
    return AnalysisResponse(
        id=item["id"],
        student_name=item["student_name"],
        analysis_detail=item["analysis_detail"],
        created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
        user_id=item["user_id"]
    )

