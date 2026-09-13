from pydantic import BaseModel, Field, model_validator
from typing import Optional
from uuid import UUID

class FinancialProfileUpdate(BaseModel):
    needs_pct: float = Field(..., ge=0.0, le=1.0)
    wants_pct: float = Field(..., ge=0.0, le=1.0)
    savings_pct: float = Field(..., ge=0.0, le=1.0)

    @model_validator(mode='after')
    def check_percentages_sum(self) -> 'FinancialProfileUpdate':
        total = sum([self.needs_pct, self.wants_pct, self.savings_pct])
        # Usamos round a 4 decimales para evitar problemas de precisión en punto flotante
        if round(total, 4) != 1.0000:
            raise ValueError(f"Los porcentajes deben sumar exactamente 1.0 (100%). Suma actual: {total}")
        return self