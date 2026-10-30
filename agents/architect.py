"""Arquitecto: diagnóstico y plan del repositorio, en una sola llamada."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block


INSTRUCTIONS = (
    "Eres el arquitecto de software del equipo. Tu única tarea es VALIDAR, no diseñar ni implementar.\n"
    "Valida que el plan y el repositorio cumplan este diseño (wallet-onboarding):\n"
    "- Stack: frontend Angular 22 + CopilotKit en frontend/; backend Python 3.13 + FastAPI + LangGraph en backend/.\n"
    "- Backend hexagonal: domain/ (reglas y máquina de estados), application/ (casos de uso), ports/ (WalletGateway), adapters/ (entrada: endpoint del agente; salida: cliente httpx). El dominio no importa FastAPI, LangGraph ni httpx.\n"
    "- Onboarding como máquina de estados por pasos (datos personales, DNI, monto máximo, activación); un paso solo avanza si pasa su validación; paso fallido vuelve al mismo nodo.\n"
    "- El frontend nunca llama a la API externa; todo pasa por el backend. La URL base de la API se lee de variable de entorno.\n"
    "- Sesión en el servidor: MemorySaver con thread_id (UUID v4) y TTL configurable (5 min por defecto) comprobado al entrar a cada nodo; thread_id no encontrado = sesión expirada. El frontend guarda thread_id en sessionStorage.\n"
    "- Fuera de alcance: cobros, proveedores de pago, movimiento de dinero, verificación de identidad externa (RENIEC).\n"
    "Reporta cada punto como CUMPLE, NO CUMPLE o NO VERIFICABLE, con evidencia del Issue o del código. No propongas código ni rediseños; si algo falta, indícalo como incumplimiento.\n"
    "Contrato de la API externa desconocido: márcalo como pendiente, no lo inventes.\n"
)


def architect_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta el alcance del issue y la constitución.") + "\nRepositorio: " + state['repo_name']
            + "\nTipo: " + state.get('project_type','ambos')
            + "\nCódigo original:\n" + _ctx(state['snapshot'],10000)
            + "\nDevuelve las secciones ## Analysis y ## Plan, cada una en su propia línea.")
    report = invoke(prompt)
    analysis, separator, plan = report.partition("\n## Plan\n")
    if not analysis.startswith("## Analysis\n") or not separator or not plan.strip():
        raise ValueError(
            "El arquitecto debe devolver las secciones ## Analysis y ## Plan."
        )
    return {
        "out_architect": report,
        "out_analysis": analysis.removeprefix("## Analysis\n").strip(),
        "out_plan": plan.strip(),
    }
