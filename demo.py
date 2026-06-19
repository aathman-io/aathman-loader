from loader import trust_load
from errors import TrustViolationError

MODEL_PATH = "model.pth"
CERT_PATH = "model.pth.aathman.json"
POLICY_PATH = "policy.yaml"
MTM_PATH = "model.mtm.yaml"  


def main():
    try:
        trust_load(
            model_path=MODEL_PATH,
            cert_path=CERT_PATH,
            policy_path=POLICY_PATH,
            mtm_path=MTM_PATH,
        )
    except TrustViolationError as e:
        print("DENIED")
        print(f"Stage: {e.stage}")
        print(f"Reason: {e.reason}")
        return

    print("SUCCESS: model loaded")


if __name__ == "__main__":
    main()
