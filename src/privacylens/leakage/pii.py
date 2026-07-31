"""
PII Leakage Auditor.

Scans model predictions, text outputs, or feature values for sensitive
Personally Identifiable Information (PII) memorized or leaked by the model.

Supports detection of:
- Email addresses
- Social Security Numbers (SSN)
- Credit card numbers
- Phone numbers
- IP addresses
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

_EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
    re.IGNORECASE,
)
_SSN_PATTERN = re.compile(
    r"\b(?!000|666|9\d{2})\d{3}[- ](?!00)\d{2}[- ](?!0{4})\d{4}\b"
)
_CREDIT_CARD_PATTERN = re.compile(
    r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
)
_PHONE_PATTERN = re.compile(
    r"\b(?:(?:\+?1[\s\-.]?)?(?:\(\d{3}\)|\d{3})[\s\-.]?\d{3}[\s\-.]?\d{4})\b"
)
_IPV4_PATTERN = re.compile(
    r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
)

PATTERNS: Dict[str, re.Pattern[str]] = {
    "EMAIL": _EMAIL_PATTERN,
    "SSN": _SSN_PATTERN,
    "CREDIT_CARD": _CREDIT_CARD_PATTERN,
    "PHONE": _PHONE_PATTERN,
    "IP_ADDRESS": _IPV4_PATTERN,
}

_SEVERITY_WEIGHTS: Dict[str, float] = {
    "SSN": 1.0,
    "CREDIT_CARD": 0.9,
    "EMAIL": 0.6,
    "PHONE": 0.5,
    "IP_ADDRESS": 0.4,
}


class PIILeakageAuditor:
    """
    Audits model outputs and training/test dataset samples for PII leakage.

    Detects sensitive strings (emails, SSNs, credit cards, phone numbers, IPs)
    present in string features, prediction labels, or generated text outputs.
    """

    def __init__(self, target_patterns: Optional[List[str]] = None) -> None:
        """
        Args:
            target_patterns: Optional list of PII types to check (e.g. ['EMAIL', 'SSN']).
                            If None, all standard PII patterns are audited.
        """
        if target_patterns:
            self.patterns = {k: v for k, v in PATTERNS.items() if k in target_patterns}
        else:
            self.patterns = PATTERNS

    def run(
        self,
        model: Any,
        X_samples: np.ndarray,
        y_samples: Optional[np.ndarray] = None,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Execute the PII Leakage audit on sample data or model outputs.

        Args:
            model: Trained model object.
            X_samples: Feature array or text list to scan for PII.
            y_samples: Optional label array.

        Returns:
            Tuple of (pii_leakage_score, details_dict).
            - pii_leakage_score: 0.0 (no leakage) to 1.0 (severe PII leakage).
            - details_dict: Detailed breakdown per PII type.
        """
        sample_strings = self._extract_strings(X_samples, y_samples)

        if not sample_strings:
            return 0.0, {
                "pii_leakage_score": 0.0,
                "total_samples_scanned": 0,
                "matches_found": 0,
                "by_type": {},
            }

        matches_by_type: Dict[str, int] = {k: 0 for k in self.patterns}
        total_matches = 0

        for text in sample_strings:
            for pii_type, pattern in self.patterns.items():
                found = pattern.findall(text)
                if found:
                    matches_by_type[pii_type] += len(found)
                    total_matches += len(found)

        # Compute weighted leakage score
        total_samples = len(sample_strings)
        weighted_sum = sum(
            (count / total_samples) * _SEVERITY_WEIGHTS.get(pii_type, 0.5)
            for pii_type, count in matches_by_type.items()
        )
        leakage_score = min(1.0, round(weighted_sum, 4))

        details = {
            "pii_leakage_score": leakage_score,
            "total_samples_scanned": total_samples,
            "matches_found": total_matches,
            "by_type": matches_by_type,
        }

        return leakage_score, details

    def _extract_strings(
        self,
        X_samples: np.ndarray,
        y_samples: Optional[np.ndarray] = None,
    ) -> List[str]:
        """Convert input arrays or list samples into string representations for scanning."""
        strings: List[str] = []

        if isinstance(X_samples, np.ndarray):
            for row in X_samples:
                row_str = " ".join(str(cell) for cell in row.flat if cell is not None)
                if row_str.strip():
                    strings.append(row_str)
        elif isinstance(X_samples, list):
            for item in X_samples:
                if isinstance(item, str):
                    strings.append(item)
                elif isinstance(item, (list, tuple)):
                    strings.append(" ".join(str(x) for x in item))

        if y_samples is not None and isinstance(y_samples, np.ndarray):
            for y_val in y_samples.flat:
                if isinstance(y_val, str) and y_val.strip():
                    strings.append(str(y_val))

        return strings
