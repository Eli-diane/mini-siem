from django.shortcuts import render
from django.http import JsonResponse
import json
import socket
import psutil
import platform
import urllib.request
import os
from google import genai
from .models import LogVarredura

def scanner_view(request):
    historico = LogVarredura.objects.all().order_by('-data_hora')[:5]
    return render(request, 'core/scanner.html', {'historico': historico})

def consultar_ollama_local(prompt_texto):
    url = "http://localhost:11434/api/generate"
    
    # PROMPT BLINDADO: EXIGE O PASSO A PASSO COMPLETO DE SOC
    prompt_rigido = f"""
    [RESTRIÇÃO CRÍTICA DE SOC]
    Você é um motor de resposta a incidentes (SOAR) sênior. O operador humano precisa de um guias operacional COMPLETO e SEQUENCIAL para resolver o problema na prática, e não apenas uma linha solta.
    
    REGRAS OBRIGATÓRIAS DE SAÍDA:
    1. DIAGNÓSTICO: Explique a causa raiz em 1 linha.
    2. PASSO 1 (AUDITORIA): Forneça o comando PowerShell para coletar a evidência.
    3. PASSO 2 (IDENTIFICAÇÃO): Forneça o comando PowerShell para filtrar o PID ou o processo culpado.
    4. PASSO 3 (CONTENÇÃO): Forneça o comando PowerShell seguro (ex: Stop-Process -Id [PID] -Force).
    
    Responda estritamente usando blocos de código PowerShell limpos para cada passo.
    
    Solicitação do operador: {prompt_texto}
    """
    
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt_rigido,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 450 # Aumentado para garantir que ele escreva o passo a passo inteiro
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            resposta_json = json.loads(response.read().decode('utf-8'))
            conteudo = resposta_json.get('response', 'Sem retorno.')
            return f"[🛡️ MODO MANUAL - OLLAMA LOCAL (QWEN 2.5)]\n\n{conteudo}"
    except Exception as e:
        return f"[ERRO CRÍTICO] Ollama local indisponível na porta 11434. ({str(e)})"

def consultar_gemini_nuvem(prompt_texto):
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "[ERRO DE CONFIGURAÇÃO] A chave GEMINI_API_KEY não está definida no ambiente."
            
        client = genai.Client(api_key=api_key)
        prompt_completo = f"""
        Você é o copiloto de um analista de SOC. Quando houver um alerta, forneça um guia prático passo a passo contendo:
        1. O comando de auditoria inicial.
        2. O comando para identificar o PID exato do processo problemático.
        3. O comando cirúrgico de contenção (Stop-Process).
        Mantenha a formatação limpa com blocos PowerShell.
        
        Alerta/Solicitação: {prompt_texto}
        """
        response = client.models.generate_content(
            model='gemini-3.6-flash', 
            contents=prompt_completo
        )
        if response and response.text:
            return f"[☁️ IA NUVEM - GEMINI FLASH]\n\n{response.text}"
        return "[AVISO] Resposta vazia da nuvem."
    except Exception as e:
        return f"[ERRO DE CONEXÃO COM A NUVEM] {str(e)}. Use o Ollama Local."

def api_dados_tempo_real(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            acao = body.get('acao')
            sistema_atual = platform.system()
            motor_ia = body.get('motor', 'gemini')
            
            if acao == 'analisar_incidente':
                detalhes_incidente = body.get('incidente', 'Anomalia de sistema')
                prompt = f"Alerta crítico no host ({sistema_atual}): {detalhes_incidente}. Forneça o passo a passo completo de auditoria e contenção."
                
                if motor_ia == 'ollama':
                    resposta = consultar_ollama_local(prompt)
                else:
                    resposta = consultar_gemini_nuvem(prompt)
                return JsonResponse({'status': 'sucesso', 'resposta_ia': resposta})

            elif acao == 'corrigir_erro':
                erro_retornado = body.get('erro', '')
                prompt_chat = f"Suporte SOC ({sistema_atual}). Erro no terminal: '{erro_retornado}'. Forneça a solução passo a passo."
                
                if motor_ia == 'ollama':
                    resposta_ia = consultar_ollama_local(prompt_chat)
                else:
                    resposta_ia = consultar_gemini_nuvem(prompt_chat)
                return JsonResponse({'status': 'sucesso', 'resposta_ia': resposta_ia})

            elif acao == 'concluir':
                dificuldade = body.get('dificuldade', 'Nenhuma registrada')
                incidente_detalhes = body.get('incidente', 'Incidente de sistema')
                prompt_doc = f"Relatório CISO e SOC para: '{incidente_detalhes}'. Obs: '{dificuldade}'. Gere o Post-Mortem executivo."
                
                if motor_ia == 'ollama':
                    documentacao_final = consultar_ollama_local(prompt_doc)
                else:
                    documentacao_final = consultar_gemini_nuvem(prompt_doc)
                    
                LogVarredura.objects.create(detalhes=f"Incidente mitigado ({motor_ia.upper()}). Obs: {dificuldade}")
                return JsonResponse({'status': 'sucesso', 'documentacao': documentacao_final})
                
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

    resultados_portas = []
    conexoes_rede = []
    target = "127.0.0.1"
    ports_to_check = [21, 22, 80, 443, 3306, 5432, 8000, 8080, 3389]
    
    for port in ports_to_check:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((target, port)) == 0:
            resultados_portas.append(f"Porta {port} está ABERTA")
        else:
            resultados_portas.append(f"Porta {port} está fechada")
        s.close()
        
    try:
        conexoes = psutil.net_connections(kind='inet')
        for conn in reversed(conexoes[:12]):
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "Escutando"
            conexoes_rede.append(f"Local: {laddr} <-> Remoto: {raddr} [Status: {conn.status}]")
    except Exception as e:
        conexoes_rede.append(f"Erro de rede: {str(e)}")
        
    cpu_uso = psutil.cpu_percent(interval=None)
    forcar_simulacao = request.GET.get('simular') == '1'
    
    alerta = None
    ia_analise = None

    if cpu_uso > 85 or forcar_simulacao:
        motivo = "Simulação Manual de Ataque Crítico" if forcar_simulacao else f"Uso de CPU em {cpu_uso}%"
        alerta = f"[ALERTA CRÍTICO - SOC] {motivo}: Anomalia detectada!"
        ia_analise = consultar_gemini_nuvem(f"Alerta crítico no host: {motivo}. Forneça o guia operacional completo de SOC.")

    return JsonResponse({
        'portas': resultados_portas,
        'conexoes': conexoes_rede,
        'cpu': cpu_uso,
        'alerta': alerta,
        'ia_analise': ia_analise
    })
