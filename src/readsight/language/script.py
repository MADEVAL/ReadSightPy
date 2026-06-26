from __future__ import annotations

from enum import Enum


class Script(str, Enum):
    Latin = "Latin"
    Cyrillic = "Cyrillic"
    Arabic = "Arabic"
    Hebrew = "Hebrew"
    Devanagari = "Devanagari"
    Bengali = "Bengali"
    Greek = "Greek"
    Armenian = "Armenian"
    Georgian = "Georgian"
    Thai = "Thai"
    Tamil = "Tamil"
    Telugu = "Telugu"
    Kannada = "Kannada"
    Malayalam = "Malayalam"
    Gujarati = "Gujarati"
    Gurmukhi = "Gurmukhi"
    Odia = "Odia"
    Ethiopic = "Ethiopic"
    Coptic = "Coptic"
    CJK = "CJK"
    Other = "Other"
