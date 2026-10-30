"""Revisor de seguridad: edita aquí las instrucciones de revisión."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block


INSTRUCTIONS = (
    "Eres el Revisor de seguridad del equipo. Tu única tarea es VALIDAR; no corrijas código.\n"
    "Valida contra este diseño: el servidor revalida cada paso antes de persistirlo (una petición manipulada no puede saltarse reglas); "
    "la expiración de sesión se aplica en el servidor, no solo en el cliente; thread_id es UUID v4 y la sesión termina con la pestaña (sessionStorage); "
    "el frontend no accede a la API externa; URL y TTL salen de configuración/variables de entorno, sin valores ni secretos hardcodeados; "
    "el monto máximo no supera 500 PEN; el formato del DNI no se presenta como verificación de identidad.\n"
    "Reporta cada punto como CUMPLE, NO CUMPLE o NO VERIFICABLE con evidencia y severidad.\n"
)


def security_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + "\nBackend:\n" + _ctx(state.get("out_backend", ""),6000) + "\nFrontend:\n" + _ctx(state.get("out_frontend", ""),6000) + _feedback_block(state) + '\nDevuelve un informe de tu rol.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
    return {"out_security": invoke(prompt)}
