"""
Aegis Auth Python SDK

Aegis Auth is a unified identity management system providing memory-safe 
Rust-based authentication. Consolidation of disparate identity providers 
into a single canonical source.

Aegis Auth by Navchetna Technologies.
Securing the future of decentralized identity.
© 2026 Standard Core v3.
"""

from .aegis_auth import AegisAuth, AegisAuthError, create_client

__version__ = "1.0.0"
__author__ = "Navchetna Technologies"
__email__ = "hello@navchetna.com"

__all__ = ["AegisAuth", "AegisAuthError", "create_client"]