import json
import os
from datetime import datetime
from typing import Optional
from config import LOG_DIR

class JSONLogger:
    """
    Klasa do logowania informacji o procesie przetwarzania obrazów w formacie JSON.
    """
    
    def __init__(self, log_filename: str = "process_log.json"):
        """
        Inicjalizuje JSONLogger.
        
        Args:
            log_filename: Nazwa pliku JSON do zapisywania logów
        """
        self.log_file_path = os.path.join(LOG_DIR, log_filename)
        self.current_process = {}
        
    def start_process(self, input_filename: str):
        """
        Rozpoczyna nowy proces logowania dla danego pliku wejściowego.
        
        Args:
            input_filename: Nazwa pliku wejściowego
        """
        self.current_process = {
            "timestamp": datetime.now().isoformat(),
            "input_file": input_filename,
            "style_description": None,
            "generation_prompt": None,
            "video_prompt": None,
            "output_image": None,
            "output_video": None,
            "status": "started"
        }
    
    def log_style_description(self, description: str):
        """
        Zapisuje opis stylu obrazu.
        
        Args:
            description: Opis stylu wygenerowany przez ImageDescriber
        """
        self.current_process["style_description"] = description
    
    def log_generation_prompt(self, prompt: str):
        """
        Zapisuje prompt do generowania obrazu.
        
        Args:
            prompt: Prompt wygenerowany przez PromptCreator
        """
        self.current_process["generation_prompt"] = prompt
    
    def log_video_prompt(self, prompt: str):
        """
        Zapisuje prompt do generowania wideo.
        
        Args:
            prompt: Prompt wprowadzony przez użytkownika
        """
        self.current_process["video_prompt"] = prompt
    
    def log_output_image(self, image_path: str):
        """
        Zapisuje ścieżkę do wygenerowanego obrazu.
        
        Args:
            image_path: Ścieżka do wygenerowanego obrazu
        """
        self.current_process["output_image"] = os.path.basename(image_path)
    
    def log_output_video(self, video_path: str):
        """
        Zapisuje ścieżkę do wygenerowanego wideo.
        
        Args:
            video_path: Ścieżka do wygenerowanego wideo
        """
        self.current_process["output_video"] = os.path.basename(video_path)
    
    def finish_process(self, success: bool = True):
        """
        Kończy proces i zapisuje dane do pliku JSON.
        
        Args:
            success: Czy proces zakończył się sukcesem
        """
        self.current_process["status"] = "completed" if success else "failed"
        self.current_process["completed_at"] = datetime.now().isoformat()
        
        # Wczytaj istniejące logi lub utwórz nową listę
        logs = []
        if os.path.exists(self.log_file_path):
            try:
                with open(self.log_file_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logs = []
        
        # Dodaj nowy log
        logs.append(self.current_process.copy())
        
        # Zapisz do pliku
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def get_all_logs(self) -> list:
        """
        Zwraca wszystkie zapisane logi.
        
        Returns:
            Lista wszystkich logów
        """
        if os.path.exists(self.log_file_path):
            try:
                with open(self.log_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return [] 