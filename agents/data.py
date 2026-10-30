"""Datos y persistencia: perfil opcional para el equipo de siete."""
from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block

INSTRUCTIONS = (
    "Eres el responsable de Datos y persistencia. Tu única tarea es VALIDAR; no definas tablas ni migraciones nuevas.\n"
    "Valida contra este diseño: no hay datos previos ni migración; el estado de sesión vive en MemorySaver de LangGraph (en memoria, se pierde al reiniciar; un thread_id no encontrado equivale a sesión expirada); "
    "el frontend solo guarda thread_id en sessionStorage (no localStorage); el avance lleva marca de tiempo y TTL de configuración; "
    "el monto máximo se guarda en (0, 500] PEN; un checkpointer persistente está fuera de alcance.\n"
    "Reporta cada punto como CUMPLE, NO CUMPLE o NO VERIFICABLE con evidencia, sin generar SQL.\n"
)


def data_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS
              + _const_block(state, "Conserva los datos existentes y respeta el alcance del Issue.")
              + "\nRepositorio: " + state["repo_name"]
              + "\nPlan aprobado:\n" + _ctx(state.get("out_plan", ""), 2500)
              + "\nEsquema y código existentes:\n" + _ctx(state.get("snapshot", ""), 6000)
              + _feedback_block(state)
              + "\nDevuelve solo un informe de validación; no incluyas SQL, código ni archivos. "
                "No ejecutes migraciones ni inventes evidencia. Marca NO EJECUTADO lo no comprobado.")
    return {"out_data": invoke(prompt)}
