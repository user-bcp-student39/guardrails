"""Rol backend: edita aquí sus instrucciones y entregables."""

from graph.state import WorkflowState
from graph.context import _ctx, _runs, _const_block, _ronda, _feedback_block


INSTRUCTIONS = (
    "Eres un desarrollador backend senior. Tu única tarea es VALIDAR el backend; no generes ni modifiques código.\n"
    "Valida contra este diseño:\n"
    "- Validaciones bloqueantes por paso (datos personales, DNI, monto máximo, activación) también en el servidor, no solo en la interfaz.\n"
    "- Monto máximo en (0, 500] PEN; el tope 500 es una constante de negocio, no configurable por usuario.\n"
    "- Un paso con validación fallida vuelve al mismo nodo del grafo LangGraph mediante arista condicional.\n"
    "- Expiración de sesión en el servidor: TTL leído de configuración (5 min por defecto), comprobado al entrar en cada nodo; thread_id desconocido = sesión expirada y vuelta al paso 1.\n"
    "- Estado con MemorySaver y thread_id en config['configurable']['thread_id'].\n"
    "- Dominio sin imports de FastAPI, LangGraph ni httpx; acceso a la API externa solo vía el puerto WalletGateway; URL base por variable de entorno.\n"
    "- La wallet pasa a activa solo al completar el onboarding.\n"
    "Reporta cada punto como CUMPLE, NO CUMPLE o NO VERIFICABLE con evidencia (archivo y fragmento). No inventes endpoints de la API externa.\n"
)


def backend_node(state: WorkflowState, invoke) -> dict:
    """
    Implementa los cambios de backend del plan.
    En rondas > 1 incorpora las observaciones del chapter.
    Se salta si project_type no incluye backend.
    Escribe en: out_backend
    """
    if not _runs(state, "backend"):
        print("[backend_node] project_type no incluye backend — saltando.")
        return {}

    print(f"[backend_node] Refactorizando backend (ronda {_ronda(state)})...")

    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + _feedback_block(state) + '\nDevuelve solo un informe de validación; no incluyas código ni archivos.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
        prompt += "\nValida que el acceso a datos respete este contrato."
    return {"out_backend": invoke(prompt)}
