"""Pydantic models for function calling."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ParameterDefinition(BaseModel):
    """Definition of a single parameter."""

    type: str


class FunctionDefinition(BaseModel):
    """Definition of a function."""

    name: str
    description: str
    parameters: Dict[str, ParameterDefinition] = Field(default_factory=dict)
    returns: Optional[ParameterDefinition] = None


class TestPrompt(BaseModel):
    """A single test prompt."""

    prompt: str


class FunctionCallResult(BaseModel):
    """Result of a function call."""

    prompt: str
    name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
