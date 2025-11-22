from groq import Groq
from config import settings
import json


class GroqService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
    
    async def analyze_syllabus(self, pdf_text: str, student_name: str) -> str:
        """Analisa ementa usando Groq API"""
        prompt = f"""
Você é um assistente educacional especializado em análise de ementas acadêmicas.

Analise detalhadamente a ementa do aluno {student_name} fornecida abaixo e forneça:

1. Resumo da ementa
2. Principais tópicos e conteúdos abordados
3. Objetivos de aprendizado identificados
4. Sugestões ou observações relevantes

Ementa do aluno {student_name}:
{pdf_text}

Forneça uma análise completa, estruturada e profissional.
"""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente educacional especializado em análise de ementas acadêmicas. Forneça análises detalhadas, estruturadas e profissionais."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis = chat_completion.choices[0].message.content
            return analysis.strip()
        
        except Exception as e:
            raise Exception(f"Erro ao analisar ementa com Groq: {str(e)}")


groq_service = GroqService()

