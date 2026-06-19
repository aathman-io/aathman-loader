import sys
import os
import torch

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

BASE_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))

sys.path.insert(0, os.path.join(BASE_DIR, "aathman-core"))
sys.path.insert(0, os.path.join(BASE_DIR, "aathman-pacm"))
sys.path.insert(0, os.path.join(BASE_DIR, "aathman-mtm"))

from errors import TrustViolationError
from verify import verify_model
from pacm import load_policy, evaluate_policy
from validator import load_and_enforce_mtm

def trust_load(
    model_path: str,
    cert_path: str,
    policy_path: str,
    mtm_path: str | None = None,
):
    
    try:
        verification_facts = verify_model(model_path, cert_path)
    except Exception as e:
        raise TrustViolationError(
            stage="verification",
            reason=str(e)
        )

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

    try:
        model = torch.load(model_path, map_location="cpu")
    except Exception:
        raise TrustViolationError(
            stage="load",
            reason="Model loading failed after trust checks"
        )

    return model
