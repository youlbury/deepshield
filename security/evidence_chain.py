import hashlib
import json
import os
import time
import datetime


try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class EvidenceChain:

    _private_key = None
    _public_key = None
    _serial_counter = 0
    _keys_initialized = False

    @classmethod
    def _init_keys(cls):
        if cls._keys_initialized:
            return

        if not CRYPTO_AVAILABLE:
            cls._keys_initialized = True
            return

        key_dir = "evidence"
        os.makedirs(key_dir, exist_ok=True)
        key_path = os.path.join(key_dir, "rsa_private.pem")

        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                cls._private_key = serialization.load_pem_private_key(
                    f.read(), password=None
                )
        else:
            cls._private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=2048
            )
            with open(key_path, "wb") as f:
                f.write(cls._private_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption()
                ))

        cls._public_key = cls._private_key.public_key()
        cls._keys_initialized = True

    @staticmethod
    def _generate_evidence_id():
        year = datetime.datetime.now().year
        EvidenceChain._serial_counter += 1
        return f"DS{year}{EvidenceChain._serial_counter:05d}"

    @staticmethod
    def _dual_hash(file_path):
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
                sha256.update(chunk)
        return md5.hexdigest(), sha256.hexdigest()

    @staticmethod
    def _generate_timestamp():
        now = datetime.datetime.now()
        ms = int(time.time() * 1000) % 1000
        return now.strftime(f'%Y-%m-%dT%H:%M:%S.{ms:03d}')

    @classmethod
    def _sign_data(cls, data_bytes):
        if not CRYPTO_AVAILABLE or cls._private_key is None:
            return None

        try:
            signature = cls._private_key.sign(
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return signature.hex()
        except Exception as e:
            print(f"Warning: RSA signing failed: {e}")
            return None

    @classmethod
    def _verify_signature(cls, data_bytes, signature_hex):
        if not CRYPTO_AVAILABLE or cls._public_key is None:
            return False

        try:
            signature = bytes.fromhex(signature_hex)
            cls._public_key.verify(
                signature,
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    @classmethod
    def archive(cls, file_path, detect_result):
        cls._init_keys()

        hash_md5, hash_sha256 = cls._dual_hash(file_path)
        evidence_id = cls._generate_evidence_id()
        timestamp = cls._generate_timestamp()
        evidence_data = {
            "evidence_id": evidence_id,
            "timestamp": timestamp,
            "hash_md5": hash_md5,
            "hash_sha256": hash_sha256,
            "modality": detect_result.get("modality"),
            "payload": detect_result.get("payload", {}),
            "integrity_status": "VERIFIED"
        }

        # RSA 数字签名
        data_bytes = json.dumps(evidence_data, sort_keys=True, ensure_ascii=False).encode('utf-8')
        signature = cls._sign_data(data_bytes)
        if signature:
            evidence_data["digital_signature"] = signature
            evidence_data["signature_algorithm"] = "RSA-2048-PSS-SHA256"

        # 持久化
        os.makedirs("evidence", exist_ok=True)
        evidence_path = os.path.join("evidence", f"{evidence_id}.json")
        with open(evidence_path, 'w', encoding='utf-8') as f:
            json.dump(evidence_data, f, indent=4, ensure_ascii=False)

        return evidence_data

    @classmethod
    def verify(cls, evidence_id):
        cls._init_keys()

        evidence_path = os.path.join("evidence", f"{evidence_id}.json")
        if not os.path.exists(evidence_path):
            return {"valid": False, "message": f"未找到证据编号: {evidence_id}"}

        with open(evidence_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        signature_hex = data.pop("digital_signature", None)
        data.pop("signature_algorithm", None)

        result = {
            "evidence_id": evidence_id,
            "timestamp": data.get("timestamp"),
            "hash_md5": data.get("hash_md5"),
            "hash_sha256": data.get("hash_sha256"),
            "modality": data.get("modality"),
        }

        # 签名验证
        if signature_hex:
            data_bytes = json.dumps(data, sort_keys=True, ensure_ascii=False).encode('utf-8')
            sig_valid = cls._verify_signature(data_bytes, signature_hex)
            result["signature_valid"] = sig_valid
            if sig_valid:
                result["valid"] = True
                result["message"] = "证据验证通过，未被篡改"
            else:
                result["valid"] = False
                result["message"] = "签名校验失败，证据可能已被篡改"
        else:
            result["signature_valid"] = False
            result["valid"] = True
            result["message"] = "证据存在（无数字签名，仅哈希校验）"

        return result
