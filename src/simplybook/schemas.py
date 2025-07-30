"""
Schemas para las funciones públicas del MCP Server
"""

# Schemas para Bookings
BOOKING_LIST_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {
            "type": "integer",
            "description": "Número de página para paginación",
            "minimum": 1
        },
        "on_page": {
            "type": "integer",
            "description": "Elementos por página",
            "minimum": 1
        },
        "upcoming_only": {
            "type": "boolean",
            "description": "Solo reservas futuras"
        },
        "status": {
            "type": "string",
            "description": "Estado de la reserva",
            "enum": ["confirmed", "confirmed_pending", "pending", "canceled"]
        },
        "services": {
            "type": "array",
            "description": "Lista de IDs de servicios para filtrar",
            "items": {
                "type": "string"
            }
        },
        "providers": {
            "type": "array",
            "description": "Lista de IDs de proveedores para filtrar",
            "items": {
                "type": "string"
            }
        },
        "client_id": {
            "type": "string",
            "description": "ID del cliente para filtrar"
        },
        "date": {
            "type": "string",
            "description": "Fecha para filtrar (YYYY-MM-DD)",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "search": {
            "type": "string",
            "description": "String de búsqueda (por código, datos del cliente)"
        },
        "additional_fields": {
            "type": "object",
            "description": "Campos adicionales para filtrar",
            "additionalProperties": {
                "type": "string"
            }
        }
    }
}

BOOKING_CREATE_SCHEMA = {
    "type": "object",
    "required": ["booking_data"],
    "properties": {
        "booking_data": {
            "type": "object",
            "required": ["service_id", "start_datetime"],
            "properties": {
                "service_id": {
                    "type": "string",
                    "description": "ID del servicio"
                },
                "start_datetime": {
                    "type": "string",
                    "description": "Fecha y hora de inicio (YYYY-MM-DD HH:mm:ss)",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$"
                },
                "client_id": {
                    "type": "string",
                    "description": "ID del cliente"
                },
                "provider_id": {
                    "type": "string",
                    "description": "ID del proveedor"
                },
                "notes": {
                    "type": "string",
                    "description": "Notas adicionales"
                }
            }
        }
    }
}

BOOKING_EDIT_SCHEMA = {
    "type": "object",
    "required": ["booking_id", "booking_data"],
    "properties": {
        "booking_id": {
            "type": "string",
            "description": "ID de la reserva a editar"
        },
        "booking_data": {
            "type": "object",
            "properties": {
                "service_id": {
                    "type": "string",
                    "description": "ID del servicio"
                },
                "start_datetime": {
                    "type": "string",
                    "description": "Fecha y hora de inicio (YYYY-MM-DD HH:mm:ss)",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$"
                },
                "provider_id": {
                    "type": "string",
                    "description": "ID del proveedor"
                },
                "notes": {
                    "type": "string",
                    "description": "Notas adicionales"
                }
            }
        }
    }
}

BOOKING_DETAILS_SCHEMA = {
    "type": "object",
    "required": ["booking_id"],
    "properties": {
        "booking_id": {
            "type": "string",
            "description": "ID de la reserva"
        }
    }
}

BOOKING_CANCEL_SCHEMA = {
    "type": "object",
    "required": ["booking_id"],
    "properties": {
        "booking_id": {
            "type": "string",
            "description": "ID de la reserva a cancelar"
        }
    }
}

BOOKING_APPROVE_SCHEMA = {
    "type": "object",
    "required": ["booking_id"],
    "properties": {
        "booking_id": {
            "type": "string",
            "description": "ID de la reserva a aprobar"
        }
    }
}

AVAILABLE_SLOTS_SCHEMA = {
    "type": "object",
    "required": ["service_id", "date"],
    "properties": {
        "service_id": {
            "type": "string",
            "description": "ID del servicio"
        },
        "date": {
            "type": "string",
            "description": "Fecha para buscar slots (YYYY-MM-DD)",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        }
    }
}

CALENDAR_DATA_SCHEMA = {
    "type": "object",
    "required": ["start_date", "end_date"],
    "properties": {
        "start_date": {
            "type": "string",
            "description": "Fecha de inicio (YYYY-MM-DD)",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "end_date": {
            "type": "string",
            "description": "Fecha de fin (YYYY-MM-DD)",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        }
    }
}

# Schemas para Services
SERVICES_LIST_SCHEMA = {
    "type": "object",
    "properties": {}  # No requiere parámetros
}

SERVICE_DETAILS_SCHEMA = {
    "type": "object",
    "required": ["service_id"],
    "properties": {
        "service_id": {
            "type": "string",
            "description": "ID del servicio"
        }
    }
}

# Schemas para Providers
PROVIDERS_LIST_SCHEMA = {
    "type": "object",
    "properties": {}  # No requiere parámetros
}

PROVIDER_DETAILS_SCHEMA = {
    "type": "object",
    "required": ["provider_id"],
    "properties": {
        "provider_id": {
            "type": "string",
            "description": "ID del proveedor"
        }
    }
}

# Schemas para Clients
CLIENTS_LIST_SCHEMA = {
    "type": "object",
    "properties": {
        "search": {
            "type": "string",
            "description": "Texto para buscar clientes"
        },
        "page": {
            "type": "integer",
            "description": "Número de página",
            "minimum": 1
        },
        "on_page": {
            "type": "integer",
            "description": "Elementos por página",
            "minimum": 1
        }
    }
} 