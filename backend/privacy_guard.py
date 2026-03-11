"""
privacy_guard.py

DIMDEA - Carbon Emission Intelligence System
Module: PrivacyGuard

Purpose:
Implement privacy-preserving logic including:
- Data anonymization
- Data minimization
- Sensitive field masking
- Role-based access filtering

NOTE:
- No database logic
- No API routes
- No UI rendering
- No carbon business logic
"""

from typing import Dict, Any, List, Tuple
import hashlib
import copy
import logging


# --------------------------------------------------
# Logging (Added for backend debugging support)
# --------------------------------------------------

logger = logging.getLogger("DIMDEA.PrivacyGuard")


class PrivacyGuard:
    """
    PrivacyGuard enforces privacy-by-design principles
    for structured organizational data.
    """

    # -----------------------------
    # Configurable Constants
    # -----------------------------

    SENSITIVE_KEYS = {"name", "email", "phone", "address", "id"}
    ALLOWED_FIELDS_DEFAULT = {"organization_id", "sector", "emissions", "year"}
    ROLES = {"admin", "analyst", "viewer"}

    def __init__(self, data: Dict[str, Any], role: str):
        """
        Initialize PrivacyGuard.

        :param data: Structured dictionary input
        :param role: Access role (admin, analyst, viewer)
        """

        # fallback safety
        if role is None:
            role = "viewer"

        self._validate_input(data, role)

        self.original_data = data
        self.role = role.lower()

        logger.info(f"PrivacyGuard initialized with role: {self.role}")

    # -----------------------------
    # Input Validation
    # -----------------------------

    def _validate_input(self, data: Dict[str, Any], role: str) -> None:

        if not isinstance(data, dict):
            raise TypeError("Input data must be a dictionary.")

        if role.lower() not in self.ROLES:
            raise ValueError(f"Role must be one of {self.ROLES}.")

    # -----------------------------
    # Utility Methods
    # -----------------------------

    def _hash_value(self, value: Any) -> str:
        """
        Hash sensitive value using SHA-256.
        """
        return hashlib.sha256(str(value).encode()).hexdigest()

    def _mask_sensitive_fields(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """
        Mask sensitive fields in dictionary.
        """

        masked_fields = []
        sanitized = copy.deepcopy(data)

        for key in sanitized.keys():

            if key.lower() in self.SENSITIVE_KEYS:
                sanitized[key] = self._hash_value(sanitized[key])
                masked_fields.append(key)

        return sanitized, masked_fields

    def _minimize_data(self, data: Dict[str, Any], allowed_fields: set) -> Dict[str, Any]:
        """
        Remove fields not in allowed list.
        """

        return {k: v for k, v in data.items() if k in allowed_fields}

    # -----------------------------
    # Role-Based Access Logic
    # -----------------------------

    def _apply_role_policy(self) -> Dict[str, Any]:
        """
        Apply role-based privacy filtering.
        """

        original_fields_count = len(self.original_data)
        masked_fields = []

        if self.role == "admin":

            # Full access
            sanitized_data = copy.deepcopy(self.original_data)
            privacy_status = "Full Access - No Masking Applied"

        elif self.role == "analyst":

            # Mask sensitive fields
            sanitized_data, masked_fields = self._mask_sensitive_fields(self.original_data)
            privacy_status = "Sensitive Fields Masked"

        else:  # viewer

            # Only allow minimal fields
            minimized = self._minimize_data(self.original_data, self.ALLOWED_FIELDS_DEFAULT)

            sanitized_data, masked_fields = self._mask_sensitive_fields(minimized)

            privacy_status = "Restricted & Masked Access"

        logger.info(f"Privacy policy applied for role: {self.role}")

        return {
            "sanitized_data": sanitized_data,
            "original_fields_count": original_fields_count,
            "sanitized_fields_count": len(sanitized_data),
            "masked_fields": masked_fields,
            "role_applied": self.role,
            "privacy_status": privacy_status
        }

    # -----------------------------
    # Public Method
    # -----------------------------

    def enforce_privacy(self) -> Dict[str, Any]:
        """
        Enforce privacy controls and return structured report.
        """

        result = self._apply_role_policy()

        logger.info("Privacy enforcement completed")

        return {
            "original_fields_count": result["original_fields_count"],
            "sanitized_fields_count": result["sanitized_fields_count"],
            "masked_fields": result["masked_fields"],
            "role_applied": result["role_applied"],
            "privacy_status": result["privacy_status"],
            "sanitized_data": result["sanitized_data"]
        }


# ---------------------------------------
# Example Standalone Execution
# ---------------------------------------

if __name__ == "__main__":

    sample_input = {
        "name": "GreenTech Industries",
        "email": "contact@greentech.com",
        "phone": "9876543210",
        "address": "Chennai, India",
        "organization_id": "GTX-2024",
        "sector": "Manufacturing",
        "emissions": 12000,
        "year": 2024
    }

    try:

        print("\n===== ADMIN VIEW =====")
        admin_guard = PrivacyGuard(sample_input, role="admin")
        print(admin_guard.enforce_privacy())

        print("\n===== ANALYST VIEW =====")
        analyst_guard = PrivacyGuard(sample_input, role="analyst")
        print(analyst_guard.enforce_privacy())

        print("\n===== VIEWER VIEW =====")
        viewer_guard = PrivacyGuard(sample_input, role="viewer")
        print(viewer_guard.enforce_privacy())

    except Exception as e:
        print(f"Error: {e}")