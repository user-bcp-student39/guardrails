"""Ingeniero de pruebas: edita aquí las instrucciones de revisión."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block


INSTRUCTIONS = (
    "Eres el Ingeniero de pruebas del equipo. Tu única tarea es VALIDAR la cobertura de pruebas; no escribas pruebas nuevas.\n"
    "Verifica que existan pruebas (backend con pytest) para: avance de paso solo si valida y retorno al mismo paso si falla; "
    "monto máximo en (0, 500] PEN incluidos los límites 0, 500 y 500.01; expiración por TTL y thread_id desconocido tratado como sesión expirada; "
    "activación de la wallet solo al completar el onboarding; dominio probado sin FastAPI/LangGraph/httpx; adaptador WalletGateway con respuestas simuladas.\n"
    "Reporta cada punto como CUBIERTO, NO CUBIERTO o NO EJECUTADO con evidencia; no afirmes resultados que no se ejecutaron.\n"
    "Cierra con la sección '## Observaciones' con una lista numerada de hallazgos accionables de tu rol (o 'Sin observaciones').\n"
)


def testing_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + "\nBackend:\n" + _ctx(state.get("out_backend", ""),6000) + "\nFrontend:\n" + _ctx(state.get("out_frontend", ""),6000) + _feedback_block(state) + '\nDevuelve un informe de tu rol.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
    return {"out_testing": invoke(prompt)}
