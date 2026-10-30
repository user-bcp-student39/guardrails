"""Rol frontend: edita aquí sus instrucciones y entregables."""

from graph.state import WorkflowState
from graph.context import _ctx, _runs, _const_block, _ronda, _feedback_block


INSTRUCTIONS = (
    "Eres un desarrollador frontend/API senior. Tu única tarea es VALIDAR el frontend; no generes ni modifiques código.\n"
    "Valida contra este diseño: Angular 22 con componentes standalone, signals, ChangeDetectionStrategy.OnPush, formularios reactivos con validadores y rutas con carga diferida; "
    "interfaz conversacional con CopilotKit que muestra el paso actual y los pasos restantes; mensaje de corrección inmediato ante validación fallida; "
    "thread_id (UUID v4) generado en el frontend, enviado en cada invocación y guardado en sessionStorage (no localStorage); "
    "el frontend nunca llama a la API externa, solo al endpoint del backend; aviso claro de expiración y reinicio explícito.\n"
    "Reporta cada punto como CUMPLE, NO CUMPLE o NO VERIFICABLE con evidencia.\n"
)


def frontend_node(state: WorkflowState, invoke) -> dict:
    """
    Implementa los cambios de frontend/API del plan.
    Mismo tratamiento del feedback que el backend.
    Se salta si project_type no incluye frontend.
    Escribe en: out_frontend
    """
    if not _runs(state, "frontend"):
        print("[frontend_node] project_type no incluye frontend — saltando.")
        return {}

    print(f"[frontend_node] Refactorizando frontend/API (ronda {_ronda(state)})...")

    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + _feedback_block(state) + '\nDevuelve solo un informe de validación; no incluyas código ni archivos.')
    return {"out_frontend": invoke(prompt)}
