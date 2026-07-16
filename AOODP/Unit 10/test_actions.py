import unittest
from actions import ActionContext, SubmitAssignmentAction, SubmitAssignmentPayload


class TestSubmitAssignmentAction(unittest.TestCase):
    def test_execute_missing_file_content_raises_value_error(self) -> None:
        # Arrange: Create a payload specifically missing the file content
        invalid_payload = SubmitAssignmentPayload(
            assignment_id="assignment-abc-123",
            student_id="student-999",
            file_content=None,  # The trigger for the failure
            student_comments="Here is my submission, hope it's okay!",
        )
        context = ActionContext(
            correlation_id="test-corr-id-001",
            user_id="student-999",
            payload=invalid_payload,
        )
        action = SubmitAssignmentAction()

        # Act & Assert: Running the action must raise a ValueError
        # and the message must specifically mention "file content"
        with self.assertRaises(ValueError) as exc_info:
            action.execute(context)
        self.assertIn("file content", str(exc_info.exception).lower())


if __name__ == "__main__":
    unittest.main()
