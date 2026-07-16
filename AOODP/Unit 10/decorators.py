from actions import Action, ActionContext


class LoggingDecorator(Action):
    def __init__(self, inner_action: Action) -> None:
        self.inner_action = inner_action

    def execute(self, context: ActionContext) -> None:
        print(f"[START] Request {context.correlation_id}: Processing action.")
        try:
            self.inner_action.execute(context)
            print(f"[FINISH] Request {context.correlation_id}: Action completed successfully.")
        except Exception as e:
            print(f"[FAIL] Request {context.correlation_id}: Action failed. Error: {e}")
            raise
