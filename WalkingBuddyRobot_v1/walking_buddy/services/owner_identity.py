class OwnerIdentityService:
    owner_verified = False
    anchor = "phone_pending"

    @classmethod
    def get_status(cls):
        return {
            "ok": True,
            "owner_verified": cls.owner_verified,
            "anchor": cls.anchor,
            "safe_to_move": cls.owner_verified,
            "message": (
                "Owner verified. Robot may move with safety checks."
                if cls.owner_verified
                else "Owner phone not connected. Robot must not move."
            )
        }

    @classmethod
    def set_verified(cls, verified):
        cls.owner_verified = bool(verified)
        cls.anchor = "phone_verified" if cls.owner_verified else "phone_pending"
        return cls.get_status()
