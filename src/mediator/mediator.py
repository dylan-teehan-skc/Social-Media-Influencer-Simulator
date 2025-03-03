# mediator.py
class Mediator:
    def __init__(self):
        self.game_manager = None
        self.ui_logic = None

    def set_game_manager(self, game_manager):
        self.game_manager = game_manager

    def set_ui_logic(self, ui_logic):
        self.ui_logic = ui_logic

    def notify(self, sender, event):
        if sender == self.game_manager:
            # Handle events from GameManager
            self.ui_logic.handle_event(event)
        elif sender == self.ui_logic:
            # Handle events from UILogic
            self.game_manager.handle_event(event)

    def get_view(self):
        return self.ui_logic.view 
    
    def get_ui_logic(self):
        return self.ui_logic 