import sys
import os
import torch

# ------------------------------------------------------------------
# Ensure loader directory is importable
# ------------------------------------------------------------------

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

BASE_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))

# Sibling repos (intentional for now)
sys.path.insert(0, os.path.join(BASE_DIR, "aathman-core"))
sys.path.insert(0, os.path.join(BASE_DIR, "aathman-pacm"))
sys.path.insert(0, os.path.join(BASE_DIR, "aathman-mtm"))

# ------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------

from errors import TrustViolationError

# Aathman Core
from verify import verify_model

# PaCM
from pacm import load_policy, evaluate_policy

# MTM (public API lives in validator.py)
from validator import load_and_enforce_mtm

# ------------------------------------------------------------------
# Trust-aware model loader
# ------------------------------------------------------------------

def trust_load(
    model_path: str,
    cert_path: str,
    policy_path: str,
    mtm_path: str | None = None,
):
    """
    Load a model only if all trust checks pass.

    Order:
    1. Identity verification (Aathman Core)
    2. Policy enforcement (PaCM)
    3. Intent enforcement (MTM)
    4. Model loading
    """

    # 1. Verify model identity (Aathman Core)
    try:
        verification_facts = verify_model(model_path, cert_path)
    except Exception as e:
        raise TrustViolationError(
            stage="verification",
            reason=str(e)
        )

    # 2. Enforce policy (PaCM)
    try:
        policy = load_policy(policy_path)
        result = evaluate_policy(policy, verification_facts)
    except Exception as e:
        raise TrustViolationError(
            stage="policy",
            reason=str(e)
        )

    if result["decision"] != "ALLOW":
        raise TrustViolationError(
            stage="policy",
            reason=f"Policy denied model usage: {result['reason']}"
        )

    # 3. Validate and enforce MTM (optional)
    if mtm_path is not None:
        try:
            load_and_enforce_mtm(mtm_path)
        except TrustViolationError:
            raise
        except Exception as e:
            raise TrustViolationError(
                stage="mtm_validation",
                reason=str(e)
            )

    # 4. Load model (only after all checks pass)
    try:
        model = torch.load(model_path, map_location="cpu")
    except Exception:
        raise TrustViolationError(
            stage="load",
            reason="Model loading failed after trust checks"
        )

    return model
