import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock
from actions import ActionContext, SubmitAssignmentAction, SubmitAssignmentPayload


class TestSubmitAssignmentAction(unittest.TestCase):
    # ... (previous validation tests remain here) ...

    def test_execute_valid_payload_saves_submission_to_repository(self) -> None:
        # Arrange
        valid_payload = SubmitAssignmentPayload(
            assignment_id="assignment-123",
            student_id="student-999",
            file_content=b"pdf_mock_data",
            student_comments="My submission notes."
        )

        context = ActionContext(
            correlation_id="test-corr-id-003",
            user_id="student-999",
            payload=valid_payload
        )

        # 1. Create our Spy-capable Mock Repository
        mock_repo = Mock()
        
        # 2. Inject it into the constructor (this will break our validation tests, which we'll fix next!)
        action = SubmitAssignmentAction(repository=mock_repo)

        # Act
        # Record the time right before execution so we can verify the timestamp side-effect
        test_start_time = datetime.now(timezone.utc)
        action.execute(context)

        # Assert
        # 1. Verify the save method was called exactly once
        mock_repo.save.assert_called_once()

        # 2. Inspect the actual Submission object passed to save()
        # call_args[0][0] retrieves the first positional argument of the first call
        saved_submission = mock_repo.save.call_args[0][0]

        self.assertEqual(saved_submission.student_id, "student-999")
        self.assertEqual(saved_submission.assignment_id, "assignment-123")
        self.assertEqual(saved_submission.file_content, b"pdf_mock_data")
        self.assertEqual(saved_submission.comments, "My submission notes.")

        # 3. Resolve the Timestamp Wrinkle:
        # Assert that submitted_at exists and occurred within a 2-second window of our start time
        self.assertIsNotNone(saved_submission.submitted_at)
        time_difference = saved_submission.submitted_at - test_start_time
        self.assertTrue(
            timedelta(seconds=0) <= time_difference <= timedelta(seconds=2),
            f"Submission timestamp {saved_submission.submitted_at} was outside the expected execution window."
        )
