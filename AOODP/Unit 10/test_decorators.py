import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock
from decorators import ActionContext, LoggingDecorator, Action


class TestLoggingDecorator(unittest.TestCase):

    def test_execute_success_path_logs_start_and_finish(self) -> None:
        # Arrange
        context = ActionContext(
            correlation_id="corr-123",
            user_id="user-1",
            payload="dummy-payload"
        )
        
        # Create a mock action that completes successfully
        mock_inner_action = Mock(spec=Action)
        decorator = LoggingDecorator(inner_action=mock_inner_action)

        # Act
        # Capture standard output stream to verify our log lines
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            decorator.execute(context)

        output = buffer.getvalue()

        # Assert
        # 1. Verify delegation occurred
        mock_inner_action.execute.assert_called_once_with(context)
        
        # 2. Verify lifecycle logs were printed
        self.assertIn("[START] Request corr-123: Processing action.", output)
        self.assertIn("[FINISH] Request corr-123: Action completed successfully.", output)
        self.assertNotIn("[FAIL]", output)

    def test_execute_failure_path_logs_start_and_fail_and_re_raises(self) -> None:
        # Arrange
        context = ActionContext(
            correlation_id="corr-999",
            user_id="user-1",
            payload="dummy-payload"
        )
        
        # Create a mock action that throws an exception when executed
        mock_inner_action = Mock(spec=Action)
        mock_inner_action.execute.side_effect = ValueError("Validation error occurred.")
        
        decorator = LoggingDecorator(inner_action=mock_inner_action)

        # Act & Assert
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            # Assert that the exception is successfully bubbled up (transparently re-raised)
            with self.assertRaises(ValueError) as context_manager:
                decorator.execute(context)

        output = buffer.getvalue()

        # Assertions
        # 1. Verify the exception message is unchanged
        self.assertEqual(str(context_manager.exception), "Validation error occurred.")
        
        # 2. Verify correct failure logging occurred
        self.assertIn("[START] Request corr-999: Processing action.", output)
        self.assertIn("[FAIL] Request corr-999: Action failed. Error: Validation error occurred.", output)
        self.assertNotIn("[FINISH]", output)


if __name__ == "__main__":
    unittest.main()

