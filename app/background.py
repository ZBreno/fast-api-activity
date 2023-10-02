from datetime import datetime

def audit_log_recipes(recipe_id: str, message=""): 
    with open("C:/Users/breno/OneDrive/Documentos/Pyhton/Desenvolvimento de Sistemas Corporativos/Atividade de Fast-API 01/app/audit_log.txt", mode="a") as logfile:
        content = f"\nrecipe {recipe_id} executed {message} at {datetime.now()}"
        logfile.write(content)