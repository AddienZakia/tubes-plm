from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    # Primary
    primary_main: str    = "#2563EB"
    primary_hover: str   = "#1D4ED8"
    primary_active: str  = "#1E40AF"

    # Neutral
    neutral_white: str   = "#FFFFFF"
    neutral_10: str      = "#F8FAFC"
    neutral_20: str      = "#F1F5F9"
    neutral_30: str      = "#E2E8F0"
    neutral_40: str      = "#CBD5E1"
    neutral_50: str      = "#94A3B8"
    neutral_60: str      = "#64748B"
    neutral_70: str      = "#475569"
    neutral_80: str      = "#334155"
    neutral_90: str      = "#1E293B"
    neutral_black: str   = "#0F172A"

    # Success
    success_main: str    = "#16A34A"
    success_hover: str   = "#15803D"
    success_active: str  = "#166534"

    # Warning
    warning_main: str    = "#D97706"
    warning_hover: str   = "#B45309"
    warning_active: str  = "#92400E"

    # Error
    error_main: str      = "#DC2626"
    error_hover: str     = "#B91C1C"
    error_active: str    = "#991B1B"

    # Info
    info_main: str       = "#0284C7"
    info_hover: str      = "#0369A1"
    info_active: str     = "#075985"


Colors = ColorPalette()