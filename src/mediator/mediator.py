class Mediator:
    """
    Mediator class is responsible for organizing the interaction between the GameManager and the UILogic.
    Notify method is used to notify the GameManager or UILogic of an event.
    """
    def __init__(self):
        self.game_manager = None
        self.ui_logic = None

    def set_game_manager(self, game_manager):
        self.game_manager = game_manager

    def set_ui_logic(self, ui_logic):
        self.ui_logic = ui_logic

    def notify(self, sender, event):
        if sender == self.game_manager:
            self.ui_logic.handle_event(event)
        elif sender == self.ui_logic:
            self.game_manager.handle_event(event)

    def get_view(self):
        return self.ui_logic.view

    def get_ui_logic(self):
        return self.ui_logic
