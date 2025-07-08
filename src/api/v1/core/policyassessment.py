class PolicyAssessment:
    base_path = "api/v1/core/policyassessment/"

    @classmethod
    def check_done(cls, assessment_id):
        return cls.base_path + f"{assessment_id}/check_done/"

    @classmethod
    def check_status(cls, external_id):
        return cls.base_path + f"check_status/?external_id={external_id}"
