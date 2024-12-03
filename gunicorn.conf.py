
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120
accesslog = "-"  # Logs de acesso no console
errorlog = "-"  # Logs de erro no console
loglevel = "info"  # Nível de log
